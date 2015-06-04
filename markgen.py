# -*- coding: utf-8 -*-

# В решении не стоит делать что-то сложное или хитрое. Например, всякие сложные матрицы
# и уравнения из статьи - они немного про другое.
# Тут всё можно сделать базовыми средствами Питона, которые ты уже знаешь.

# Требуется построить марковcкий генератор текстов n-го порядка
# (http://ru.wikipedia.org/wiki/Цепь_Маркова).
# Логически состоит из двух компонент - обучающей и эксплуатирующей.

# Обучающей части на вход подается список урлов, ведущих на текстовые
# файлы. Она должна скачать их, вызывая внутри curl и получая от него
# данные через пайп (использовать libcurl не надо, надо просто запустить curl как отдельный процесс). Файлы содержат текст на естественном языке. Для простоты можно обрабатывать только буквы английского языка и цифры. Пунктуацию откидываем, морфологию учитывать не нужно, стоит лишь
# привести текcт к одному регистру, чтобы повысить заполняемость цепи.
# Также задается параметр n - порядок цепи. По входному тексту строится
# марковская цепь, и сохраняется в файл (можно выдавать в стандартный
# вывод).

# Эксплуатирующей части на вход подаются начальный отрывок из n слов и
# число - количество слов, которые надо достроить по начальному отрывку и
# построенной обучающей частью марковской цепи, которую надо загрузить из
# файла. Если в какой-то момент программа не знает какую-то
# последовательность слов (не встречалась при построении марковской цепи),
# то на этом можно построение текста завершить. Вывод надо выдавать в
# поток стандартного вывода. Вход можно принимать как со стандартного
# потока ввода, так и указанием файлов и параметров в командной
# строке, но не хардкодить имена в тексте программы.

# http://textfiles.com/adventure/221baker.txt

# import argparse
import re
import pickle
import subprocess
import sys
import os

# def __get_data(self):
#     cmdline = ["cmd", "/q", "/k", 'diskpart /s %s' % (self.filename)]
#     cmd = subprocess.Popen(cmdline, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
#     result, errors = cmd.communicate()
#     if errors: raise Exception(errors)
#     return result

# script_file = open(self.filename, "w+")
# for command in commands:
#     script_file.write('%s\n' % (command))
# script_file.close()
def save_obj(obj, filename):
    with open(filename, 'w') as file:
        pickle.dump(obj, file, 0)
        # pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(filename):
    with open(filename, 'r') as file:
        return pickle.load(file)

class Sources:
    def __init__(self, filename):
        self.filename = filename

    def get_sources(self):
        sources = []
        current_directory = os.path.dirname(os.path.realpath(__file__))
        print "Pwd: ", current_directory
        file = open(filename, 'r')
        for line in file:
            sources.append(line.rstrip())
        print sources
        file.close
        return sources

    # def get_sources(self):
    #     sources = []
    #     config_file = open(self.filename, "r")
    #     for line in config_file:
    #         sources.append(line)
    #     config_file.close()
    #     return sources


class Learner:
    def __init__(self, sources, order, filename):
        self.sources = sources
        self.chain = {}
        self.order = order
        self.filename = filename

    def learn(self):
        for file_url in self.sources:
            self.add_file_to_chain(file_url)
        save_obj(self.chain, filename)

    def add_file_to_chain(self, file_url):
        words = self.read_words(file_url)
        # chains = {}
        for index in range(self.order, len(words)):
            segment = tuple(words[(index - order) : index])
            # print "Segment: ", segment
            word = words[index]
            # print "Word: ", word
            if segment not in self.chain:
                self.chain[segment] = [word]
                # print "Segment not in chain yet, creating it: ", self.chain[segment]
            else:
                if word not in self.chain[segment]: self.chain[segment].append(word)
                # print "Segment already in chain: ", self.chain[segment]

    def read_file(self, file_url):
        cmdline = ["curl %s" % (file_url)]
        cmd = subprocess.Popen(cmdline, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        result, errors = cmd.communicate()
        # if errors: raise Exception(errors)
        return result

    def read_words(self, file_url):
        regex = re.compile('[^a-z0-9$]')
        text = self.read_file(file_url).lower()
        words = [word for word in regex.sub(' ', text).split()]
        # for word in words: print word
        return words

class ChainUser:
    def __init__(self, file):
        self.chain = load_obj(file)
        print self.chain


# handle_args(sys.argv)
def confini(args):
    if len(args) == 1:
        print "HELP!"
    elif args[1] == "-l":
        print "LEARN!"
        get_sources(args[2])
    elif args[1] == "-u":
        print "USE!"
    else:
        print "HELP!!!!"

confini(sys.argv)



# order = 2
# l = Learner(["http://textfiles.com/adventure/221baker.txt", "http://textfiles.com/100/anonymit", "http://textfiles.com/programming/archives.txt"], order)
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