# Final-Project-IronHack-23
Development of the final project as part of the IronHack Data Analysis course in Madrid, April 2023

Desarrollo de la aplicación de recomendación de mascotas "HelPets".

El objetivo de la misma es la creación de un método para recomendar mascotas en base a una serie de filtros y decisiones puestas por el usuario, y proporcionar las tiendas más cercanas divididas en 4 categorías (Protectoras de animales, Veterinarios, Tiendas de Mascotas y Criadores).

**1) Obtención y limpiado de datos
**2) Assembly of geocode via the Googlemaps API
**3) Visualization on Tableau
**4) Assembly on Streamlit

1) Usando como base las bibliotecas de razas de perros y gatos de las empresas de pienso animal Royal Canin y Purina, y mediante BeautifulSoup, se obtuvieron 5 tablas por parte de los perros (XS, S, M, L, XL) y 4 de gatos. Purina presentaba también una base de datos de perros, pero la información proporcionada no era igual de informativa. 

El proceso de limpiado de cada una de las tablas incluía la sustitución de caracteres innecesarios, separación del texto apropiada, creación de múltiples columnas, y obtención de url de las fotos de cada raza.

En el caso de los perros, se creó e integró un dataframe independiente para detectar si una raza concreta era hipoalergénica.

Cada una de las tablas se usó para crear sendas tabla grupales, una para perros y otras para gatps (Archivos DogAssembly.ipynb y CatAssembly.ipynb)

Antes de la integración en csv, se rellenaron todas las celdas vacía y se eliminaron los valores NaN, creado los archivos TablaPerra.csv and tablaGatuna.csv. El archivo de perros, sin embargo, presenta vacío en columnas, dado que debido a los diferentes valores presentes en las tablas originales de la base de datos; nuevas categorías tuvieron que ser creadas aglutinando diferentes strings.

2) Para desarrollar un código que permitiera introducir una dirección y mostrar
