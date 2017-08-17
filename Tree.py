import pygtrie
import re
import csv
import logging

from Node import Node


class Tree:
    def __init__(self, 
        tree_name, root_key, 
        feature_descriptions=None,
        aggregate_numerical_features=False):

        self.tree_name = tree_name
        self.root_key = root_key
        self.tree = pygtrie.CharTrie()
        self.aggregate_numerical_features = aggregate_numerical_features

        self.data = list()

        # Construct root node
        root = Node(root_key, is_root=True)
        self.insert_node(root)

    
    def create_node(self, key, features, score, parent):
        if self.tree.has_key(unicode(key)):
            return self.tree[unicode(key)]

        n = Node(key, feature_vector=features)
        n.parent = parent
        parent.children.append(n)
        n.parent.num_children += 1
        self.insert_node(n)

        return self.tree[unicode(key)]


    def insert_node(self, node):
        if self.tree.has_key(unicode(node.key)):
            return

        self.tree[unicode(node.key)] = node


    def get_node_by_key(self, key):
        if self.tree.has_key(unicode(key)):
            return self.tree[unicode(key)]
        else:
            logging.warn("No node with key: {} in tree.".format(key))
            return None


    def delete_node_by_key(self, key, recursive=True):
        try:
            assert key is not self.root_key # Can't delete root
        except AssertionError:
            logging.error("Cannot delete root.")
            exit(1)

        if not self.tree.has_key(key):
            return

        if recursive:
            keys = self.tree.keys(prefix=unicode(key))
            for k in keys:
                try:
                    self.tree.pop(unicode(k))
                except:
                    pass
        else:
            try:
                self.tree.pop(unicode(key))
            except:
                pass


    def get_items_by_key_references(self, key):
        try:
            items = self.tree.items(key)
        except:
            items = list()

        return [item[1] for item in items]


    def get_items_by_key(self, key):
        try:
            items = self.tree.items(key)
        except:
            items = list()

        return [item[0] for item in items]


    def insert_entry(self, key, features, score):
        assert key.find(self.root_key) is not -1

        # remove all nonalphanum. chars from key
        key = re.sub(r'\W+', '', key)

        idx_end = key.find(self.root_key) + len(self.root_key) + 1
        
        parent = self.tree[unicode(self.root_key)]
        
        while idx_end <= len(key):
            prefix = key[0:idx_end]

            new_node = self.create_node(prefix, features, score, parent)
            parent = new_node
            idx_end += 1


    def delete_entry(self, key):
        idx_end = len(key)

        while idx_end > len(self.root_key):
            key = key[0:idx_end]
            
            if not self.tree.has_key(unicode(key)):
                return 

            parent = self.tree[unicode(key)].parent
            parent.num_children -= 1
            parent.children.remove(self.tree[unicode(key)])

            self.delete_node_by_key(key, recursive=False)

            if parent.num_children != 0:
                return

            idx_end -= 1


    def inorder_traversal(self):
        return self.get_items_by_key_references(self.root_key)


    # TODO: List expressions vs Readability?
    def get_leaves_references(self):
        nodes = self.get_items_by_key_references(self.root_key)
        leaves = list()

        for n in nodes:
            if n.is_leaf():
                leaves.append(n)

        return leaves


    def serialize_tree(self):
        nodes = self.get_items_by_key_references(self.root_key)
        for n in nodes:
            pass #TODO 


    def load_data_from_csv(self, path, key_column, feature_columns=list(), score_column=None):
        with open(path, 'r') as file:
            csv_reader = csv.DictReader(file)
            self.key_column = key_column
            self.feature_columns = feature_columns

            for row in csv_reader:
                try:
                    entry = [ row[key_column] ]
                    entry += [ row[f] for f in feature_columns ]

                    if score_column:
                        entry.append(row[score_column])
                    else:
                        entry.append(0.0)

                    self.data.append(entry)

                except KeyError:
                    logging.error("Please check your column names.")
                    exit(1)


    def load_data_from_list(self, data):
        self.data = data


    def build_tree(self):
        for entry in self.data:
            key = None 
            features = None 
            score = None
            key = entry[0]
            score = entry[-1]

            if len(entry) == 2:
                features = None
            else:
                features = entry[1:len(entry)-2]
            
            self.insert_entry(key, features, score)


    def clear_tree(self):
        victims = self.inorder_traversal()
        for v in victims:
            if v.is_root:
                continue

            self.delete_node_by_key(v.key)

