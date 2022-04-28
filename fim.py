from Apriori import Apriori
from Apriori_Close import Apriori_Close
from Apriori_Rare import Apriori_Rare
from Eclat import Eclat
import argparse
import time
from datetime import datetime
from collections import defaultdict


def get_config():
    parser = argparse.ArgumentParser(description='itemset mining argument parser')
    parser.add_argument('algo', type=str, choices=['apriori', 'eclat', 'aprioriclose', 'apriorirare'], help='algorithm mode')
    parser.add_argument('minimum_support', type=float, default=3, nargs='?',
                        help='minimum support of the frequent itemset')
    parser.add_argument('input_file', type=str, default='input/data.txt', nargs='?', help='file containing the transactions')
    parser.add_argument('output_file', type=str, default='output/data_output.txt', nargs='?', help='file containing the result')
    args = parser.parse_args()
    return args

def run_algo(algo, min_support_ratio,  input_file,output_file):
    if algo == 'apriori':
        apriori = Apriori()
        apriori.read_input(input_file)
        print("[Apriori] Finding frequent itemsets with min support > ",
        min_support_ratio, '--')
        start_time = time.time()
        apriori.find_supersets_k(min_support_ratio)
        apriori.display_output()
        apriori.save_output(output_file)
        end_time=time.time()-start_time
        print(end_time)
        print('----------\n')

    elif algo == 'eclat':
        eclat = Eclat()
        eclat.read_input(input_file)
        print("[Eclat] Finding frequent itemsets with min support > ",
        min_support_ratio, '--')
        start_time = time.time()
        eclat.find_supersets_k(min_support_ratio)
        eclat.display_output()
        eclat.save_output(output_file)
        end_time=time.time()-start_time
        print(end_time)
        print('----------\n')
        
    elif algo == 'aprioriclose':
        close = Apriori_Close()
        close.read_input(input_file)
        print("[Apriori Close] Finding frequent closed itemset with min support > ",
        min_support_ratio, '--')
        start_time = time.time()
        close.find_supersets_k(min_support_ratio)
        close.closed()
        close.display_output()
        close.save_output(output_file)
        end_time=time.time()-start_time
        print(end_time)
        print('----------\n')        
    elif algo == 'apriorirare':
        rare = Apriori_Rare()
        rare.read_input(input_file)
        print("[Apriori Rare] Finding rare itemset with min support < ",
        min_support_ratio, '--')
        start_time = time.time()
        rare.find_supersets_k(min_support_ratio)
        rare.display_output()
        rare.save_output(output_file)
        end_time=time.time()-start_time
        print(end_time)
        print('----------\n')
    else:
        raise NotImplementedError('\nInvalid algorithm.\n')
def main():
    args = get_config()
    run_algo(args.algo, args.minimum_support, args.input_file, args.output_file)
if __name__ == "__main__":
    main()