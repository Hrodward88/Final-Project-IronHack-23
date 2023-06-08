# Final-Project-IronHack-23
Development of the final project as part of the IronHack Data Analysis course in Madrid, April 2023

Desarrollo de la aplicación de recomendación de mascotas "HelPets".

El objetivo de la misma es la creación de un método para recomendar mascotas en base a una serie de filtros y decisiones puestas por el usuario, y proporcionar las tiendas más cercanas divididas en 4 categorías (Protectoras de animales, Veterinarios, Tiendas de Mascotas y Criadores).

**1) Obtención y limpiado de datos
**2) Assembly of geocode via the Googlemaps API
**3) Visualization on Tableau
**4) Assembly on Streamlit
**5) Mejoras

1) Usando como base las bibliotecas de razas de perros y gatos de las empresas de pienso animal Royal Canin y Purina, y mediante BeautifulSoup, se obtuvieron 5 tablas por parte de los perros (XS, S, M, L, XL) y 4 de gatos. Purina presentaba también una base de datos de perros, pero la información proporcionada no era igual de informativa. 
![Screenshot 2023-06-08 at 21 00 04](https://github.com/Hrodward88/Final-Project-IronHack-23/assets/129097999/3e5e3c71-a90f-41f4-8fb7-a2e5539f9e07)

El proceso de limpiado de cada una de las tablas incluía la sustitución de caracteres innecesarios, separación del texto apropiada, creación de múltiples columnas, y obtención de url de las fotos de cada raza.
![Screenshot 2023-06-08 at 21 00 18](https://github.com/Hrodward88/Final-Project-IronHack-23/assets/129097999/cc4b7604-19ea-4f68-9011-977d34a0a598)

En el caso de los perros, se creó e integró un dataframe independiente para detectar si una raza concreta era hipoalergénica.

Cada una de las tablas se usó para crear sendas tabla grupales, una para perros y otras para gatps (Archivos DogAssembly.ipynb y CatAssembly.ipynb)

Antes de la integración en csv, se rellenaron todas las celdas vacía y se eliminaron los valores NaN, creado los archivos TablaPerra.csv and tablaGatuna.csv. El archivo de perros, sin embargo, presenta vacío en columnas, dado que debido a los diferentes valores presentes en las tablas originales de la base de datos; nuevas categorías tuvieron que ser creadas aglutinando diferentes strings.
![Screenshot 2023-06-08 at 20 59 39](https://github.com/Hrodward88/Final-Project-IronHack-23/assets/129097999/8e288d09-af53-45d9-b9cb-1e409b30a024)
![Screenshot 2023-06-08 at 21 01 07](https://github.com/Hrodward88/Final-Project-IronHack-23/assets/129097999/0ec2f642-5cae-4db6-89f1-aaa032bb7728)

2) Para desarrollar un código que permitiera introducir una dirección y mostrar las tiendas más cercanas, usamos la API de Google, dándole accesso a geocode y places, mediante la API_KEY creada expresamente para este proyecto.
![Screenshot 2023-06-08 at 21 43 06](https://github.com/Hrodward88/Final-Project-IronHack-23/assets/129097999/6f2812c1-ef70-45aa-b273-e1553d7a9a77)

Con ello, se consiguió crear una sección para un input por parte del usuario, y distintos radios para cada uno de los 4 grupos de tiendas, introducidos por separado. Se incluyó además un mensaje para evitar que el radio fuese 0 m.
![Screenshot 2023-06-08 at 21 43 22](https://github.com/Hrodward88/Final-Project-IronHack-23/assets/129097999/25c6e18f-6c11-462d-b4e8-833145f812e3)

Se inclutó también al final del código la lista incluyendo la tienda más cercana de cada grupo.

![Screenshot 2023-06-08 at 21 43 41](https://github.com/Hrodward88/Final-Project-IronHack-23/assets/129097999/93f4277d-4105-42fd-95cf-048f93d5ae1e)

3) Visualización en Tableau

Usando Tableau Public, se crean algunos gráficos que permitan visualizar mejor algunos de los datos. Para ello, se crearon diversos campos calculados que permitiesen contar el numero de razas por categorías como país, alergia y tamaños.

<img width="461" alt="Catcountries" src="https://github.com/Hrodward88/Final-Project-IronHack-23/assets/129097999/56ee6625-d876-42ab-a47a-57401a5c6f71">
<img width="703" alt="Dogsizes" src="https://github.com/Hrodward88/Final-Project-IronHack-23/assets/129097999/ae181a33-7738-4127-ae4b-132302f54f59">


4) Finalmente, todos estos elementos en conjunto permitieron establecer una aplicación web básica en Streamlit, incluyendo selección de la base de datos a usar, con sus filtros correspondientes, presentación de imágenes individuales e información de cada raza concreta tras la selección.

Finalmente, mediante una integración con google maps, tenemos disponible un mapa interactivo donde el usuario puede introducir un input y los diferentes elementos aparecen en listas desplegables, además de en una lista extra mostrando los elementos más cercanos de cada grupo.

![Screenshot 2023-06-08 at 22 11 14](https://github.com/Hrodward88/Final-Project-IronHack-23/assets/129097999/e9b5f8bd-d59c-4b9f-86d2-84140204f754)

![Screenshot 2023-06-08 at 22 11 32](https://github.com/Hrodward88/Final-Project-IronHack-23/assets/129097999/6dbe24a7-b3da-4c29-a4a6-2541603408fd)

![Screenshot 2023-06-08 at 22 12 19](https://github.com/Hrodward88/Final-Project-IronHack-23/assets/129097999/e7451dab-5952-41dc-b4e2-0f8153b9d7a8)

5) El proyecto tiene amplio margen de mejora, con la inclusión de mayor tipo de variedad de animales, mejores filtros, y la vuelta al plan original, en el cuál la aplicación de los filtros presenta al usuario con recomendaciones adecuadas a sus necesidades, sin necesidad de hacer una primera selección por especie.

