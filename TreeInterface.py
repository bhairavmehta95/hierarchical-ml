from Tree import Tree
import Queue

class TreeInterface(Tree):
    def __init__(self, tree_name, root_key, 
        feature_descriptions=None,
        aggregate_numerical_features=False):
            
        Tree.__init__(self, tree_name, root_key, feature_descriptions, 
            aggregate_numerical_features)

        self.queue = Queue.Queue()
    

    def propogate(self):
        leaves = self.get_leaves_references()
        for leaf in leaves:
            if not leaf.parent.visited:
                self.queue.put(leaf.parent)
                leaf.parent.visited = True

        while not self.queue.empty():
            n = self.queue.get()
            self.score_node(n)

            if n.parent and n.score is not 0 and not n.parent.visited:
                self.queue.put(n.parent)
                n.parent.visited = True


    def score_node(self, node):
        raise NotImplementedError("All TreeInterface Classes should implement this!")