# Proyecto final de estructura de datos con Dijkstra y Streamlit

![image](https://github.com/user-attachments/assets/5e71dec6-d948-4172-a085-a2c300242981)

## Descripción general
Este programa gestiona una red geografíca de ubicaciones que están conectadas entre si por medio de nodos en un grafo donde representan una ubicación especifica y las conecciones son las distancias de separación entre si. Permitiendo que el usuario calcule rutas optimas entre dos puntos y que pueda agregar las diferentes paradas intermedias. Permitiendo que sea un programa eficiente para la logística de transporte.

Ademas el programa cuenta con una interfaz visual con Streamlit, que es una herramienta de código abierto que facilita su uso a comparación de Tkinter y Pygame. En este proyecto Streamlit se encarga de mostra la interfaz de forma interactiva, donde el ususario puede seleccionar la ubicación de inicio y final, además tiene la opción de seleccionar diferentes paradas intermedias y ejecutar el algoritmo de Dijikstra para que pueda obtener la ruta que sea mas optima entre las diferentes elecciones que el usuario desee. 

## Manual de Usuario
Después de correr el programa, se mostrará en la interfaz visual el mapa con los puntos de ubicación predeterminados. El usuario tendrá que escoger el punto de origen y destino para que el programa le dé la ruta más corta. Adicionalmente, tiene la opción de agregar las paradas intermedias que desee. Luego deberá hacer clic en la opción de “Buscar ruta más corta” para que el programa realice los cálculos y le muestre al usuario la ruta más óptima.

En el mapa se resaltarán los puntos con los siguientes colores:

Verde: punto de inicio

Naranja: paradas intermedias

Vinotinto: destino

Rojo: conexiones entre los puntos


### Enlaces de interés
* https://streamlit.io/
