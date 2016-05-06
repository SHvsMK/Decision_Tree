import math
from node import Node
import sys

def ID3(data_set, attribute_metadata, numerical_splits_count, depth):
    '''
    See Textbook for algorithm.
    Make sure to handle unknown values, some suggested approaches were
    given in lecture.
    ========================================================================================================
    Input:  A data_set, attribute_metadata, maximum number of splits to consider for numerical attributes,
	maximum depth to search to (depth = 0 indicates that this node should output a label)
    ========================================================================================================
    Output: The node representing the decision tree learned over the given data set
    ========================================================================================================

    '''
    # Your code here

    # decision tree to be returned
    node = Node()

    # base case
    theta = 0.0 # threshold of entropy
    if not data_set:
        return node
    elif depth == 0:
        node.label = mode(data_set)
        return node
    elif check_homogenous(data_set):
        node.label = data_set[0][0]
        return node
    # no attributes to split
    elif numerical_splits_count[1:] == [0] * (len(numerical_splits_count) - 1):
        node.label = mode(data_set)
        return node
    elif entropy(data_set) == theta:
        node.label = mode(data_set)
        return node

    # split on best attribute
    splitting_attr, splitting_value = pick_best_attribute(data_set, attribute_metadata, numerical_splits_count)

    # avoid pass by reference error
    numerical_splits_count = list(numerical_splits_count)
    numerical_splits_count[splitting_attr] -= 1

    # describe the node
    node.decision_attribute = splitting_attr
    node.is_nominal = attribute_metadata[splitting_attr]['is_nominal']
    node.splitting_value = splitting_value
    node.name = attribute_metadata[splitting_attr]['name']

    # if is nominal
    if node.is_nominal:
        # put data in data_set into different branches
        branches = {}
        for data in data_set:
            if data[splitting_attr] not in branches:
                branches[data[splitting_attr]] = []
            branches[data[splitting_attr]].append(data)
        for attr, sub_data_set in branches.items():
            node.children[attr] = ID3(sub_data_set, attribute_metadata, numerical_splits_count, depth - 1)
    # else is numeric
    else:
        left_sub_data_set = []
        right_sub_data_set = []
        for data in data_set:
            if data[splitting_attr] < splitting_value:
                left_sub_data_set.append(data)
            else:
                right_sub_data_set.append(data)
        node.children = []
        node.children.append(ID3(left_sub_data_set, attribute_metadata, numerical_splits_count, depth - 1))
        node.children.append(ID3(right_sub_data_set, attribute_metadata, numerical_splits_count, depth - 1))

    # return the generated tree
    return node

def check_homogenous(data_set):
    '''
    ========================================================================================================
    Input:  A data_set
    ========================================================================================================
    Job:    Checks if the output value (index 0) is the same for all examples in the the data_set, if so return that output value, otherwise return None.
    ========================================================================================================
    Output: Return either the homogenous attribute or None
    ========================================================================================================
     '''
    # Your code here

    if not data_set:
        return None

    #Load the attribute at index 0
    attr_val = data_set[0][0]

    #Compare every item's attribute with attr_val
    for data in data_set:
        if data[0] != attr_val and data[0] != '?':
            return None

    #Return attr_val
    return attr_val
# ======== Test Cases =============================
# data_set = [[0],[1],[1],[1],[1],[1]]
# check_homogenous(data_set) ==  None
# data_set = [[0],[1],[None],[0]]
# check_homogenous(data_set) ==  None
# data_set = [[1],[1],[1],[1],[1],[1]]
# check_homogenous(data_set) ==  1

def pick_best_attribute(data_set, attribute_metadata, numerical_splits_count):
    '''
    ========================================================================================================
    Input:  A data_set, attribute_metadata, splits counts for numeric
    ========================================================================================================
    Job:    Find the attribute that maximizes the gain ratio. If attribute is numeric return best split value.
            If nominal, then split value is False.
            If gain ratio of all the attributes is 0, then return False, False
            Only consider numeric splits for which numerical_splits_count is greater than zero
    ========================================================================================================
    Output: best attribute, split value if numeric
    ========================================================================================================
    '''
    # Your code here
    max_gain = float('-inf')
    best_attr = -1
    best_split = False

    for i in range(1, len(attribute_metadata)):
        if numerical_splits_count[i] == 0:
            continue
        if attribute_metadata[i]['is_nominal']:
            gain = gain_ratio_nominal(data_set, i)
            if gain > max_gain:
                max_gain = gain
                best_attr = i
        else:
            gain, split = gain_ratio_numeric(data_set, i, 1)
            if gain > max_gain:
                max_gain = gain
                best_attr = i
                best_split = split

    if best_attr == -1:
        raise ValueError('invalid splitting attribute')

    return best_attr, best_split

# # ======== Test Cases =============================
# numerical_splits_count = [20,20]
# attribute_metadata = [{'name': "winner",'is_nominal': True},{'name': "opprundifferential",'is_nominal': False}]
# data_set = [[1, 0.27]  [0, 0.42], [0, 0.86], [0, 0.68], [0, 0.04], [1, 0.01], [1, 0.33], [1, 0.42], [0, 0.51], [1, 0.4]]
# pick_best_attribute(data_set, attribute_metadata, numerical_splits_count) == (1, 0.51)
# attribute_metadata = [{'name': "winner",'is_nominal': True},{'name': "weather",'is_nominal': True}]
# data_set = [[0, 0], [1, 0], [0, 2], [0, 2], [0, 3], [1, 1], [0, 4], [0, 2], [1, 2], [1, 5]]
# pick_best_attribute(data_set, attribute_metadata, numerical_splits_count) == (1, False)

# Uses gain_ratio_nominal or gain_ratio_numeric to calculate gain ratio.

def mode(data_set):
    '''
    ========================================================================================================
    Input:  A data_set
    ========================================================================================================
    Job:    Takes a data_set and finds mode of index 0.
    ========================================================================================================
    Output: mode of index 0.
    ========================================================================================================
    '''
    # Your code here

    #Use a dictionary to save the count of possible classifications
    dict = {}

    #Use to store the mode
    classification = None
    maxm = 0

    #Count the possible classifications
    for data in data_set:
        key = data[0]
        if key == '?':
            continue
        if dict.has_key(key):
            dict[key] +=1
        else:
            dict[key] = 1

    #Get the classification which counts most
    for key, val in dict.items():
        if classification == None:
            classification = key
            maxm = val
        else:
            if val > maxm:
                classification = key
                maxm = val

    return classification
# ======== Test case =============================
# data_set = [[0],[1],[1],[1],[1],[1]]
# mode(data_set) == 1
# data_set = [[0],[1],[0],[0]]
# mode(data_set) == 0

def entropy(data_set):
    '''
    ========================================================================================================
    Input:  A data_set
    ========================================================================================================
    Job:    Calculates the entropy of the attribute at the 0th index, the value we want to predict.
    ========================================================================================================
    Output: Returns entropy. See Textbook for formula
    ========================================================================================================
    '''
    #Save the count of data_set
    total = len(data_set)

    #Save the count of possible classifications
    dict = {}

    #Inital entropy value
    entropy_val = 0.0

    #Count the possible classifications
    for data in data_set:
        key = data[0]
        if dict.has_key(key):
            dict[key] += 1
        else:
            dict[key] = 1

    #Compute the entropy value
    for _, val in dict.items():
        pi = float(val) / total
        entropy_val += pi * math.log(pi, 2)

    return - entropy_val

# ======== Test case =============================
# data_set = [[0],[1],[1],[1],[0],[1],[1],[1]]
# entropy(data_set) == 0.811
# data_set = [[0],[0],[1],[1],[0],[1],[1],[0]]
# entropy(data_set) == 1.0
# data_set = [[0],[0],[0],[0],[0],[0],[0],[0]]
# entropy(data_set) == 0


def gain_ratio_nominal(data_set, attribute):
    '''
    ========================================================================================================
    Input:  Subset of data_set, index for a nominal attribute
    ========================================================================================================
    Job:    Finds the gain ratio of a nominal attribute in relation to the variable we are training on.
    ========================================================================================================
    Output: Returns gain_ratio. See https://en.wikipedia.org/wiki/Information_gain_ratio
    ========================================================================================================
    '''
    # Your code here
    IG = 0.0
    IV = 0.0
    IGR = 0.0
    HEx = 0.0
    H_sub_total = 0.0
    total = len(data_set)

    dict = split_on_nominal(data_set, attribute)

    for key, val in dict.items():
        sub = val
        sub_total = len(sub)
        H_sub = entropy(sub)
        H_sub_total += H_sub * sub_total / total
        piv = float(sub_total) / total
        IV_sub = piv * math.log(piv, 2)
        IV += IV_sub

    HEx = entropy(data_set)
    IG = HEx - H_sub_total
    IV = - IV
    IGR = IG / IV

    return IGR
# ======== Test case =============================
# data_set, attr = [[1, 2], [1, 0], [1, 0], [0, 2], [0, 2], [0, 0], [1, 3], [0, 4], [0, 3], [1, 1]], 1
# gain_ratio_nominal(data_set,attr) == 0.11470666361703151
# data_set, attr = [[1, 2], [1, 2], [0, 4], [0, 0], [0, 1], [0, 3], [0, 0], [0, 0], [0, 4], [0, 2]], 1
# gain_ratio_nominal(data_set,attr) == 0.2056423328155741
# data_set, attr = [[0, 3], [0, 3], [0, 3], [0, 4], [0, 4], [0, 4], [0, 0], [0, 2], [1, 4], [0, 4]], 1
# gain_ratio_nominal(data_set,attr) == 0.06409559743967516

def gain_ratio_numeric(data_set, attribute, steps):
    '''
    ========================================================================================================
    Input:  Subset of data set, the index for a numeric attribute, and a step size for normalizing the data.
    ========================================================================================================
    Job:    Calculate the gain_ratio_numeric and find the best single threshold value
            The threshold will be used to split examples into two sets
                 those with attribute value GREATER THAN OR EQUAL TO threshold
                 those with attribute value LESS THAN threshold
            Use the equation here: https://en.wikipedia.org/wiki/Information_gain_ratio
            And restrict your search for possible thresholds to examples with array index mod(step) == 0
    ========================================================================================================
    Output: This function returns the gain ratio and threshold value
    ========================================================================================================
    '''
    # Your code here
    IG = 0.0
    IV = 0.0
    IGR = 0.0
    threshold = 0.0
    HEx = 0.0
    total = len(data_set)

    HEx = entropy(data_set)

    for i in range(total):
        if (i % steps) == 0:
            thresh = data_set[i][attribute]
            sub1, sub2 = split_on_numerical(data_set, attribute, thresh)
            IG = HEx - entropy(sub1) *len(sub1) / total - entropy(sub2) * len(sub2) / total
            piv1 = float(len(sub1)) / total
            piv2 = float(len(sub2)) / total
            if piv1 == 0:
                IV_sub1 = 0
            else:
                IV_sub1 = piv1 * math.log(piv1, 2)
            if piv2 == 0:
                IV_sub2 = 0
            else:
                IV_sub2 = piv2 * math.log(piv2, 2)
            IV = - (IV_sub1 + IV_sub2)
            # print IV
            if IV == 0:
                continue
            if IG / IV > IGR:
                IGR = IG / IV
                threshold = thresh

    return IGR, threshold
# ======== Test case =============================
# data_set,attr,step = [[0,0.05], [1,0.17], [1,0.64], [0,0.38], [0,0.19], [1,0.68], [1,0.69], [1,0.17], [1,0.4], [0,0.53]], 1, 2
# gain_ratio_numeric(data_set,attr,step) == (0.31918053332474033, 0.64)
# data_set,attr,step = [[1, 0.35], [1, 0.24], [0, 0.67], [0, 0.36], [1, 0.94], [1, 0.4], [1, 0.15], [0, 0.1], [1, 0.61], [1, 0.17]], 1, 4
# gain_ratio_numeric(data_set,attr,step) == (0.11689800358692547, 0.94)
# data_set,attr,step = [[1, 0.1], [0, 0.29], [1, 0.03], [0, 0.47], [1, 0.25], [1, 0.12], [1, 0.67], [1, 0.73], [1, 0.85], [1, 0.25]], 1, 1
# gain_ratio_numeric(data_set,attr,step) == (0.23645279766002802, 0.29)

def split_on_nominal(data_set, attribute):
    '''
    ========================================================================================================
    Input:  subset of data set, the index for a nominal attribute.
    ========================================================================================================
    Job:    Creates a dictionary of all values of the attribute.
    ========================================================================================================
    Output: Dictionary of all values pointing to a list of all the data with that attribute
    ========================================================================================================
    '''
    # Your code here
    split = {}

    for data in data_set:
        key = data[attribute]
        if split.has_key(key):
            split[key].append(data)
        else:
            split[key] = [data]

    return split
# ======== Test case =============================
# data_set, attr = [[0, 4], [1, 3], [1, 2], [0, 0], [0, 0], [0, 4], [1, 4], [0, 2], [1, 2], [0, 1]], 1
# split_on_nominal(data_set, attr) == {0: [[0, 0], [0, 0]], 1: [[0, 1]], 2: [[1, 2], [0, 2], [1, 2]], 3: [[1, 3]], 4: [[0, 4], [0, 4], [1, 4]]}
# data_set, attr = [[1, 2], [1, 0], [0, 0], [1, 3], [0, 2], [0, 3], [0, 4], [0, 4], [1, 2], [0, 1]], 1
# split on_nominal(data_set, attr) == {0: [[1, 0], [0, 0]], 1: [[0, 1]], 2: [[1, 2], [0, 2], [1, 2]], 3: [[1, 3], [0, 3]], 4: [[0, 4], [0, 4]]}

def split_on_numerical(data_set, attribute, splitting_value):
    '''
    ========================================================================================================
    Input:  Subset of data set, the index for a numeric attribute, threshold (splitting) value
    ========================================================================================================
    Job:    Splits data_set into a tuple of two lists, the first list contains the examples where the given
	attribute has value less than the splitting value, the second list contains the other examples
    ========================================================================================================
    Output: Tuple of two lists as described above
    ========================================================================================================
    '''
    # Your code here
    split = {}

    missing_attribute = False

    if sum(x[attribute] == '?' for x in data_set) != 0:
        count_below_splitting_attr = reduce(lambda x, y: x + (y[a] < splitting_value), data_set, 0)
        count_above_splitting_attr = reduce(lambda x, y: x + (y[a] >= splitting_value), data_set, 0)
        if  count_below_splitting_attr < count_above_splitting_attr:
            missing_attribute = True


    sub1 = [data for data in data_set if data[attribute] < splitting_value or (not missing_attribute and data[attribute] == '?')]
    sub2 = [data for data in data_set if data[attribute] >= splitting_value or (missing_attribute and data[attribute] == '?')]
    split = (sub1, sub2)

    return split
# ======== Test case =============================
# d_set,a,sval = [[1, 0.25], [1, 0.89], [0, 0.93], [0, 0.48], [1, 0.19], [1, 0.49], [0, 0.6], [0, 0.6], [1, 0.34], [1, 0.19]],1,0.48
# split_on_numerical(d_set,a,sval) == ([[1, 0.25], [1, 0.19], [1, 0.34], [1, 0.19]],[[1, 0.89], [0, 0.93], [0, 0.48], [1, 0.49], [0, 0.6], [0, 0.6]])
# d_set,a,sval = [[0, 0.91], [0, 0.84], [1, 0.82], [1, 0.07], [0, 0.82],[0, 0.59], [0, 0.87], [0, 0.17], [1, 0.05], [1, 0.76]],1,0.17
# split_on_numerical(d_set,a,sval) == ([[1, 0.07], [1, 0.05]],[[0, 0.91],[0, 0.84], [1, 0.82], [0, 0.82], [0, 0.59], [0, 0.87], [0, 0.17], [1, 0.76]])
