import streamlit as st
import pandas as pd
import requests
from PIL import Image
import io

st.title('Bienvenido al recomendador de mascotas')

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
    image_table = []

    # Download and add images of remaining breeds to the table
    for index, row in filtered_data.iterrows():
        image_url = row['Foto']
        image = download_image(image_url)
        if image is not None:
            # Resize the image to a smaller size
            image.thumbnail((200, 200))
            image_table.append((image, row['Raza']))

    # Display the table of images and breed names
    num_images = len(image_table)
    num_cols = 4  # Number of columns in the table
    num_rows = (num_images + num_cols - 1) // num_cols  # Calculate the number of rows based on the number of images
    for i in range(num_rows):
        cols = st.columns(num_cols)
        for j in range(num_cols):
            index = i * num_cols + j
            if index < num_images:
                cols[j].image(image_table[index][0], use_column_width=True)
                cols[j].write(image_table[index][1])

elif selection == "Gatos":
    st.dataframe(gatos_data)
    st.write('# Aquí tienes algunos filtros básicos que ayudarán a sugerir tu mascota ideal')
    # Define columns to be shown initially
    initial_catcolumns = ['Maullido', 'Sociabilidad', 'Alergia', 'Niños']

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
    image_table = []

    # Download and add images of remaining breeds to the table
    for index, row in filtered_data.iterrows():
        image_url = row['Foto']
        image = download_image(image_url)
        if image is not None:
            # Resize the image to a smaller size
            image.thumbnail((200, 200))
            image_table.append((image, row['Raza']))

    # Display the table of images and breed names
    num_images = len(image_table)
    num_cols = 4  # Number of columns in the table
    num_rows = (num_images + num_cols - 1) // num_cols  # Calculate the number of rows based on the number of images
    for i in range(num_rows):
        cols = st.columns(num_cols)
        for j in range(num_cols):
            index = i * num_cols + j
            if index < num_images:
                cols[j].image(image_table[index][0], use_column_width=True)
                cols[j].write(image_table[index][1])
