# -*- coding: utf-8 -*-
from __future__ import print_function
import re
import subprocess
import sys
import random
try:
    import cPickle as pickle
except:
    import pickle


class Learner(object):
    def __init__(self, sources, order, output_file):
        self.sources = sources
        self.chain = {}
        self.order = order
        self.filename = output_file

    def learn(self):
        print("Reading file(s)...")
        for file_url in self.sources:
            self.add_file_to_chain(file_url)
        self.save_chain()

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

    def save_chain(self):
        with open(self.filename, 'w+') as chain_file:
            pickle.dump(self.chain, chain_file, pickle.HIGHEST_PROTOCOL)


class ChainUser(object):
    def __init__(self, chain_file, length, words):
        self.order = 0
        self.filename = chain_file
        self.phrase = [word.lower() for word in words]
        self.length = length
        self.chain = {}

    def get_chain(self):
        print("Reading chain from file...")
        with open(self.filename) as chain_file:
            self.chain = pickle.load(chain_file)
            self.order = len(self.chain.keys()[0])

    def next_words(self):
        key = tuple(self.phrase[-self.order:])
        if key in self.chain:
            return self.chain[key]
        else:
            print(".\n\nInterrupted. No more words in sequence.")
            print("Current sequence length: %s words" % (len(self.phrase)))
            sys.exit()

    def construct_phrase(self):
        while len(self.phrase) < self.length:
            next_word = random.choice(self.next_words())
            self.phrase.append(next_word)
            print(' %s' % (self.phrase[-1]), end='')
        print(".")

    def find_result(self):
        print("Finding words...")
        print('Result sequence: %s' % (' '.join(self.phrase)), end='')
        self.construct_phrase()

    def process_phrase(self):
        print("Processing...")
        if len(self.phrase) == self.order:
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
    with open(filename, 'r+') as file:
        for line in file:
            sources.append(line.rstrip())
    return sources


def print_help():
    help_string = '''Usage:
    Learn mode:
        python markgen.py -l urls_file chain_order chain_file
            -l - flag for learn mode (building Markov's chain and save it to file)
            urls_file - file with urls to text files (string)
            chain_order - Markov's chain order (integer)
            chain_file - file to wite Markov's chain (string)

    Use mode:
        python markgen.py -u chain_file phrase_length word1 dord2 ...
            -u - flag for use mode (read Markov's chain from file and build phrase)
            chain_file - file with prebuilded Markov's chain (string)
            phrase_length - number of words in output sentence (integer)
            word1, word2, etc. - first words of output sentence (stings)'''
    print(help_string)


def handle_args(args):
    if len(args) == 1:
        print_help()
    elif args[1] == "-l":
        source = get_sources(args[2])
        order = int(args[3])
        output = args[4]
        l = Learner(source, order, output)
        l.learn()
        print("Done.")
    elif args[1] == "-u":
        chain_file = args[2]
        length = int(args[3])
        words = args[4:]
        u = ChainUser(chain_file, length, words)
        u.get_chain()
        u.process_phrase()
    else:
        print_help()

handle_args(sys.argv)
