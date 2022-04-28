import sys
import time
from collections import defaultdict

class FrequentItemsetMining():
    def __init__(self):
        self.item_sets = set()
        self.transactions = []
        self.frequent_itemsets = {}
        self.transactions_total = 0
    def read_input(self, filename):
        pass
    def save_output(self, filename):
        pass
    def display_output(self):
        pass
        
    def calculate_1_long_itemset_support(self):
        pass
    def recalucate_support(self, to_check=None):
        pass
    def minimum_support_evaluation(self, min_support, to_check=None):
        to_be_pruned = []
        if to_check is None:
            to_check = self.frequent_itemsets

        for k, v in to_check.items():
            if v<min_support:
                to_be_pruned.append(k)
        for k in to_be_pruned:
            to_check.pop(k)

    def find_supersets_k(self, min_support):
        pass
    
class Apriori_Close(FrequentItemsetMining):
    def __init__(self):
        super().__init__()

    def read_input(self, filename):
        print('reading input data...')
        with open(filename, 'r') as fp:
            for line in fp:
                trans = [int(item) for item in line.split()]
                self.transactions.append(frozenset(trans))

                for item in trans:
                    self.item_sets.add(frozenset([item]))
            self.transactions_total = len(self.transactions)

    def calculate_1_long_itemset_support(self):
        self.frequent_itemsets = {}
        for trans in self.transactions:
            for item in self.item_sets:
                if item.issubset(trans):
                    try:
                        self.frequent_itemsets[item] += 1
                    except KeyError:
                        self.frequent_itemsets[item] = 1

    def recalucate_support(self, to_check=None):
        if not to_check or type(to_check) != dict:
            return
        for trans in self.transactions:
            for k in to_check.keys():
                if k.issubset(trans):
                    to_check[k] += 1

    def find_supersets_k(self, min_support):
        # find the first level
        self.calculate_1_long_itemset_support()
        self.minimum_support_evaluation(min_support)

        # try to find the next k+1 level until there aren't any anymore
        previous_level = self.frequent_itemsets
        while True:
            # create a new dictionary for the new level
            current_level = dict()
            items = list(previous_level.items())
            item_sets = set()
            for item in previous_level.keys():
                item_sets.add(item)
            for i in range(len(items)):
                for j in range(i+1, len(items)):
                    k1, v1 = items[i]
                    k2, v2 = items[j]
                    new_key = k1 | k2
                    continue_flag = 0
                    for k in new_key:
                        temporary_set = frozenset(new_key - set({k}))
                        testing_set = frozenset([temporary_set])
                        if not testing_set.issubset(item_sets):
                            continue_flag = 1
                            break
                    if new_key not in self.frequent_itemsets and continue_flag == 0:
                        current_level[new_key] = 0

            self.recalucate_support(current_level)
            self.minimum_support_evaluation(min_support, current_level)

            if len(current_level.items()) == 0:
                print("Done!")
                return
            #store the current level to use in the generation of the k+1 level
            previous_level = current_level
            # store the new frequent itemsets into the frequent itemsets dictionary 
            self.frequent_itemsets.update(current_level)

    def closed(self) :
        list1 = []
        list2 = []
        item_sets = sorted(self.frequent_itemsets.keys(),key = len ,reverse=True)
        for item in item_sets :
            if len(item) == len(item_sets[0]) :
                self.frequent_itemsets[item] = [self.frequent_itemsets[item], True]
                list1.append(item)
            else :
                closed  = True
                if  len(list1[0]) - len(item) == 2 :
                    list1 = list2
                    list2 = []    
                list2.append(item)
                for super_set in list1 :
                    if item <= super_set and (self.frequent_itemsets[item] == self.frequent_itemsets[super_set][0]):
                        closed=False
                self.frequent_itemsets[item] = [self.frequent_itemsets[item], closed]
        return self.frequent_itemsets

    def save_output(self, filename):
        print("Saving output to file:", filename)
        with open(filename, 'w') as f:
            for k, v in self.frequent_itemsets.items():
                items = ' '.join([str(item) for item in sorted(k)])
                if v[1]==True:
                    f.write('{} ({})+\n'.format(items, v))
                if v[1]==False:
                    f.write('{} ({})-\n'.format(items, v))

    def display_output(self):
        c=0
        for k, v in self.frequent_itemsets.items():
            items = ' '.join([str(item) for item in sorted(k)])
            if v[1]== True:
                print('{} ({})+\n'.format(items, v[0]))
                c+=1
            if v[1]==False:
                print('{} ({})-\n'.format(items, v[0]))
        print("___________________________________________________________________")
        print("\n{} frequent itemsets.".format(len(self.frequent_itemsets)))
        print("\n{} Closed frequent itemsets".format(c))
