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
        print("Saving output to file:", filename)
        with open(filename, 'w') as f:
            for k, v in self.frequent_itemsets.items():
                items = ' '.join([str(item) for item in sorted(k)])
                f.write('{} ({})\n'.format(items, v))
    def save_frequent_itemsets(self):
        keys=[]
        values=[]
        for k, v in self.frequent_itemsets.items():
            items = ''.join([str(item) for item in sorted(k)])
            keys.append(items)
            values.append(v)
        for k in keys:
            if k.count('-'):
                k.replace('-','')
                k=''.join(('-',k))

        fq=dict(zip(keys,values))
        return fq
    def display_output(self):
        for k, v in self.frequent_itemsets.items():
            items = ' '.join([str(item) for item in sorted(k)])
            print('{} ({})\n'.format(items, v))
        print("___________________________________________________________________")
        print("\n{} Frequent itemsets.".format(len(self.frequent_itemsets)))

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

class Eclat(FrequentItemsetMining):
    
    def __init__(self):
        super().__init__()
        self.tidset_data = dict()

    def read_input(self, filename):
        print('reading input data...')
        with open(filename, 'r') as fp:
            trans_count = 0
            for idx, line in enumerate(fp):
                trans = [int(item) for item in line.split()]
                self.transactions.append(frozenset(trans))
                for item in trans:
                    self.item_sets.add(frozenset([item]))
                    key = frozenset([item])
                    if key in self.tidset_data.keys():
                        self.tidset_data[key].update({trans_count})
                    else:
                        self.tidset_data[key] = set({trans_count})
                trans_count += 1
            self.transactions_total = trans_count

    def calculate_1_long_itemset_support(self):
        self.frequent_itemsets = dict()
        for key, tidset in self.tidset_data.items():
                self.frequent_itemsets[key] = len(tidset)

    def recalucate_support(self, to_check=None):
            for key in to_check.keys():
                tidsets = [self.tidset_data[frozenset([item])] for item in key]
                intersect = set.intersection(*tidsets)
                to_check[key] = len(intersect)

    def find_supersets_k(self, min_support):
        # find the first level
        self.calculate_1_long_itemset_support()
        self.minimum_support_evaluation(min_support)
        # try to find the next k+1 level until there aren't any anymore
        previous_itemsets_of_prefix = {0: self.frequent_itemsets}
        while True:
            # create a new dictionary for the new level
            current_itemsets_of_prefix = dict()
            super_k_sets_total = 0
            for _, prev_prefix_dict in previous_itemsets_of_prefix.items():
                items = list(prev_prefix_dict.items())
                for i in range(len(items)):
                    k1, v1 = items[i]
                    current_prefix_dict = dict()
                    for j in range(i+1, len(items)):
                        k2, v2 = items[j]
                        new_key = k1 | k2
                        if new_key not in self.frequent_itemsets:
                            current_prefix_dict[new_key] = 0
                    self.recalucate_support(current_prefix_dict)
                    self.minimum_support_evaluation(
                        min_support, current_prefix_dict)
                    current_itemsets_of_prefix[k1] = current_prefix_dict
                    super_k_sets_total += len(
                        current_prefix_dict.items())
            if super_k_sets_total == 0:
                print("Done!")
                return
            #store the current level to use in the generation of the k+1 level
            previous_itemsets_of_prefix = current_itemsets_of_prefix
            # store the new frequent itemsets into the frequent itemsets dictionary 
            for _, current_prefix_dict in current_itemsets_of_prefix.items():
                self.frequent_itemsets.update(current_prefix_dict)   

