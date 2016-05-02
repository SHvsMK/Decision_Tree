from nose import with_setup
import modules.ID3 as ID3

def setup():
    print "ID3 Test setup"

def teardown():
    print "ID3 Test teardown"

def func_split_on_nominal_start():
    print "split_on_nominal_test start"

def func_split_on_nominal_end():
    print "split_on_nominal_test end"

@with_setup(func_split_on_nominal_start, func_split_on_nominal_end)
def Test_split_on_nominal():
    split = {}

    data_set, attr = [[0, 4], [1, 3], [1, 2], [0, 0], [0, 0], [0, 4], [1, 4], [0, 2], [1, 2], [0, 1]], 1
    split = ID3.split_on_nominal(data_set, attr)
    assert split == {0: [[0, 0], [0, 0]], 1: [[0, 1]], 2: [[1, 2], [0, 2], [1, 2]], 3: [[1, 3]], 4: [[0, 4], [0, 4], [1, 4]]}

    data_set, attr = [[1, 2], [1, 0], [0, 0], [1, 3], [0, 2], [0, 3], [0, 4], [0, 4], [1, 2], [0, 1]], 1
    split = ID3.split_on_nominal(data_set, attr)
    assert split == {0: [[1, 0], [0, 0]], 1: [[0, 1]], 2: [[1, 2], [0, 2], [1, 2]], 3: [[1, 3], [0, 3]], 4: [[0, 4], [0, 4]]}

def func_split_on_numerical_start():
    print "split_on_numerical_test start"

def func_split_on_numerical_end():
    print "split_on_numerical_test end"

@with_setup(func_split_on_numerical_start, func_split_on_numerical_end)
def Test_split_on_numerical():
    split = {}

    d_set,a,sval = [[1, 0.25], [1, 0.89], [0, 0.93], [0, 0.48], [1, 0.19], [1, 0.49], [0, 0.6], [0, 0.6], [1, 0.34], [1, 0.19]],1,0.48
    split = ID3.split_on_numerical(d_set,a,sval)
    assert split == ([[1, 0.25], [1, 0.19], [1, 0.34], [1, 0.19]],[[1, 0.89], [0, 0.93], [0, 0.48], [1, 0.49], [0, 0.6], [0, 0.6]])

    d_set,a,sval = [[0, 0.91], [0, 0.84], [1, 0.82], [1, 0.07], [0, 0.82],[0, 0.59], [0, 0.87], [0, 0.17], [1, 0.05], [1, 0.76]],1,0.17
    split = ID3.split_on_numerical(d_set,a,sval)
    assert split == ([[1, 0.07], [1, 0.05]],[[0, 0.91],[0, 0.84], [1, 0.82], [0, 0.82], [0, 0.59], [0, 0.87], [0, 0.17], [1, 0.76]])

def func_entropy_start():
    print "entropy_test start"

def func_entropy_end():
    print "entropy_test end"

@with_setup(func_entropy_start, func_entropy_end)
def Test_entropy():
    entropy = 0.0

    data_set = [[1],[1],[0]]
    entropy = ID3.entropy(data_set)
    assert (entropy - 0.918) < 0.001

    data_set = [[1]]
    entropy = ID3.entropy(data_set)
    assert entropy == 0

    data_set = [[0],[1]]
    entropy = ID3.entropy(data_set)
    assert entropy == 1.0

    data_set = [[0],[1],[1],[1],[0],[1],[1],[1]]
    entropy = ID3.entropy(data_set)
    assert (entropy - 0.811) < 0.001

    data_set = [[0],[0],[1],[1],[0],[1],[1],[0]]
    entropy = ID3.entropy(data_set)
    assert entropy == 1.0

    data_set = [[0],[0],[0],[0],[0],[0],[0],[0]]
    entropy = ID3.entropy(data_set)
    assert entropy == 0

def func_mode_start():
    print "mode_test start"

def func_mode_end():
    print "mode_test end"

@with_setup(func_mode_start, func_mode_end)
def Test_mode():
    mode = 0

    data_set = [[0],[1],[1],[1],[1],[1]]
    mode = ID3.mode(data_set)
    assert mode == 1

    data_set = [[0],[1],[0],[0]]
    mode = ID3.mode(data_set)
    assert mode == 0

def func_check_homogenous_start():
    print "check_homogenous_test start"

def func_check_homogenous_end():
    print "check_homogenous_test end"

@with_setup(func_check_homogenous_start, func_check_homogenous_end)
def Test_check_homogenous():
    attr_val = None

    data_set = [[0],[1],[1],[1],[1],[1]]
    attr_val = ID3.check_homogenous(data_set)
    assert attr_val ==  None

    data_set = [[0],[1],[None],[0]]
    attr_val = ID3.check_homogenous(data_set)
    # assert attr_val ==  None

    data_set = [[1],[1],[1],[1],[1],[1]]
    attr_val = ID3.check_homogenous(data_set)
    assert attr_val ==  1

def func_gain_ratio_nominal_start():
    print "gain_ratio_nominal_test start"

def func_gain_ratio_nominal_end():
    print "gain_ratio_nominal_test end"

@with_setup(func_gain_ratio_nominal_start, func_gain_ratio_nominal_end)
def Test_gain_ratio_nominal():
    IGR = 0.0

    data_set, attr = [[1, 2], [1, 0], [1, 0], [0, 2], [0, 2], [0, 0], [1, 3], [0, 4], [0, 3], [1, 1]], 1
    IGR = ID3.gain_ratio_nominal(data_set,attr)
    print IGR
    assert IGR == 0.11470666361703151

    data_set, attr = [[1, 2], [1, 2], [0, 4], [0, 0], [0, 1], [0, 3], [0, 0], [0, 0], [0, 4], [0, 2]], 1
    IGR = ID3.gain_ratio_nominal(data_set,attr)
    print IGR
    assert (IGR - 0.2056423328155741) < 0.00001

    data_set, attr = [[0, 3], [0, 3], [0, 3], [0, 4], [0, 4], [0, 4], [0, 0], [0, 2], [1, 4], [0, 4]], 1
    IGR = ID3.gain_ratio_nominal(data_set,attr)
    print IGR
    assert IGR == 0.06409559743967516

def func_gain_ratio_numeric_start():
    print "gain_ratio_numeric_test start"

def func_gain_ratio_numeric_end():
    print "gain_ratio_numeric_test end"

@with_setup(func_gain_ratio_numeric_start, func_gain_ratio_numeric_end)
def Test_gain_ratio_numeric():
    IGR = 0.0
    threshold = 0.0

    data_set,attr,step = [[0,0.05], [1,0.17], [1,0.64], [0,0.38], [0,0.19], [1,0.68], [1,0.69], [1,0.17], [1,0.4], [0,0.53]], 1, 2
    IGR, threshold = ID3.gain_ratio_numeric(data_set,attr,step)
    assert threshold == 0.64
    assert (IGR - 0.31918053332474033) < 0.0000001

    data_set,attr,step = [[1, 0.35], [1, 0.24], [0, 0.67], [0, 0.36], [1, 0.94], [1, 0.4], [1, 0.15], [0, 0.1], [1, 0.61], [1, 0.17]], 1, 4
    IGR, threshold = ID3.gain_ratio_numeric(data_set,attr,step)
    assert (IGR, threshold) == (0.11689800358692547, 0.94)

    data_set,attr,step = [[1, 0.1], [0, 0.29], [1, 0.03], [0, 0.47], [1, 0.25], [1, 0.12], [1, 0.67], [1, 0.73], [1, 0.85], [1, 0.25]], 1, 1
    IGR, threshold = ID3.gain_ratio_numeric(data_set,attr,step)
    assert (IGR, threshold) == (0.23645279766002802, 0.29)

def func_pick_best_attribute_start():
    print "pick_best_attribute_test start"

def func_pick_best_attribute_end():
    print "pick_best_attribute_test end"

@with_setup(func_pick_best_attribute_start, func_pick_best_attribute_end)
def Test_pick_best_attribute():
    attri = -1
    split = None

    numerical_splits_count = [20,20]

    attribute_metadata = [{'name': "winner",'is_nominal': True},{'name': "opprundifferential",'is_nominal': False}]
    data_set = [[1, 0.27], [0, 0.42], [0, 0.86], [0, 0.68], [0, 0.04], [1, 0.01], [1, 0.33], [1, 0.42], [0, 0.51], [1, 0.4]]
    attri, split = ID3.pick_best_attribute(data_set, attribute_metadata, numerical_splits_count)
    assert (attri, split) == (1, 0.51)

    attribute_metadata = [{'name': "winner",'is_nominal': True},{'name': "weather",'is_nominal': True}]
    data_set = [[0, 0], [1, 0], [0, 2], [0, 2], [0, 3], [1, 1], [0, 4], [0, 2], [1, 2], [1, 5]]
    attri, split = ID3.pick_best_attribute(data_set, attribute_metadata, numerical_splits_count)
    assert (attri, split) == (1, False)
