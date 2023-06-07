import streamlit as st
import pandas as pd
import requests
from PIL import Image
import io
import googlemaps

# Set the page layout
st.set_page_config(layout="wide")

def main():
    st.title("Localizador de tiendas")

st.title('Bienvenido al recomendador de mascotas')

# Initialize the Google Maps Geocoding client with your API key
gmaps = googlemaps.Client(key='AIzaSyDpY4rSYCn3_B59-hxMT9cesG0O7cSkUnM')

groups = [
    {
        'group_name': 'PROTECTORAS DE ANIMALES',
        'keyword': 'protectora animales, animal shelter',
        'radius_prompt': "Radio de búsqueda en metros para protectoras: "
    },
    {
        'group_name': 'VETERINARIOS',
        'keyword': 'Veterinario, Veterinary',
        'radius_prompt': "Radio de búsqueda en metros para veterinarios: "
    },
    {
        'group_name': 'TIENDAS DE MASCOTAS',
        'keyword': 'Tiendas de mascotas, pet shop, animal shop, tienda de animales',
        'radius_prompt': "Radio de búsqueda en metros para tiendas de mascotas: "
    },
    {
        'group_name': 'CRIADORES DE PERROS',
        'keyword': 'Criadores, criadores de perros, dog breeders, kennels, cat breeders, criadores de gatos',
        'radius_prompt': "Radio de búsqueda en metros para criadores: "
    }
]

def get_distance(origin, destination):
    distance = gmaps.distance_matrix(
        origins=origin,
        destinations=destination,
        mode='walking'
    )['rows'][0]['elements'][0]['distance']['text']
    return distance

def convert_distance_to_numeric(distance):
    if isinstance(distance, float):
        return distance
    else:
        numeric_distance = float(distance.split(' ')[0])
        return numeric_distance

def find_nearest_shop(origin, shops):
    nearest_shop = None
    min_distance = float('inf')

    for shop in shops:
        shop_latitude = shop['geometry']['location']['lat']
        shop_longitude = shop['geometry']['location']['lng']
        distance = get_distance(origin, (shop_latitude, shop_longitude))
        numeric_distance = convert_distance_to_numeric(distance)
        if numeric_distance < min_distance:
            min_distance = numeric_distance
            nearest_shop = shop

    return nearest_shop, min_distance

def geocode_address(address):
    geocode_result = gmaps.geocode(address)

    if geocode_result:
        location = geocode_result[0]['geometry']['location']
        latitude = location['lat']
        longitude = location['lng']
        return latitude, longitude
    else:
        st.warning("No se encontró la dirección. Ingresa una dirección válida.")
        return None, None


# Sidebar
sidebar_width = 300
st.sidebar.title("Opciones")
address = st.sidebar.text_input("Ingresa una dirección:")

latitude, longitude = geocode_address(address)
if latitude is not None and longitude is not None:
    closest_shops = []

    for group in groups:
        group_name = group['group_name']
        keyword = group['keyword']
        radius_prompt = group['radius_prompt']

        with st.sidebar.expander(group_name):
            radius = st.number_input(radius_prompt, value=1000)

            if radius == 0:
                st.warning(f"El radio debe ser mayor que cero. No se puede realizar la búsqueda para {group_name}.")
                closest_shops.append(None)
                continue

            response = gmaps.places_nearby(
                location=(latitude, longitude),
                radius=radius,
                keyword=keyword
            )

            shops = response['results']

            if not shops:
                st.warning(f"NO HAY RESULTADOS PARA {group_name} (Rango: {radius} m)")
                closest_shops.append(None)
            else:
                st.subheader(f"RESULTADOS PARA {group_name} (Rango: {radius} m):")
                for shop in shops:
                    st.write(f"Nombre: {shop['name']}")
                    st.write(f"Dirección: {shop['vicinity']}")
                    st.write(f"Distancia: {convert_distance_to_numeric(get_distance((latitude, longitude), (shop['geometry']['location']['lat'], shop['geometry']['location']['lng'])))} m")
                    st.write('---')

                nearest_shop, min_distance = find_nearest_shop((latitude, longitude), shops)

                closest_shops.append({
                    'name': nearest_shop['name'],
                    'vicinity': nearest_shop['vicinity'],
                    'distance': min_distance
                })

    st.subheader("TIENDA MÁS CERCANA POR CATEGORÍA:")
    for i, group in enumerate(groups):
        group_name = group['group_name']
        closest_shop = closest_shops[i]
        if closest_shop is None:
            st.write(f"No hay tiendas cercanas para {group_name}.")
        else:
            st.write(f"Para {group_name}:")
            st.write(f"Nombre: {closest_shop['name']}")
            st.write(f"Dirección: {closest_shop['vicinity']}")
            st.write(f"Distancia: {convert_distance_to_numeric(closest_shop['distance'])} m")
            st.write('---')


# Pre-load the CSV file
perros_data = pd.read_csv('Dog CSVs/TablaPerra.csv')
gatos_data = pd.read_csv('Cat CSVs/TablaGatuna.csv')

st.write('# ¿Qué tipo de animal quieres?')
# Create a filter to choose between "Perros" and "Gatos"
selection = st.selectbox("Select an animal", ["Perros", "Gatos"])

# Download and display images of remaining breeds
def download_image(url):
    try:
        response = requests.get(url)
        image = Image.open(io.BytesIO(response.content))
        return image
    except Exception as e:
        st.warning(f"Failed to download image from URL: {url}")
        return None

# Display the selected CSV file and apply filters
if selection == "Perros":
    st.dataframe(perros_data)
    st.write('# Aquí tienes algunos filtros básicos que ayudarán a sugerir tu mascota ideal')
    # Define columns to be shown initially
    initial_dogcolumns = ['Tamaño', 'No Alergia', 'Sociable', 'Casa', 'Cuidados']

    # Create filter components
    filters = {}

    # Add filters for selected columns
    for column in initial_dogcolumns:
        unique_values = perros_data[column].unique()
        selected_values = st.multiselect(f'Filtrar por {column}', unique_values)
        if selected_values:
            filters[column] = selected_values

    # Apply filters sequentially
    filtered_data = perros_data.copy()
    for column, values in filters.items():
        filtered_data = filtered_data[filtered_data[column].isin(values)]

    # Display the filtered data
    st.dataframe(filtered_data)

    # Create a table for displaying the images and breed names
    breed_images = []
    breed_names = []

    # Iterate through the filtered data to fetch images and breed names
    for _, row in filtered_data.iterrows():
        breed_images.append(download_image(row['Foto']))
        breed_names.append(row['Raza'])

    # Display the images and breed names in a table
    col1, col2, col3 = st.columns(3)
    for i, (image, breed) in enumerate(zip(breed_images, breed_names)):
        if i % 3 == 0:
            col1.image(image, use_column_width=True)
            col1.write(breed)
        elif i % 3 == 1:
            col2.image(image, use_column_width=True)
            col2.write(breed)
        else:
            col3.image(image, use_column_width=True)
            col3.write(breed)

elif selection == "Gatos":
    st.dataframe(gatos_data)
    st.write('# Aquí tienes algunos filtros básicos que ayudarán a sugerir tu mascota ideal')
    # Define columns to be shown initially
    initial_catcolumns = ['Actividad', 'Sociabilidad', 'Maullido', 'Alergia', 'Niños']

    # Create filter components
    filters = {}

    # Add filters for selected columns
    for column in initial_catcolumns:
        unique_values = gatos_data[column].unique()
        selected_values = st.multiselect(f'Filtrar por {column}', unique_values)
        if selected_values:
            filters[column] = selected_values

    # Apply filters sequentially
    filtered_data = gatos_data.copy()
    for column, values in filters.items():
        filtered_data = filtered_data[filtered_data[column].isin(values)]

    # Display the filtered data
    st.dataframe(filtered_data)

    # Create a table for displaying the images and breed names
    breed_images = []
    breed_names = []

    # Iterate through the filtered data to fetch images and breed names
    for _, row in filtered_data.iterrows():
        breed_images.append(download_image(row['Foto']))
        breed_names.append(row['Raza'])

    # Display the images and breed names in a table
    col1, col2, col3 = st.columns(3)
    for i, (image, breed) in enumerate(zip(breed_images, breed_names)):
        if i % 3 == 0:
            col1.image(image, use_column_width=True)
            col1.write(breed)
        elif i % 3 == 1:
            col2.image(image, use_column_width=True)
            col2.write(breed)
        else:
            col3.image(image, use_column_width=True)
            col3.write(breed)

if __name__ == '__main__':
    main()
