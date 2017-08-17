from TreeInterface import TreeInterface
import csv
import re
from datetime import datetime, timedelta

# Temporary Unit Testing interface
def unit_test():
    t = RealtimeTollmaster(tree_name='LV', root_key='371')

    t.insert_entry('371243', [], 0)
    t.insert_entry('371244', [], 0)
    t.insert_entry('371255', [], 0)
    t.insert_entry('371256', [], 0)
    
    print(t.get_items_by_key('371'), t.get_items_by_key('3712'))
    t.delete_node_by_key('371243')
    print(t.get_items_by_key('371'), t.get_items_by_key('3712'))
    
    nodes = t.inorder_traversal()

    for node in nodes:
        node.update_features()
        node.calculate_score()
        node.print_info()
    
    leaves = t.get_leaves_references()
    for l in leaves:
        print(l.key, l.parent.get_children())

    t.find_suspect_prefixes()

    t.delete_node_by_key('371') # assertion should fail


class RealtimeTollmaster(TreeInterface):
    def __init__(self, tree_name, root_key, 
        feature_descriptions=None,
        aggregate_numerical_features=False):
            
        TreeInterface.__init__(self, tree_name, root_key, feature_descriptions, 
            aggregate_numerical_features)

    # User Defined Scoring Function 
    def score_node(self, node):
        if node.is_leaf():
            node.score = 1.0

        accumulated_score = 0.0

        for child in node.children:
            accumulated_score += child.score

        if len(node.children) is 0:
            node.score = 1.0

        else:
            node.score = accumulated_score / 10 # Should be divided by 10


    # User defined alert threshold / mechanism
    def find_suspect_prefixes(self):
        leaves = self.get_leaves_references()
        for l in leaves:
            self.score_node(l)

        self.propogate()

        nodes = self.inorder_traversal()

        for n in nodes:
            if n.score > 0.2 and not n.is_leaf():
                print(n.key, n.score)


    # Reading Data
    def read_data(self, path):
        with open(path, 'rt') as f:
            csv_reader = csv.reader(f, delimiter=',')
            self.buckets = list()
            first_entry = True
            earliest_time = None

            for idx, row in enumerate(csv_reader):
                if idx == 0:
                    continue

                number = re.sub(r'\W+', '', row[1])
                number = number[0:11] # 11 = Most common Latvia Length

                date = datetime.strptime(row[2], "%d-%m-%Y %H:%M:%S")
                score = int(row[5])

                if first_entry or date > earliest_time + timedelta(minutes=3):
                    earliest_time = date
                    self.buckets.append([])
                    first_entry = False

                self.buckets[-1].append( [number, date, score] )


    # Driver function
    def driver(self):
        self.read_data(path='lvafull.csv')

        for idx, bucket in enumerate(self.buckets):
            if idx == 5: break
            print("For 3 Minute Period Starting From {}".format(
                bucket[0][1].strftime('%y-%m-%d %H:%M:%S')))
            self.clear_tree()
            self.load_data_from_list(data=bucket)
            self.build_tree()
            self.find_suspect_prefixes()


if __name__ == '__main__':
    t = RealtimeTollmaster(tree_name='LV', root_key='371')
    t.driver()

    unit_test()
