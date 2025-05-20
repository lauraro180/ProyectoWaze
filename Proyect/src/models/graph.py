from typing import Dict, List
from src.models.node import Node

class Graph:
    def __init__(self):
        self.nodes: Dict[str, Node] = {}

    def add_node(self, node: Node):
        if node.id in self.nodes:
            raise ValueError(f"Node with ID {node.id} already exists")
        
        self.nodes[node.id] = node

    def remove_node(self, node_id: str):
        if node_id not in self.nodes:
            raise ValueError(f"Node with ID {node_id} not found")
        
        del self.nodes[node_id]

    def get_node(self, node_id: str) -> Node:
        if node_id not in self.nodes:
            raise ValueError(f"Node with ID {node_id} not found")
        
        return self.nodes[node_id]

    def connect_nodes(self, node1_id: str, node2_id: str, distance: float):
        if node1_id not in self.nodes or node2_id not in self.nodes:
            raise ValueError("Both nodes must exist in the graph")
        
        node1 = self.nodes[node1_id]
        node2 = self.nodes[node2_id]
        
        node1.add_connection(node2, distance)
        node2.add_connection(node1, distance)

    def get_all_nodes(self) -> List[Node]:
        return list(self.nodes.values())

    def node_count(self) -> int:
        return len(self.nodes)
    
    def dijkstra(self, node1_id, node2_id):
        distances = {}
        for node_id in self.nodes:
            distances[node_id] = float("infinity")
        distances[node1_id] = 0
        
        previous = {}
        unvisited = list(self.nodes.keys())
        
        while unvisited:
            current = None
            min_distance = float("infinity")
            for i in unvisited:
                if distances[i] < min_distance:
                    min_distance = distances[i]
                    current = i
            
            if current == node2_id:
                break
                
            unvisited.remove(current)
            
            current_node = self.nodes[current]
            connections = current_node.get_connections()
            for neighbor_id, connection_data in connections.items():
                distance = connection_data["distance"]
                new_distance = distances[current] + distance
                if new_distance < distances[neighbor_id]:
                    distances[neighbor_id] = new_distance
                    previous[neighbor_id] = current
        
        camino_optimo = []
        current = node2_id
        
        if node2_id not in previous and node2_id != node1_id:
            return None, float("infinity")
            
        while current != node1_id:
            camino_optimo.append(current)
            if current not in previous:
                return None, float("infinity")
            current = previous[current]
            
        camino_optimo.append(node1_id)
        camino_optimo.reverse()
        
        return camino_optimo, distances[node2_id]
    
    def build_path_through_waypoints(self, origin_id, destination_id, waypoints):
        if not waypoints:
            return self.dijkstra(origin_id, destination_id)
        
        # Eliminar waypoints que no están en el grafo
        valid_waypoints = [wp for wp in waypoints if wp in self.nodes]
        
        if not valid_waypoints:
            return None, float("infinity")
        
        # Encontrar el camino más corto entre el origen y el primer waypoint
        camino_optimo, distancia_total = self.dijkstra(origin_id, valid_waypoints[0])
        
        if camino_optimo is None:
            return None, float("infinity")
        
        # Recorrer los waypoints intermedios
        for i in range(len(valid_waypoints) - 1):
            camino_parcial, distancia_parcial = self.dijkstra(valid_waypoints[i], valid_waypoints[i + 1])
            
            if camino_parcial is None:
                return None, float("infinity")
            
            # Eliminar el primer nodo del camino parcial (ya está en el camino óptimo)
            camino_parcial.pop(0)
            camino_optimo += camino_parcial
            distancia_total += distancia_parcial
        
        # Agregar el destino al final del camino óptimo
        if valid_waypoints[-1] != destination_id:
            camino_final, distancia_final = self.dijkstra(valid_waypoints[-1], destination_id)
            
            if camino_final is None:
                return None, float("infinity")
            
            # Eliminar el primer nodo del camino final (ya está en el camino óptimo)
            camino_final.pop(0)
            camino_optimo += camino_final
            distancia_total += distancia_final
        
        return camino_optimo, distancia_total
    
    def dijkstra_with_waypoints(self, origin_id, destination_id, waypoints=None):
        if not waypoints:
            path, distance = self.dijkstra(origin_id, destination_id)
            return path, distance, []
        
        if len(waypoints) <= 3:  # Reducimos el límite de 4 a 3 para evitar demasiadas permutaciones
            # Para pocos waypoints, usar fuerza bruta para encontrar el orden óptimo
            import itertools
            
            best_distance = float("infinity")
            best_path = None
            best_order = None
            
            # Probar todas las permutaciones posibles de waypoints
            for perm in itertools.permutations(waypoints):
                path, distance = self.build_path_through_waypoints(origin_id, destination_id, list(perm))
                
                if path is not None and distance < best_distance:
                    best_distance = distance
                    best_path = path
                    best_order = list(perm)
            
            return best_path, best_distance, best_order
        else:
            # Para muchos waypoints, usar algoritmo voraz del vecino más cercano
            remaining = set(waypoints)
            ordered_waypoints = []
            current = origin_id
            
            # Construir ruta por vecino más cercano
            while remaining:
                best_next = None
                best_distance = float("infinity")
                
                for waypoint in remaining:
                    path, distance = self.dijkstra(current, waypoint)
                    if path is not None and distance < best_distance:
                        best_distance = distance
                        best_next = waypoint
                if best_next is None:
                    # No se encontró un camino válido
                    return None, float("infinity"), None
                
                ordered_waypoints.append(best_next)
                current = best_next
                remaining.remove(best_next)
            
            # Calcular la ruta final con el orden optimizado
            final_path, final_distance = self.build_path_through_waypoints(
                origin_id, destination_id, ordered_waypoints)
            
            return final_path, final_distance, ordered_waypoints
