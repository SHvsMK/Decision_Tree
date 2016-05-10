from random import shuffle
from ID3 import *
from operator import xor
from parse import parse
import matplotlib.pyplot as plt
import os.path
from pruning import validation_accuracy
import random

# NOTE: these functions are just for your reference, you will NOT be graded on their output
# so you can feel free to implement them as you choose, or not implement them at all if you want
# to use an entirely different method for graphing

def get_graph_accuracy_partial(train_set, attribute_metadata, validate_set, numerical_splits_count, pct):
    '''
    get_graph_accuracy_partial - Given a training set, attribute metadata, validation set, numerical splits count, and percentage,
    this function will return the validation accuracy of a specified (percentage) portion of the training set.
    '''
    # randomly generate an array of indices from 0 to len(train_set) - 1
    random_indices = random.sample(range(len(train_set)), int(pct * len(train_set)))
    # train the decision tree
    decision_tree = ID3([train_set[i] for i in random_indices], attribute_metadata, numerical_splits_count, float('inf'))
    # calculate the accuracy on validation set
    return validation_accuracy(decision_tree, validate_set)

def get_graph_data(train_set, attribute_metadata, validate_set, numerical_splits_count, iterations, pcts):
    '''
    Given a training set, attribute metadata, validation set, numerical splits count, iterations, and percentages,
    this function will return an array of the averaged graph accuracy partials based off the number of iterations.
    '''
    # the array of average accuracies to be returned
    average_accuracies = []
    # calculate average accuracy for each percentage
    for percentage in pcts:
        total_accuracy = 0.0
        for i in range(iterations):
            total_accuracy += get_graph_accuracy_partial(train_set, attribute_metadata, validate_set, numerical_splits_count, percentage)
        average_accuracies.append(total_accuracy/iterations)
    return average_accuracies

# get_graph will plot the points of the results from get_graph_data and return a graph
def get_graph(train_set, attribute_metadata, validate_set, numerical_splits_count, depth, iterations, lower, upper, increment):
    '''
    get_graph - Given a training set, attribute metadata, validation set, numerical splits count, depth, iterations, lower(range),
    upper(range), and increment, this function will graph the results from get_graph_data in reference to the drange
    percentages of the data.
    '''
    # generate the array of percentages
    percentages = []
    percentage = lower
    while percentage <= upper:
        percentages.append(percentage)
        percentage += increment
    # calculate accuracies for all percentages
    average_accuracies = get_graph_data(train_set, attribute_metadata, validate_set, numerical_splits_count, iterations, percentages)
    # plot the graph
    plt.plot(percentages, average_accuracies)
    plt.show()
