import numpy as np
import sys
import time

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

    def calculate_1_long_itemset_support(self):
        pass

    def recalucate_support(self, to_check=None):
        pass

    def minimum_support_evaluation(self, min_support, to_check=None):
        pass
        

    def find_supersets_k(self, min_support):
        pass


class Apriori_Rare(FrequentItemsetMining):
    def __init__(self):
        super().__init__()
        self.rare_itemsets = {}

    def read_input(self, filename):
        print('reading input data...')
        with open(filename, 'r') as fp:
            for line in fp:
                trans = [int(item) for item in line.split()]
                self.transactions.append(frozenset(trans))

                for item in trans:
                    self.item_sets.add(frozenset([item]))
            self.transactions_total = len(self.transactions)

    def display_output(self):
        for k, v in self.rare_itemsets.items():
            items = ' '.join([str(item) for item in sorted(k)])
            print('{} ({})\n'.format(items, v))
        print("___________________________________________________________________")
        print("\n{} Rare itemsets.".format(len(self.rare_itemsets)))
        print("\n{} Frequent itemsets.".format(len(self.frequent_itemsets)))

    def calculate_1_long_itemset_support(self):
        self.frequent_itemsets = {}
        for trans in self.transactions:
            for item in self.item_sets:
                if item.issubset(trans):
                    try:
                        self.frequent_itemsets[item] += 1
                    except KeyError:
                        self.frequent_itemsets[item] = 1

    def recalucate_support(self, dict_to_check=None):
        if not dict_to_check or type(dict_to_check) != dict:
            return
        for trans in self.transactions:
            for k in dict_to_check.keys():
                if k.issubset(trans):
                    dict_to_check[k] += 1

    def minimum_support_evaluation(self, min_support, to_check=None):
        #create two lists to store the rare itemsets and their supports
        rare_keys = []
        rare_values=[]
        if to_check is None:
            to_check = self.frequent_itemsets
        for k, v in to_check.items():
            if v < min_support:
                rare_keys.append(k)
                rare_values.append(v)
        dict_rare = dict(zip(rare_keys, rare_values)) #create a dictionary of rare itemsets and their support using the lists
        #delete the rare itemsets
        for k in rare_keys:
            to_check.pop(k)
        #store the new rare itemset into the dictionary of rare_itemsets
        self.rare_itemsets.update(dict_rare)
    def find_supersets_k(self, min_support):
        # find the first level
        self.calculate_1_long_itemset_support()
        self.minimum_support_evaluation(min_support)

        #try to find the next k+1 level until there aren't any anymore
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

    def save_output(self, filename):
        print("Saving output to file:", filename)
        with open(filename, 'w') as f:
            for k, v in self.rare_itemsets.items():
                items = ' '.join([str(item) for item in sorted(k)])
                f.write('{} ({})\n'.format(items, v))
