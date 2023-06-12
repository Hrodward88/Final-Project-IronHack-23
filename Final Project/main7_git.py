import streamlit as st
import pandas as pd
import requests
from PIL import Image
import io
import googlemaps
import base64
import folium
from PIL import Image
from io import BytesIO

# Set the page layout
st.set_page_config(layout="wide")




# Function to show breed information
def show_breed_info(breed):
    if selection == "Perros":
        breed_info = perros_data[perros_data["Raza"] == breed]
        if not breed_info.empty:
            st.subheader(f"Información sobre la raza {breed}:")
            # Select specific columns to display
            show_columns = ['Raza', 'País', 'Acerca de', 'Tamaño', 'Rasgo 1', 'Rasgo 2', 'Rasgo 3', 'Rasgo 4', 'Rasgo 5', 'Rasgo 6']
            # Create a DataFrame with the selected columns
            breed_info_subset = breed_info[show_columns].reset_index(drop=True)
            # Set the background color of the DataFrame to white
            breed_info_subset_styled = breed_info_subset.style.set_table_styles(
                [{'selector': 'table', 'props': [('background-color', 'white')]}]
            )
            # Display the styled DataFrame as a table
            st.table(breed_info_subset_styled)
        else:
            st.warning("No se encontró información sobre esta raza.")
    elif selection == "Gatos":
        breed_info = gatos_data[gatos_data["Raza"] == breed]
        if not breed_info.empty:
            st.subheader(f"Información sobre la raza {breed}:")
            show_columns = ['Raza', 'País', 'Origen', 'Descripción']
            breed_info_subset = breed_info[show_columns].reset_index(drop=True)
            breed_info_subset_styled = breed_info_subset.style.set_table_styles(
                [{'selector': 'table', 'props': [('background-color', 'white')]}]
            )
            st.table(breed_info_subset_styled)
        else:
            st.warning("No se encontró información sobre esta raza.")




def main():
    st.title("Localizador de tiendas")




st.title('Bienvenido al recomendador de mascotas HelPet')
st.write('(Versión preliminar, que esto un trabajo muy perro, no se pongan de uñas)')
st.image("header.jpeg", width=600)

# Initialize the Google Maps Geocoding client with your API key
gmaps = googlemaps.Client(key='API_KEY')

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
        'group_name': 'CRIADORES',
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


# Define the column names for each dataframe
perros_columns = ['Raza', 'Tamaño', 'No Alergia', 'País', 'Esperanza de vida promedio']
gatos_columns = ['Raza', 'Constitución', 'Alergia', 'País']


# Pre-load the CSV file
perros_data = pd.read_csv('Dog CSVs/TablaPerra.csv')
gatos_data = pd.read_csv('Cat CSVs/TablaGatuna.csv')

st.markdown('# ¿Qué tipo de animal quieres?')
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
    # Add the image
    st.image("dogportrait.jpeg", width=400)
    st.write('## Así que un perro. Buena elección.')
    st.dataframe(perros_data[perros_columns])
    
    st.write('# Aquí tienes algunos filtros básicos que ayudarán a sugerir tu perro ideal, y algunos datos curiosos')
    # Load the images
    image1 = Image.open('Dogsizes.png')
    image2 = Image.open('Dogallergies.png')
    image3 = Image.open('Dogcountries.png')

    # Calculate the desired width and height for the resized images
    desired_width = 500
    desired_height = 400

    # Resize the images
    resized_image1 = image1.resize((desired_width, desired_height), Image.ANTIALIAS)
    resized_image2 = image2.resize((desired_width, desired_height), Image.ANTIALIAS)
    resized_image3 = image3.resize((desired_width, desired_height), Image.ANTIALIAS)

    # Display the resized images in columns
    col1, col2, col3 = st.columns(3)
    col1.image(resized_image1, use_column_width=True)
    col2.image(resized_image2, use_column_width=True)
    col3.image(resized_image3, use_column_width=True)
    # Define columns to be shown initially
    initial_dogcolumns = ['Tamaño', 'No Alergia', 'Sociable', 'Casa', 'Experiencia', 'Entrenamiento', 'Cuidados']

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
    st.dataframe(filtered_data[perros_columns])

    # Create a table for displaying the images and breed names
    breed_images = []
    breed_names = []

    # Iterate through the filtered data to fetch images and breed names
    for _, row in filtered_data.iterrows():
        breed_images.append(download_image(row['Foto']))
        breed_names.append(row['Raza'])

    # Define the desired width and height for the images
    desired_width = 300
    desired_height = 200

    # Resize the images to the desired size
    resized_images = []
    for image in breed_images:
        resized_image = image.resize((desired_width, desired_height))
        resized_images.append(resized_image)

    # Display the resized images and breed names
    col1, col2, col3 = st.columns(3)
    for i, (image, breed) in enumerate(zip(resized_images, breed_names)):
        if i % 3 == 0:
            col1.image(image, use_column_width=True, caption=breed)
            if col1.button(f'Ver información {filtered_data.iloc[i]["Raza"]}'):
                show_breed_info(breed)
        elif i % 3 == 1:
            col2.image(image, use_column_width=True, caption=breed)
            if col2.button(f'Ver información {filtered_data.iloc[i]["Raza"]}'):
                show_breed_info(breed)
        else:
            col3.image(image, use_column_width=True, caption=breed)
            if col3.button(f'Ver información {filtered_data.iloc[i]["Raza"]}'):
                show_breed_info(breed)


elif selection == "Gatos":
    # Add the image
    st.image("catportrait.jpeg", width=400)
    st.write('## Así que un gato. Buena elección.')
    st.dataframe(gatos_data[gatos_columns])

    st.write('# Aquí tienes algunos filtros básicos que ayudarán a sugerir tu gato ideal, y algunos datos curiosos.')
    # Load the images
    image1 = Image.open('Catsizes.png')
    image2 = Image.open('Catallergies.png')
    image3 = Image.open('Catcountries.png')

    # Calculate the desired width and height for the resized images
    desired_width = 500
    desired_height = 400

    # Resize the images
    resized_image1 = image1.resize((desired_width, desired_height), Image.ANTIALIAS)
    resized_image2 = image2.resize((desired_width, desired_height), Image.ANTIALIAS)
    resized_image3 = image3.resize((desired_width, desired_height), Image.ANTIALIAS)

    # Display the resized images in columns
    col1, col2, col3 = st.columns(3)
    col1.image(resized_image1, use_column_width=True)
    col2.image(resized_image2, use_column_width=True)
    col3.image(resized_image3, use_column_width=True)
    
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
    st.dataframe(filtered_data[gatos_columns])

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
            col1.image(image, use_column_width=True, caption=breed)
            if col1.button(f'Ver información {filtered_data.iloc[i]["Raza"]}'):
                show_breed_info(breed)
        elif i % 3 == 1:
            col2.image(image, use_column_width=True, caption=breed)
            if col2.button(f'Ver información {filtered_data.iloc[i]["Raza"]}'):
                show_breed_info(breed)
        else:
            col3.image(image, use_column_width=True, caption=breed)
            if col3.button(f'Ver información {filtered_data.iloc[i]["Raza"]}'):
                show_breed_info(breed)

# Pre-load the CSV file
perros_data = pd.read_csv('Dog CSVs/TablaPerra.csv')
gatos_data = pd.read_csv('Cat CSVs/TablaGatuna.csv')

if __name__ == '__main__':
    main()

# Get the address from the user
address = st.text_input("Ingresa una dirección:")

# Check if the address is provided
if address:
    latitude, longitude = geocode_address(address)
    
    if latitude is not None and longitude is not None:
        m = folium.Map(location=[latitude, longitude], zoom_start=14)

        # Add a marker for the input address
        folium.Marker(
            location=[latitude, longitude],
            popup="Input Address",
            icon=folium.Icon(color="red", icon="info-sign"),
        ).add_to(m)
        
        closest_shops = []
    
        for group in groups:
            group_name = group['group_name']
            keyword = group['keyword']
            radius_prompt = group['radius_prompt']
    
            with st.expander(group_name):
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
                        shop_latitude = shop['geometry']['location']['lat']
                        shop_longitude = shop['geometry']['location']['lng']
                        shop_name = shop['name']
                        shop_address = shop['vicinity']
                         # Get the shop type based on the group name
                        shop_type = None
                        for group in groups:
                            if group['group_name'] == group_name:
                                shop_type = group['group_name']
                                break

                        # Get the color for the shop type
                        if shop_type == 'PROTECTORAS DE ANIMALES':
                            color = 'green'
                        elif shop_type == 'VETERINARIOS':
                            color = 'blue'
                        elif shop_type == 'TIENDAS DE MASCOTAS':
                            color = 'orange'
                        elif shop_type == 'CRIADORES':
                            color = 'purple'
                        else:
                            color = 'red'  # Default color if no specific color is defined for the shop type
    
                        st.write(f"Nombre: {shop_name}")
                        st.write(f"Dirección: {shop_address}")
                        st.write(f"Distancia: {convert_distance_to_numeric(get_distance((latitude, longitude), (shop_latitude, shop_longitude)))} km")
                        st.write('---')
    
                        # Add a marker for each nearby shop
                        folium.Marker(
                            location=[shop_latitude, shop_longitude],
                            popup=f"Nombre: {shop_name}<br>Dirección: {shop_address}",
                            icon=folium.Icon(color=color, icon="shopping-cart"),
                        ).add_to(m)

                        
                    nearest_shop, min_distance = find_nearest_shop((latitude, longitude), shops)
    
                    closest_shops.append({
                        'name': nearest_shop['name'],
                        'vicinity': nearest_shop['vicinity'],
                        'distance': min_distance
                    })
        # Add legend to the map
        legend_html = '''
            <div style="position: fixed; 
                        bottom: 50px; left: 50px; width: 200px; height: 120px; 
                        border:2px solid grey; z-index:9999; font-size:14px;
                        background-color:white;
                        ">&nbsp;<b>Legend</b><br>
                        &nbsp;<i class="fa fa-circle" style="color:green"></i>&nbsp;Protectoras de Animales<br>
                        &nbsp;<i class="fa fa-circle" style="color:blue"></i>&nbsp;Veterinarios<br>
                        &nbsp;<i class="fa fa-circle" style="color:orange"></i>&nbsp;Tiendas de Mascotas<br>
                        &nbsp;<i class="fa fa-circle" style="color:purple"></i>&nbsp;Criadores
            </div>
            '''

        # Add the legend HTML to the map
        m.get_root().html.add_child(folium.Element(legend_html))  

        # Generate the HTML string for the Folium map
        map_html = m.get_root().render()


        # Display the map using Streamlit
        st.components.v1.html(map_html, height=500)
    
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
                st.write(f"Distancia: {closest_shop['distance']} km")
