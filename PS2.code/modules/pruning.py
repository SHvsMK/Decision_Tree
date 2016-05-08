from node import Node
from ID3 import *
from operator import xor

# Note, these functions are provided for your reference.  You will not be graded on their behavior,
# so you can implement them as you choose or not implement them at all if you want to use a different
# architecture for pruning.

def reduced_error_pruning(root,training_set,validation_set):
    '''
    take the a node, training set, and validation set and returns the improved node.
    You can implement this as you choose, but the goal is to remove some nodes such that doing so improves validation accuracy.
    NOTE you will probably not need to use the training set for your pruning strategy, but it's passed as an argument in the starter code just in case.
    '''
    # Your code here
    # if is leaf node
    if not root.label:
        return

    # if not leaf node
    # traverse to the leaf node (to do the pruning from leaf node)
    if root.is_nominal:
        for attr, child in root.children:
            new_training_set = [data for data in training_set if data[root.decision_attribute] == attr]
            new_validation_set = [data for data in validation_set if data[root.decision_attribute] == attr]
            reduced_error_pruning(child, new_training_set, new_validation_set)
    else:
        # left child
        new_training_set = [data for data in training_set if data[root.decision_attribute] < root.splitting_value]
        new_validation_set = [data for data in validation_set if data[root.decision_attribute] < root.splitting_value]
        reduced_error_pruning(root.children[0], new_training_set, new_validation_set)
        # right child
        new_training_set = [data for data in training_set if data[root.decision_attribute] >= root.splitting_value]
        new_validation_set = [data for data in validation_set if data[root.decision_attribute] >= root.splitting_value]
        reduced_error_pruning(root.children[1], new_training_set, new_validation_set)

    # pruning
    unpruned_accuracy = validation_accuracy(root, validation_set)
    new_label = mode(validate_set)
    pruned_accuracy = sum(data[0] == new_label for data in validation_set) / len(validation_set)
    if pruned_accuracy >= unpruned_accuracy:
        root.label = new_label
        root.children = {}

def validation_accuracy(tree,validation_set):
    '''
    takes a tree and a validation set and returns the accuracy of the set on the given tree
    '''
    # Your code here
    correct_count = 0
    for data in validation_set:
        if tree.classify(data) == data[0]:
            correct_count += 1

    return correct_count / float(len(validation_set))
