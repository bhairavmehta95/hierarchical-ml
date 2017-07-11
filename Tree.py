import pygtrie
import re
from Node import Node


class Tree:
    def __init__(self, country_iso, country_code):
        self.country_iso = country_iso
        self.country_code = country_code
        self.tree = pygtrie.CharTrie()

        # Construct node with country code as root
        root = Node(country_code, is_root=True)
        self.insert_node(root)


    def create_node(self, key, parent):
        if self.tree.has_key(unicode(key)):
            return self.tree[unicode(key)]

        n = Node(key)
        n.parent = parent
        n.parent.children += 1
        self.insert_node(n)

        return self.tree[unicode(key)]


    def insert_node(self, node):
        if self.tree.has_key(unicode(node.key)):
            return

        self.tree[unicode(node.key)] = node


    def get_node(self, key):
        if self.tree.has_key(unicode(key)):
            return self.tree[unicode(key)]
        else:
            return None


    def delete_node_by_key(self, key, recursive=True):
        assert key is not self.country_code # Can't delete root

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


    def insert_phone_number(self, number):
        assert number.find(self.country_code) is not -1

        # remove all nonalphanum. chars from number
        number = re.sub(r'\W+', '', number)

        idx_end = number.find(self.country_code) + len(self.country_code) + 1
        
        parent = self.tree[unicode(self.country_code)]
        
        while idx_end <= len(number):
            key = number[0:idx_end]
            new = self.create_node(key, parent=parent)
            parent = new
            idx_end += 1


    def delete_phone_number(self, number):
        idx_end = len(number)

        while idx_end > len(self.country_code):
            key = number[0:idx_end]
            
            if not self.tree.has_key(unicode(key)):
                return 

            parent = self.tree[unicode(key)].parent
            self.delete_node_by_key(key, recursive=False)
            parent.children -= 1

            if parent.children != 0:
                return

            idx_end -= 1


    def get_items_nodes(self, key):
        try:
            items = self.tree.items(key)
        except:
            items = []

        return [item[1] for item in items]


    def get_items(self, key):
        try:
            items = self.tree.items(key)
        except:
            items = []

        return items


    def inorder_traversal(self):
        return self.get_items_nodes(self.country_code)


    def serialize_tree(self):
        nodes = self.get_items_nodes(self.country_code)
        for n in nodes:
            


if __name__ == '__main__':
    t = Tree('LV', '371')

    t.insert_phone_number('371243')
    t.insert_phone_number('371244')
    t.insert_phone_number('371255')
    t.insert_phone_number('371256')
    
    print(t.get_items('371'), t.get_items('3712'))
    t.delete_node_by_key('371243')
    print(t.get_items('371'), t.get_items('3712'))
    
    nodes = t.inorder_traversal()

    for node in nodes:
        node.update_features()
        node.calculate_score()
        node.print_info()
    

    t.delete_node_by_key('371') # assertion should fail

