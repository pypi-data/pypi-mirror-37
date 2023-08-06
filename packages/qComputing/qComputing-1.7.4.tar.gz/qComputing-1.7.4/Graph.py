
class Vertex(object):
    """
    This class represents what is contained at a vertex on a graph either a class label with a class state i.e 0 or 1
    or a quantum label with a quantum state
    """
    def __init__(self,state,label):
        """
        :param state: This is the actual state 0 or 1 for the classical case or density matrix for quantum case
        :param label: This is just the label for the vertex
        """
        self.graph_state= state
        self.node =label
        self.adjacent = {}

    def add_neighbor(self,neighbor,weight):
        """
        :param neighbor:  This is the keyword for the adjacent dictionary. This is a vertex object
        :param weight: This is a value for a specific key. Contains weights for the edges connected to the vertex
        :return:
        """
        self.adjacent[neighbor] = weight

    def __str__(self):
        stringvar ={'label':self.node, 'state':self.graph_state, 'adjacent':self.adjacent.values(),'Neighbors':[x.node for x in self.adjacent]}
        return 'Label: {label} \n State: {state} \n Adjacent Weights: {adjacent} \n Neighbors: {Neighbors} '.format(**stringvar)

    def get_weight(self,neighbor):
        """
        :param neighbor: this is the keyword and is the memory lab provided by python not the label assigned by user
        :return: returns the weight for a specific neighbor
        """
        return self.adjacent[neighbor]

    def get_connections(self):
        return self.adjacent.keys()

    def get_id(self):
        return self.node



class Graph(object):
    """
    This defines a graph object with dictionary of vertex objects. The keys are the labels and values are the vertex
    objects
    """

    def __init__(self):
        """
        This is the dictionary of vertex objects
        """
        self.vertices ={}

    def __iter__(self):
        """
        :return:  Makes vertex objects iterables. So one should be able to use for loops on them
        """
        return iter(self.vertices)

    def add_vertex(self,state,label):
        """
        :param state: The actual state to be held at the vertex could be classical values or quantum mechanical states
        :param label: The label for the state. Could be a classical label or a quantum mechanical label
        :return:  returns a vertex object
        """
        new_vertex = Vertex(state,label)
        self.vertices[label] = new_vertex
        return new_vertex

    def add_edge(self,first,firststate,second,secondstate,weight):
        """
        This creates an edge from one 'from' vertex to a 'to' vertex
        :param first: Label for the 'from ' state
        :param firststate: Actual state of the 'from' state
        :param second:  Label for the 'to' state
        :param secondstate: Actual state of the 'to' state
        :param weight: The weight to be used for this edge
        """
        if first not in self.vertices:
            self.add_vertex(first,firststate)
        if second not in self.vertices:
            self.add_vertex(second,secondstate)

        self.vertices[first].add_neighbor(self.vertices[second],weight)
        self.vertices[second].add_neighbor(self.vertices[first],weight)

if __name__ == '__main__':
    g = Graph()

    g.add_vertex(0,'q1')
    g.add_vertex(0,'q2')
    g.add_vertex(1,'q3')

    g.add_edge('q1',0,'q2',0,0.8)
    g.add_edge('q1',0,'q3',1,0.5)

    print(g.vertices['q1'])
    print(g.vertices['q1'].adjacent[g.vertices['q2']])
    print(g.vertices['q1'].adjacent[g.vertices['q3']])
    print(g.vertices['q2'])


