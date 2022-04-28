import itertools
from Apriori import Apriori
from Eclat import Eclat
import time
import sys

class associationrules():
    def __init__(self,algorithm,minimum_support, minimum_confidance,input_file,output_file):
        self.minimum_support = minimum_support
        self.minimum_confidance = minimum_confidance
        self.algorithm=algorithm
        self.freq_itemsets={}
        self.input_file=""
        self.output_file=""

    def rule_generation(self, freq_itemsets, minimum_confidance):
        association_rules = {}
        for key in freq_itemsets.keys():
            for itemset in freq_itemsets:
                set_len = len(itemset)
                if int(key) > 1:
                    for consequent_len in range(1, set_len):
                        # Getting all possible combinations of the itemsets-consequents
                        itemset_subsets = set(itertools.combinations(set(list(itemset)), (set_len - consequent_len)))
                        consequents = set(itertools.combinations(set(list(itemset)), consequent_len))
                        for itemset_subset in itemset_subsets:
                            for consequent in consequents:
                                # Check if the pairs occur in the dataset.
                                set_union = set(list(itemset_subset)).union(set(list(consequent)))
                                if set_union == set(list(itemset)) and len(set_union) == len(itemset):
                                    if len(itemset_subset) == 1:
                                        itemset_subset = itemset_subset[0]
                                        sub_key = 1
                                    else:
                                        sub_key = len(itemset_subset)
                                        itemset_subset = ''.join(sorted(set(itemset_subset)))
                                    
                                    confidence = freq_itemsets[itemset] / freq_itemsets[itemset_subset]
                                    if confidence >= self.minimum_confidance:
                                        if len(consequent) == 1:
                                            consequent = consequent[0]
                                        flag = 0
                                        if flag == 0:
                                            association_rules[tuple([itemset_subset, consequent,freq_itemsets[itemset]])] = confidence
                                            
        return association_rules

    def display_rule(self,association_rules):
        for k, v in association_rules.items():
            if v==1:
               print("{} ===> {} support={} confidence={}\n".format(k[0],''.join(sorted(set(k[1]))),k[2],round(v,2))) 
            else:
                print("{} ---> {} support={} confidence={}\n".format(k[0],''.join(sorted(set(k[1]))),k[2],round(v,2)))
        print("in total we have {} association rules".format(len(association_rules)))

    def save_rules(self,association_rules,filename):
        print("Saving output to file:",filename)
        with open(filename, 'w') as f:
            for k, v in association_rules.items():
                if v==1:
                    f.write("{}===>{} support={} conf={}\n".format(k[0],''.join(sorted(set(k[1]))),k[2],round(v,1)))
                else:
                    f.write("{}--->{} support={} conf={}\n".format(k[0],''.join(sorted(set(k[1]))),k[2],round(v,1)))
            
    def algo(self, algorithm, minsup, minconf,input_file,output_file):
        if algorithm== "apriori":
            apriori = Apriori()
            apriori.read_input(input_file)
            start_time = time.time()
            apriori.find_supersets_k(minsup)
            self.freq_itemsets=apriori.save_frequent_itemsets()
            rules=self.rule_generation(self.freq_itemsets,minconf)
            end_time=time.time()-start_time
            self.display_rule(rules)
            print("in total we have {} frequent itemsets".format(len(self.freq_itemsets)))
            self.save_rules(rules,output_file)
            print(end_time)
        if algorithm== "eclat":
            eclat = Eclat()
            eclat.read_input(input_file)
            start_time = time.time()
            eclat.find_supersets_k(minsup)
            self.freq_itemsets=eclat.save_frequent_itemsets()
            rules=self.rule_generation(self.freq_itemsets,minconf)
            end_time=time.time()-start_time
            self.display_rule(rules)
            print("in total we have {} frequent itemsets".format(len(self.freq_itemsets)))
            self.save_rules(rules,output_file)
            print(end_time)

if __name__ == '__main__':
    if len(sys.argv) != 6:
        print("Please use correct args!")
        sys.exit()
    algorithm = sys.argv[1]
    minimum_support = float(sys.argv[2])
    minimum_confidance=float(sys.argv[3])
    input_file = sys.argv[4]
    output_file = sys.argv[5]
    
    ass=associationrules(algorithm,minimum_support, minimum_confidance,input_file,output_file)
    ass.algo(algorithm,minimum_support, minimum_confidance,input_file,output_file)
