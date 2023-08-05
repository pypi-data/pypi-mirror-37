from .core import InputNode
from ..utils.generic import isinstance_str


class Input(InputNode):
    pass


class FeatureSet:
    """Wrapper for set of Nodes that when fed to Transformations map to all given Nodes.

    Parameters
    ----------
    nodes : list of megatron.Node or str
        nodes to group together, or names of nodes to create, then group together.
        if strs provided, shape of each is assumed to be a single column.

    Attributes
    ----------
    nodes : list of megatron.Node
        nodes to group together.
    names : list of str
        names of each given Node.
    name_to_index : dict of str to int
        utility data structure for quick indexing of names.
    """
    def __init__(self, nodes):
        self.nodes = nodes
        self.names = [node.name for node in self.nodes]
        self.name_to_index = {name: i for i, name in enumerate(self.names)}

    def apply_layer(self, layer):
        new_nodes = [node.apply_layer(layer) for node in self.nodes]
        return FeatureSet(new_nodes, self.names)

    def get(self, key):
        if isinstance(key, str):
            return self.nodes[self.name_to_index[key]]
        else:
            raise KeyError("Invalid key type; must be str")

    def __getitem__(self, key):
        if isinstance(key, list):
            return [self.get(k) for k in key]
        else:
            return self.get(key)

    def set(self, key, node):
        if isinstance(key, str):
            self.nodes[self.name_to_index[key]] = node
        else:
            raise KeyError("Invalid key type; must be str")

    def __setitem__(self, key, node):
        self.set(key, node)
