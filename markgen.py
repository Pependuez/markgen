# -*- coding: utf-8 -*-

# import argparse
import re
# import pickle
# import json
import subprocess
import sys
import os
import random


class Learner:
    def __init__(self, sources, order, output_file):
        self.sources = sources
        self.chain = {}
        self.order = order
        self.filename = output_file

    def learn(self):
        for file_url in self.sources:
            self.add_file_to_chain(file_url)
        self.save_chain(self.chain, self.filename)

    def add_file_to_chain(self, file_url):
        words = self.read_words(file_url)
        for index in range(self.order, len(words)):
            segment = tuple(words[(index - self.order): index])
            word = words[index]
            if segment not in self.chain:
                self.chain[segment] = [word]
            else:
                if word not in self.chain[segment]:
                    self.chain[segment].append(word)

    def read_file(self, file_url):
        cmdline = ["curl %s" % (file_url)]
        cmd = subprocess.Popen(
            cmdline, stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        result, errors = cmd.communicate()
        return result

    def read_words(self, file_url):
        regex = re.compile('[^a-z0-9$]')
        text = self.read_file(file_url).lower()
        words = [word for word in regex.sub(' ', text).split()]
        return words

    def save_chain(self, obj, filename):
        file = open(filename, 'w+')
        for key in obj:
            print "%s : %s" % (key, obj[key])
            file.write("%s%s\n" % (key, obj[key]))


class ChainUser:
    def __init__(self, chain_file, length, words):
        self.order = 0
        self.filename = chain_file
        print "Words: ", words
        self.phrase = words  # .split(' ')
        self.length = length
        self.chain = {}

    def get_chain(self):
        print "Reading chain from file..."
        with open(self.filename, 'r+') as file:
            for line in file:
                regex_key = re.compile('\((.+)\)\[')
                regex_value = re.compile('\)\[(.+)\]')

                key = tuple(re.sub("'", "", re.search(
                        regex_key, line).group(1)).split(", "))

                # print "Key: ", key

                value = list(re.sub("'", "", re.search(
                    regex_value, line).group(1)).split(", "))

                # print "Value: ", value
                self.chain[key] = value
                self.order = len(self.chain.keys()[0])
            print "Chain length: ", len(self.chain)
            print "Order: ", self.order

    def next_words(self):
        search_key = tuple(self.phrase[-self.order:])
        return self.chain[search_key]

    def construct_phrase(self):
        while len(self.phrase) < self.length:
            next_word = random.choice(self.next_words())
            self.phrase.append(next_word)
            sys.stdout.write(', %s' % (self.phrase[-1]))
        # return self.phrase

    def find_result(self):
        print "finding..."
        sys.stdout.write('Result sequence: %s' % (self.phrase))
        self.construct_phrase()

    def process_phrase(self):
        if len(self.phrase) == self.order:
            print "processing..."
            self.find_result()
        elif len(self.phrase) > self.order:
            self.check_first_words()
            self.find_result()
        else:
            self.phrase = self.expand_phrase()
            self.find_result()

    def check_first_words(self):
        if tuple(self.phrase[:self.order]) in self.chain:
            counter = 0
            length = len(self.phrase)
            order = self.order
            while counter < length - order:
                word = self.phrase[order+counter]
                key = tuple(self.phrase[counter:(order+counter)])
                if word not in self.chain[key]:
                    self.cant_find()
                counter += 1
        else:
            self.cant_find()

    def cant_find(self):
        sys.exit('There are no such sequence.')

    def expand_phrase(self):
        for key in self.chain:
            if key[:len(self.phrase)] == tuple(self.phrase):
                return list(key)


def get_sources(filename):
    sources = []
    file = open(filename, 'r')
    for line in file:
        sources.append(line.rstrip())
    file.close
    return sources


def handle_args(args):
    print args
    if len(args) == 1:
        print "HELP!"
    elif args[1] == "-l":
        print "LEARN!"
        source = get_sources(args[2])
        order = int(args[3])
        output = args[4]
        l = Learner(source, order, output)
        l.learn()
    elif args[1] == "-u":
        print "USE!"
        chain_file = args[2]
        length = int(args[3])
        words = args[4:]
        u = ChainUser(chain_file, length, words)
        u.get_chain()
        u.process_phrase()
    else:
        print "HELP!!!!"

handle_args(sys.argv)


# def save_chain(obj, filename):
#     with open(filename, 'w') as file:
#         pickle.dump(obj, file, 0)
#         # pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

# def load_obj(filename):
#     with open(filename, 'r') as file:
#         return pickle.load(file)

# class Sources:
#     def __init__(self, filename):
#         self.filename = filename

#     def get_sources(self):
#         sources = []
#         current_directory = os.path.dirname(os.path.realpath(__file__))
#         print "Pwd: ", current_directory
#         file = open(filename, 'r')
#         for line in file:
#             sources.append(line.rstrip())
#         print sources
#         file.close
#         return sources

#     # def get_sources(self):
#     #     sources = []
#     #     config_file = open(self.filename, "r")
#     #     for line in config_file:
#     #         sources.append(line)
#     #     config_file.close()
#     #     return sources


# class Learner:
#     def __init__(self, sources, order, filename):
#         self.sources = sources
#         self.chain = {}
#         self.order = order
#         self.filename = filename

#     def learn(self):
#         for file_url in self.sources:
#             self.add_file_to_chain(file_url)
#         save_chain(self.chain, filename)

#     def add_file_to_chain(self, file_url):
#         words = self.read_words(file_url)
#         # chains = {}
#         for index in range(self.order, len(words)):
#             segment = tuple(words[(index - order) : index])
#             # print "Segment: ", segment
#             word = words[index]
#             # print "Word: ", word
#             if segment not in self.chain:
#                 self.chain[segment] = [word]

#                 # print "Segment not in chain yet, creating it: ",
#                       self.chain[segment]
#             else:
#                 if word not in self.chain[segment]:
#                     self.chain[segment].append(word)
#                 # print "Segment already in chain: ", self.chain[segment]

#     def read_file(self, file_url):
#         cmdline = ["curl %s" % (file_url)]
#         cmd = subprocess.Popen(
#             cmdline, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE, shell=True)
#             result, errors = cmd.communicate()
#         # if errors: raise Exception(errors)
#         return result

#     def read_words(self, file_url):
#         regex = re.compile('[^a-z0-9$]')
#         text = self.read_file(file_url).lower()
#         words = [word for word in regex.sub(' ', text).split()]
#         # for word in words: print word
#         return words

# class ChainUser:
#     def __init__(self, file):
#         self.chain = load_obj(file)
#         print self.chain


# # handle_args(sys.argv)
# def confini(args):
#     if len(args) == 1:
#         print "HELP!"
#     elif args[1] == "-l":
#         print "LEARN!"
#         get_sources(args[2])
#     elif args[1] == "-u":
#         print "USE!"
#     else:
#         print "HELP!!!!"

# confini(sys.argv)


# Example: http://textfiles.com/adventure/221baker.txt


# order = 2
# l = Learner(["http://textfiles.com/adventure/221baker.txt",
#     "http://textfiles.com/100/anonymit",
#     "http://textfiles.com/programming/archives.txt"], order)
# l = Learner(["http://textfiles.com/sf/apf-6.0"], order)
# l = Learner(["http://norvig.com/big.txt"], order)

# l.learn()
# c = ChainUser("markov.cnf")
# tt = l.read_words("http://textfiles.com/adventure/221baker.txt")
# for word in tt:

#     print word

# print "Total: %s words" % (len(tt))
# s = Sources("config.cnf")
# print s.get_sources()

# def download_files(source):
#     filenames=[]
#     return filenames

# def add_file_to_chains(files):
#     pass

# def learn(files):
#     for file in files:
#         add_file_to_chains(file)

# def confini():
#     if len(sys.argv) == 1:
#         print "HELP!!!"
#     elif sys.argv[1] == "-l":
#         print "Learn!"
#         print "Links to text file name: ", sys.argv[2]
#         print "Order: ", sys.argv[3]
#         print "Output file name: ", sys.argv[4]
#         sources = Sources(sys.argv[2])
#         order = sys.argv[3]
#         filename = sys.argv[4]
#         l = Learner(sources.get_sources(), order, filename)
#         l.learn()
#     elif sys.argv[1] == "-u":
#         print "Use!"
#         print "Links file: ", sys.argv[2]
#         print "Order: ", sys.argv[3]
#         print "Dictum length: ", sys.argv[4]
#     else:
#         print "ERROR!!!"

# def get_sources(filename):
#     sources = []
#     current_directory = os.path.dirname(os.path.realpath(__file__))
#     print "Pwd: ", current_directory
#     file = open(filename, 'r')
#     for line in file:
#         sources.append(line.rstrip())
#     print sources
#     file.close
#     return sources

# def handle_args(args):
#     print args
#     if len(args) == 1:
#         print "HELP!"
#     elif args[1] == "-l":
#         print "LEARN!"
#         get_sources(args[2])
#     elif args[1] == "-u":
#         print "USE!"
#     else:
#         print "HELP!!!!"


# import sys
# import os

# def get_sources(filename):
#     sources = []
#     # current_directory = os.path.dirname(os.path.realpath(__file__))
#     # print "Pwd: ", current_directory
#     file = open(filename, 'r')
#     for line in file:
#         sources.append(line.rstrip())
#     print sources
#     file.close
#     return sources

# def handle_args(args):
#     print args
#     if len(args) == 1:
#         print "HELP!"
#     elif args[1] == "-l":
#         print "LEARN!"
#         get_sources(args[2])
#     elif args[1] == "-u":
#         print "USE!"
#     else:
#         print "HELP!!!!"

# handle_args(sys.argv)


# def get_data(self):
#     cmdline = ["cmd", "/q", "/k", 'diskpart /s %s' % (self.filename)]
#    cmd = subprocess.Popen(
#       cmdline, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
#       stderr=subprocess.PIPE, shell=True)
#       result, errors = cmd.communicate()
#    if errors: raise Exception(errors)
#    return result

# script_file = open(self.filename, "w+")
# for command in commands:
#     script_file.write('%s\n' % (command))
