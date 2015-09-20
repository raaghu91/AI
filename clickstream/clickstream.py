__author__ = 'wildgoose'
import pandas as pd
import math
from scipy.stats import chisquare
import time

class feature:
    def __init__(self):
        self.fid = None
        self.mid = None
        self.left = None
        self.right = None
        self.is_leaf = False
        self.label =None

count_nodes_expanded = 0
train_DF = pd.read_csv("trainlabs.csv",header = None)
lst = []
for i in range(len(train_DF)):
     lst.append(train_DF.values[i][0])

def give_counts(ent_list):
    count = len(ent_list)
    #print "count " + str(count)
    count_pos = 0
    count_neg = 0
    for i in ent_list:
        #print ent_list[i]
        if i == 0:
            count_neg+=1
        elif i == 1:
            count_pos+=1
    return count,count_pos,count_neg

def calc_entropy(ent_list):

    count,count_pos,count_neg = give_counts(ent_list)
#     print "count neg: " + str(count_neg)
#     print "count pos: " + str(count_pos)
    if count == 0:
        return 0,0
    prob_neg = count_neg/float(count)
    prob_pos = count_pos/float(count)

#     print "print neg: " + str(prob_neg)
#     print "print pos: " + str(prob_pos)
    if prob_neg == 0:
        entropy_s = -prob_pos*math.log(prob_pos,2)
    elif prob_pos == 0:
        entropy_s =  - prob_neg*math.log(prob_neg,2)
    else :
        entropy_s = -prob_pos*math.log(prob_pos,2) - prob_neg*math.log(prob_neg,2)
    #print entropy_s
    return count,entropy_s

# c_total,e_s = calc_entropy(lst)
# print c_total,e_s
trainfeat_DF = pd.read_csv("trainfeat.csv",header = None,delimiter='\s')

def calc_gain(i, train_subset,train_subset_labels):
    max_val = 0
    inf_gain = -1
    list_for_gain = []
    list_for_length = []
    len_train_subset = len(train_subset)
    c_total,e_s = calc_entropy(train_subset_labels)
    for j in train_subset:
        #print trainfeat_DF.values[j][0]
        list_for_gain.append((trainfeat_DF.values[j][i],train_DF.values[j][0],j))
        list_for_length.append(trainfeat_DF.values[j][i])
    #print "test length" + str(len(set(list_for_length)))
    if str(len(set(list_for_length))) > 1:
        #print "in if"
        for x in list_for_gain:
            #print x
            if x[0]>max_val:
                max_val = x[0]
                #print max_val
        #print max_val
        if max_val ==0:
            return 0,0,0
        elif max_val ==1:
            d = {1:[],2:[]}
            for k in list_for_gain:
                #print k
                val = k[0]
                #print val
                if val == 0:
    #                 print "0"
                    d[1].append(k)
                elif val== 1:
    #                 print "1"
                    d[2].append(k)
        else:
            d = {1:[],2:[]}
            for k in list_for_gain:
                #print k
                val = k[0]
                #print val
                if val >=0 and val <= max_val/2:
                    d[1].append(k)
                elif val > max_val/2:
                    d[2].append(k)
            #print d
        #print lst
        #print d
        #return list_for_gain,d

        list_a = d[1]
        list_b = d[2]
        list_a_1 = []
        for i in list_a:
            list_a_1.append(i[1])
        list_b_1 = []
        for j in list_b:
            list_b_1.append(j[1])
        #print list_b_1
    #     print list_a_1
    #     print list_b_1
        #if len(set(list_b_1)) > 1 and len(set(list_a_1)) > 1 :
        c_a1,e_s_a1 = calc_entropy(list_a_1)
        c_b1,e_s_b1 = calc_entropy(list_b_1)
        inf_gain = e_s - ((c_a1/float(c_total) * e_s_a1) + (c_b1/float(c_total) * e_s_b1))
        #else:
           # inf_gain = e_s
    #print "inf_gain : " + str(inf_gain)
    return inf_gain,d, max_val/2

# i_g =calc_gain(112)
# print i_g


#visited = []
def max_attr(train_subset,train_subset_labels, unvisited):#ig_list = []
    max_ig = -1
    max_ig_attr = -1
    for i in unvisited:
        # if i not in visited:
            #print i
        val_1,dct,mid = calc_gain(i, train_subset,train_subset_labels)
        print i, val_1
        if val_1 > max_ig:
            max_ig = val_1
            max_ig_attr = i
            max_ig_mid = mid
            max_dct = dct
            #print max_ig,max_ig_attr
        #ig_list.append(val_1)
    #print ig_list
    # visited.append(max_ig_attr)
    print max_ig, max_ig_attr
    return max_ig_attr,max_ig_mid,max_dct

def pure(train_subset_labels):
    list = []
    for entry in train_subset_labels:
            list.append(entry)
    if(len(set(list))) > 1:
        return False
    else:
        return True

def chi_sq_distribution(d):
    list_a = d[1]
    list_b = d[2]
    list_a_1 = []
    for i in list_a:
        list_a_1.append(i[1])
    list_b_1 = []
    for j in list_b:
        list_b_1.append(j[1])
    count_a,count_pos_a,count_neg_a = give_counts(list_a_1)
    count_b,count_pos_b,count_neg_b = give_counts(list_b_1)
    total_count = count_a+count_b
    count_pos = count_pos_a+count_pos_b
    count_neg = count_neg_a+count_neg_b
    if count_a == 0 or count_b == 0:
        return (0,0)
    exp_count_pos_a = count_a * count_pos/total_count
    exp_count_neg_a = count_a * count_neg/total_count
    exp_count_pos_b = count_b * count_pos/total_count
    exp_count_neg_b = count_b * count_neg/total_count
    if exp_count_pos_a == 0 or exp_count_neg_a == 0 or exp_count_pos_b ==0 or exp_count_neg_b == 0:
        return(0,0)
    #print exp_count_pos_a,exp_count_neg_a,exp_count_pos_b,exp_count_neg_b
    #print "orig"
    #print count_pos_a,count_neg_a,count_pos_b,count_neg_b
#     s_val = ((exp_count_pos_a - count_pos_a) * (exp_count_pos_a - count_pos_a))/float(exp_count_pos_a) + \
#                 ((exp_count_neg_a - count_neg_a) * (exp_count_neg_a - count_neg_a))/float(exp_count_neg_a) + \
#                     ((exp_count_pos_b - count_pos_b) * (exp_count_pos_b - count_pos_b))/float(exp_count_pos_b) + \
#                         ((exp_count_neg_b - count_neg_b) * (exp_count_neg_b - count_neg_b))/float(exp_count_neg_b)
#     p_val = chisqprob(s_val, 1)
#     print "chisquare"
    s_p =   chisquare([count_pos_a, count_neg_a, count_pos_b, count_neg_b], \
                     f_exp=[exp_count_pos_a, exp_count_neg_a, exp_count_pos_b, exp_count_neg_b],  ddof=1)

    # if math.isnan(s_p[1]):
    #     return (0,0)
    return s_p
total_features = []
for i in range(274):
    total_features.append(i)

def id3_1(train_subset,train_subset_labels,total_features):
    node = feature()
    if len(set(train_subset_labels)) == 1:
        node.is_leaf = True
        node.label = train_subset_labels[0]
        return node
    if len(total_features) == 0:
        node.is_leaf = True
        if train_subset_labels.count(0) > train_subset_labels.count(1):
            node.label = 0
        else:
            node.label = 1
        return node
    attr_fid,attr_mid,attr_dct = max_attr(train_subset,train_subset_labels,total_features)
    node.fid = attr_fid
    node.mid = attr_mid
    total_features.remove(attr_fid)
    left_subset = []
    right_subset = []
    left_subset_labels = []
    right_subset_labels = []
    for entry in attr_dct[1]:
            left_subset.append(entry[2])
            left_subset_labels.append(entry[1])
    for entry in attr_dct[2]:
            right_subset.append(entry[2])
            right_subset_labels.append(entry[1])
    if not left_subset:
        node_left = feature()
        node_left.is_leaf = True
        if left_subset_labels.count(0) > left_subset_labels.count(1):
            node_left.label = 0
        else:
            node_left.label = 1
        node.left = node_left
    else:
        node.left = id3_1(left_subset,left_subset_labels,total_features)
    if not right_subset:
        node_right = feature()
        node_right.is_leaf = True
        if right_subset_labels.count(0) > right_subset_labels.count(1):
            node_right.label = 0
        else:
            node_right.label = 1
        node.right = node_right
    else:
        node.right = id3_1(right_subset,right_subset_labels,total_features)
    return node




def id3(train_subset,train_subset_labels, visited):
    global count_nodes_expanded
    count_nodes_expanded+=1
    attr_fid,attr_mid,attr_dct = max_attr(train_subset,train_subset_labels,list(set(total_features) - set(visited)))
    visited.append(attr_fid)
    print visited
    s_and_p = chi_sq_distribution(attr_dct)
    p_value = s_and_p[1]
    left_subset = []
    right_subset = []
    left_subset_labels = []
    right_subset_labels = []
    for entry in attr_dct[1]:
            left_subset.append(entry[2])
            left_subset_labels.append(entry[1])
    for entry in attr_dct[2]:
            right_subset.append(entry[2])
            right_subset_labels.append(entry[1])
    node = feature(attr_fid,attr_mid)
    if p_value > 0.01:
        print "p_value > 0.01 : " + str(p_value)
        return node
    else:
        print "p_value: " + str(p_value)
        if pure(left_subset_labels):
            return node
        else:
            node.left = id3(left_subset,left_subset_labels,visited)
        if pure(right_subset_labels):
            return node
        else:
            node.right = id3(right_subset,right_subset_labels,visited)
        return node

def test_accuracy(root):
    testfeat_DF = pd.read_csv("testfeat.csv",header = None,delimiter='\s')
    test_DF = pd.read_csv("testlabs.csv",header = None)
    correct = 0
    correct_zeros = 0
    correct_ones = 0
    actual_zero = 0
    for j in range(25000):
        node = root
        while not node.is_leaf:
            if testfeat_DF.values[j][node.fid] > node.mid:
                node = node.right
            else:
                node = node.left
        label = node.label
        if test_DF.values[j][0] == 0:
            actual_zero +=1
        if test_DF.values[j][0] == label:
            correct +=1
            if label == 0:
                correct_zeros+=1
            else:
                correct_ones +=1
    accuracy = correct/float(25000)
    print accuracy,correct,correct_zeros,correct_ones,actual_zero

def main():
    begin = time.time()
    train_list = []
    train_list_labels = []
    for i in range(40000):
        #print train_DF[i][0]
        train_list.append(i)
        train_list_labels.append(train_DF.values[i][0])
    # i_g,d,mid =calc_gain(112,train_list,train_list_labels)
    # print i_g
    root = id3_1(train_list,train_list_labels,total_features)
    end = time.time()
    total_time = end-begin
    test_accuracy(root)
    print "Time Taken : " + str(total_time)
    print count_nodes_expanded


main()



# p_val = chi_sq_distribution(dct)
# print p_val