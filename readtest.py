import sys
import os
import pickle
import re


def get_chain(filename):
    chain = {}
    # current_directory = os.path.dirname(os.path.realpath(__file__))
    # print "Pwd: ", current_directory
    # file = open(filename, 'r')
    # for line in file:
    #     sources.append(line.rstrip())
    # print sources
    # file.close
    # def load_obj(filename):
    # source = []
    with open(filename, 'r+') as file:
        for line in file:
            regex_key = re.compile('\((.+)\)\[')
            regex_value = re.compile('\)\[(.+)\]')
            key = tuple(re.sub("'", "",re.search(regex_key, line).group(1)).split(", "))
            # key = tuple(re.search(regex_key, line).group(1).split(", "))
            print "Key: ", key
            value = list(re.sub("'", "",re.search(regex_value, line).group(1)).split(", "))
            # value = list(re.search(regex_value, line).group(1).split(", "))
            print "Value: ", value
            chain[key] = value
    return chain


def handle_args(args):
    print args
    if len(args) == 1:
        print "HELP!"
    elif args[1] == "-l":
        print "LEARN!"
        get_sources(args[2])
    elif args[1] == "-u":
        print "USE!"
        filename = args[2]
        chain = get_chain(filename)
        for key in chain:
            print chain[key]
    else:
        print "HELP!!!!"

handle_args(sys.argv)
