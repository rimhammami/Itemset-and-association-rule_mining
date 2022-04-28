# Itemset-and-association-rule_mining

There are 4 itemset mining algorithms in this software: Apriori, Eclat, Apriori-Close, and Apriori-Rare

the cmd is as follows: Python fim.py [algorithm] <minimum_support> [inputfile.txt] [outputfile.txt]

where algorithm has to be one of the following: apriori, eclat, aprioriclose, or apriori rare

e.g.: Python fim.py Apriori 3 input/d.txt output/doutputApriori.txt


For association rule mining the cmd has to be in the following format: 

Python arm.py [algorithm] <minimum_support> <minimum_confidence> [inputfile.txt] [outputfile.txt]

where: (1) algorithm can either be Apriori or Eclat (2) minimum_confidence ranges from 0 to 1


e.g.: Python arm.py apriori 3 0.6 input/d.txt output/darm.txt 
