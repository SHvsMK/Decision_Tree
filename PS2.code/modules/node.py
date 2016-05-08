# DOCUMENTATION
# =====================================
# Class node attributes:
# ----------------------------
# children - a list of 2 nodes if numeric, and a dictionary (key=attribute value, value=node) if nominal.  
#            For numeric, the 0 index holds examples < the splitting_value, the 
#            index holds examples >= the splitting value
#
# label - is None if there is a decision attribute, and is the output label (0 or 1 for
#	the homework data set) if there are no other attributes
#       to split on or the data is homogenous
#
# decision_attribute - the index of the decision attribute being split on
#
# is_nominal - is the decision attribute nominal
#
# value - Ignore (not used, output class if any goes in label)
#
# splitting_value - if numeric, where to split
#
# name - name of the attribute being split on

class Node:
    def __init__(self):
        # initialize all attributes
        self.label = None
        self.decision_attribute = None
        self.is_nominal = None
        self.value = None
        self.splitting_value = None
        self.children = {}
        self.name = None

    def classify(self, instance):
        '''
        given a single observation, will return the output of the tree
        '''
	# Your code here

        # instance is actually an entry of data_set

        # if the node is leaf node, return the label
        if self.label != None:
            return self.label

        if self.is_nominal:
            if self.children.has_key(instance[self.decision_attribute]):
                return self.children[instance[self.decision_attribute]].classify(instance)
            else:
                # self.value store the mode of a non-leaf node
                return self.value
        else:
            if instance[self.decision_attribute] < self.splitting_value:
                return self.children[0].classify(instance)
            else:
                return self.children[1].classify(instance)

    def print_tree(self, indent = 0):
        '''
        returns a string of the entire tree in human readable form
        IMPLEMENTING THIS FUNCTION IS OPTIONAL
        '''
        # Your code here
        pass


    def print_dnf_tree(self):
        '''
        returns the disjunct normalized form of the tree.
        '''
        return ' v '.join(map(lambda x: ''.join(['(', ' ^ '.join(x), ')']), dfs(self)))

def dfs(node):
    '''
    return None if no leaf node are labeled 1
           Array of arrays of attribute-comparison-value tuples: 
                i.e. [[A=1, B<1.2], [A=2, B>5.2]]
    '''

    if node.label == 1:
        return [[]]
    elif node.label == 0:
        return None

    # store the paths
    paths = []

    # if is nominal
    if node.is_nominal:
        for attr_val, child in node.children.items():
            sub_paths = dfs(child)
            if not sub_paths:
                continue
            for path in sub_paths:
                path.insert(0, ''.join([node.name, '=', str(attr_val)]))
                paths.append(path)
    # if is numeric
    else:
        # left child
        sub_paths = dfs(node.children[0])
        if sub_paths:
            for path in sub_paths:
                # insert the decision attribute and splitting value in the beginning of the path
                path.insert(0, ''.join([node.name, '<', str(node.splitting_value)]))
                paths.append(path)
        # right child
        sub_paths = dfs(node.children[1])
        if sub_paths:
            for path in sub_paths:
                # insert the decision attribute and splitting value in the beginning of the path
                path.insert(0, ''.join([node.name, '>=', str(node.splitting_value)]))
                paths.append(path)

    return paths
