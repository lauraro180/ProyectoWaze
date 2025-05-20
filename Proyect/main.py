import streamlit as st
import folium
from streamlit_folium import folium_static
from src.models.node import Node
from src.models.graph import Graph

def create_bogota_network():
    bogota_graph = Graph()

    # Define 5 key locations in Bogotá with their coordinates
    locations = [
        ("La Candelaria", 4.59659835363888, -74.07293427567559),
        ("Colegio Anglo Americano", 4.749018394993704, -74.02816728851406),
        ("Centro Comercial Colina", 4.7327708833535524, -74.06665016589406),
        ("Movistar Arena", 4.649472865968035, -74.07724590451186),
        ("Plaza Mayor (Chía)", 4.865646518255673, -74.0398853891656),
        ("Parque Simón Bolívar", 4.6581051106732305, -74.09357618851733),
        ("Centro Comercial Unicentro", 4.7042968130947616, -74.0413798306461),
        ("Aereopuerto Guaymaral", 4.812816468415563, -74.06361800878007)
    ]


    # Create and add nodes to the graph
    nodes = []
    for name, lat, lon in locations:
        node = Node(name, lat, lon)
        bogota_graph.add_node(node)
        nodes.append(node)

    # Connect nodes (you can adjust distances as needed)
    for i in range(len(nodes)):
        for j in range(i+1, len(nodes)):
            # Calculate a sample distance (in km)
            # You might want to replace this with actual distances
            distance = ((nodes[i].latitude - nodes[j].latitude)**2 + 
                        (nodes[i].longitude - nodes[j].longitude)**2)**0.5 * 111
            bogota_graph.connect_nodes(nodes[i].id, nodes[j].id, distance)

    return bogota_graph

def show_shortest_path(graph, map_obj):
    # Obtener todos los nodos para crear las opciones de selección
    all_nodes = graph.get_all_nodes()
    node_names = [node.name for node in all_nodes]
    node_dict = {node.name: node.id for node in all_nodes}
    
    # Crear selectores para origen y destino
    st.subheader("1. Selecciona el origen y destino")
    col1, col2 = st.columns(2)
    with col1:
        origen = st.selectbox("Origen:", node_names, key="origen")
    with col2:
        destino = st.selectbox("Destino:", node_names, key="destino")
    
    # Selector para puntos intermedios obligatorios    st.subheader("2. Selecciona puntos intermedios (opcional)")
    waypoint_options = [name for name in node_names if name != origen and name != destino]
    selected_waypoints = st.multiselect("Paradas intermedias:", waypoint_options)
    
    # Obtener los IDs de los nodos intermedios seleccionados
    waypoints = [node_dict[name] for name in selected_waypoints]
    
    # Botón para calcular la ruta
    if st.button("Buscar ruta más corta", type="primary"):
        origen_id = node_dict[origen]
        destino_id = node_dict[destino]
          # Ejecutar el algoritmo con waypoints optimizados
        path, distance, ordered_waypoints = graph.dijkstra_with_waypoints(origen_id, destino_id, waypoints)
        if path is None:
            st.error(f"No existe una ruta entre {origen} y {destino} pasando por todos los puntos seleccionados.")
        else:
            st.markdown("---")
            st.header("Resultados")
            
            # Crear un nuevo mapa para mostrar la ruta
            route_map = folium.Map(location=[4.7310, -74.0721], zoom_start=11)
              # Añadir todos los nodos y conexiones al mapa
            for node in graph.get_all_nodes():
                # Determinar el color y tipo de ícono según el tipo de nodo
                icon_color = 'blue'
                icon_type = 'info-sign'
                
                if node.id == origen_id:
                    icon_color = 'green'
                    icon_type = 'play'
                elif node.id == destino_id:
                    icon_color = 'darkred'
                    icon_type = 'flag'
                elif node.id in ordered_waypoints:
                    # Mostrar número de orden en waypoints
                    wp_index = ordered_waypoints.index(node.id) + 1
                    icon_color = 'orange'
                    icon_type = 'screenshot'
                
                folium.Marker(
                    location=[node.latitude, node.longitude],
                    popup=node.name,
                    tooltip=node.name,
                    icon=folium.Icon(color=icon_color, icon=icon_type)
                ).add_to(route_map)
            
            # Destacar los nodos en la ruta
            route_nodes = [graph.get_node(node_id) for node_id in path]
            
            # Dibujar la ruta como una línea roja más gruesa
            route_points = [[node.latitude, node.longitude] for node in route_nodes]
            folium.PolyLine(
                locations=route_points,
                color='red',
                weight=5,
                opacity=0.7,
                tooltip=f"Distancia: {distance:.2f} km"
            ).add_to(route_map)            # Mostrar el mapa con la ruta
            st.success(f"Ruta encontrada: Distancia total: {distance:.2f} km")
            folium_static(route_map)
            
            # Marcar que se ha calculado una ruta
            st.session_state.route_calculated = True

            
            # Botón para reiniciar y ver el mapa general
            if st.button("Reiniciar planificador", key="reset"):
                st.session_state.route_calculated = False
                st.experimental_rerun()

def create_bogota_map(graph):
    """
    Create a Folium map of Bogotá with nodes and connections
    """
    # Center the map on Bogotá
    m = folium.Map(location=[4.7310, -74.0721], zoom_start=11)

    # Add nodes to the map
    for node in graph.get_all_nodes():
        # Create a marker for each node
        folium.Marker(
            location=[node.latitude, node.longitude],
            popup=node.name,
            tooltip=node.name,
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(m)

        # Add connections
        for conn_id, conn_info in node.get_connections().items():
            connected_node = conn_info['node']
            # Draw lines between connected nodes
            folium.PolyLine(
                locations=[
                    [node.latitude, node.longitude],
                    [connected_node.latitude, connected_node.longitude]
                ],
                color='blue',
                weight=2,
                opacity=0.5
            ).add_to(m)

    return m  # Corregido: return fuera del bucle for

def main():
    st.title("Bogotá Logistics Network")

    # Inicializar variable de sesión si no existe
    if 'route_calculated' not in st.session_state:
        st.session_state.route_calculated = False

    # Create the graph
    bogota_graph = create_bogota_network()
    
    # Añadir la función para mostrar la ruta más corta primero
    show_shortest_path(bogota_graph, None)
    
    # Mostrar el mapa base solo si no se ha calculado una ruta
    if not st.session_state.route_calculated:
        st.subheader("Mapa de la red de Bogotá")
        bogota_map = create_bogota_map(bogota_graph)
        folium_static(bogota_map)

if __name__ == "__main__":
    main()
