import redis
from redisgraph import Node, Edge, Graph

class KnowledgeGraph:
    ''' Encapsulates a knowledge graph. '''
    def __init__(self, graph, graph_name, host='localhost', port=6379):
        ''' Connect to Redis. '''
        self.redis = redis.Redis(host=host, port=port)
        self.graph = Graph(graph_name, self.redis)
    def add_node (self, props, label=None, commit=True):
        ''' Add a node to the graph. '''
        n = Node(label=label, properties=props)
        self.graph.add_node (n)
        if commit:
            self.graph.commit ()
    def add_edge (self, subj, pred, obj, props, commit=True):
        ''' Add an edge. '''
        e = Edge(subj, pred, obj, properties=props)
        self.graph.add_edge (e)
        if commit:
            self.graph.commit ()
    def commit (self):
        ''' Commit changes. '''
        self.graph.commit ()
    def query (self, query):
        ''' Query the graph. '''
        return self.graph.query (query)
    def delete (self):
        ''' Delete the entire graph. '''
        self.graph.delete ()
