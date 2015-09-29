#!/usr/bin/env python3

# -*- coding: utf-8 -*-

# import
import argparse
import os
import subprocess
import csv
import numpy
from collections import defaultdict


# Control argument
def unsigned_int(val):
    val = int(val)
    if val < 0:
        raise argparse.ArgumentTypeError("You can't use signed value")

    return val


def isdir(val):
    val = str(val)
    if not os.path.isdir(val):
        raise argparse.ArgumentTypeError("We need "+val+" is a directory")

    return val


# Main function
def main():

    parser = argparse.ArgumentParser(prog="run",
                                     description="Run bench_rev_comp")
    parser.add_argument("-o", "--output", type=str, help="output prefix",
                        required=True)
    parser.add_argument("-i", "--input", type=str,
                        help="csv file content list of sequence")
    parser.add_argument("-n", "--nb-call", type=unsigned_int,
                        help="Number of repeat run for calculate mean",
                        default=10)
    parser.add_argument("-l", "--list-lang", nargs='+', type=isdir,
                        default=["all"], help="List of language you want bench",
                        action='store')
    parser.add_argument("-N", "--nb-of-nuc", type=unsigned_int,
                        help="Each call run on this nucleotide number",
                        default=1000000)

    args = vars(parser.parse_args())

    if not os.path.isfile(args["input"]):
        print("We can't find "+args["input"]+" use data/generate_data.py")

    for lang in args["list_lang"]:
        read_run_store(lang, args["nb_call"], args["output"],
                       args["input"], args["nb_of_nuc"])


def read_run_store(lang, nb_call, output, seq_file, nb_of_nuc):
    all_data = defaultdict(list)
    with open(seq_file) as csvfile:
        seq_reader = csv.DictReader(csvfile)
        for row in seq_reader:
            tmp_dict = run(lang+"/bench", row["seq"], row["gc"], nb_call,
                            nb_of_nuc/len(row["seq"]))
            for k in tmp_dict.keys():
                all_data[k] = tmp_dict[k]

        store(all_data, output, lang, nb_call)

        
def run(bin_path, seq, gc, nb_call, nb_repeat):
    ret = defaultdict(list)
    for i in range(nb_call):
        result = subprocess.Popen([bin_path, str(nb_repeat), str(seq)],
                                  stdout=subprocess.PIPE,
                                  universal_newlines=True)

        result_reader = csv.DictReader(result.stdout)
        for row in result_reader:
            for algo in row.keys():
                ret[str(len(seq))+"_"+str(gc)+"_"+algo].append(int(row[algo]))

    return ret

def store(result, output, lang, nb_call):
    with open(output+"_"+lang+"_raw.csv", "w") as raw, open(
            output+"_resume.csv", "w") as clean:
        raw.write(",".join(["len", "gc", "algo"] + ["res_"+str(i) for i in
                                                    range(nb_call)]) + "\n")
        clean.write(",".join(["language", "len", "gc", "algo", "mean",
                              "stderror"]) + "\n")
        for len_gc_algo in result:
            (length, gc, algo) = len_gc_algo.split("_")
            raw.write(",".join([length, gc, algo] +
                               [str(i) for i in result[len_gc_algo]]) + "\n")

            mean = numpy.mean(result[len_gc_algo])
            std = numpy.std(result[len_gc_algo]))
            clean.write(",".join([lang, length, gc, algo, str(mean), str(std))
                                 + "\n")

        
if __name__ == '__main__':
    main()