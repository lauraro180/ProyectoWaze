import uuid

class Node:
    def __init__(self, name, latitude, longitude):
        # Generate unique identifier
        self.id = str(uuid.uuid4())
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        
        # Optional: Connections to other nodes
        self.connections = {}

    def add_connection(self, target_node, distance):
        """
        Add a connection to another node with a distance
        """
        if not isinstance(target_node, Node):
            raise TypeError("Connection must be to another Node")
        
        if distance < 0:
            raise ValueError("Distance cannot be negative")
        
        self.connections[target_node.id] = {
            'node': target_node,
            'distance': distance
        }

    def get_connections(self):
        return self.connections

    def __repr__(self):
        return f"Node: {self.name} (ID: {self.id}, Lat: {self.latitude}, Lon: {self.longitude})"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'latitude': self.latitude,
            'longitude': self.longitude
        }
