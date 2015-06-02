# -*- coding: utf-8 -*-

# В решении не стоит делать что-то сложное или хитрое. Например, всякие сложные матрицы
# и уравнения из статьи - они немного про другое.
# Тут всё можно сделать базовыми средствами Питона, которые ты уже знаешь.

# Требуется построить марковcкий генератор текстов n-го порядка (http://ru.wikipedia.org/wiki/Цепь_Маркова). Логически состоит из
# двух компонент - обучающей и эксплуатирующей.

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

import argparse
import re
# import os
import subprocess

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

class Sources:
    def __init__(self, config):
        self.config = config

    def get_sources(self):
        sources = []
        config_file = open(self.config, "r")
        for line in config_file:
            sources.append(line)
        script_file.close()
        return sources

class Learner:
    def __init__(self, sources):
        self.sources = sources
        self.chain = {}

    def learn(self):
        for file_url in self.sources:
            add_file_to_chain(file_url)

    def add_file_to_chain(self, file_url):
        words = read_words(file_url)
        pass

    def read_file(self, file_url):
        cmdline = ["curl %s" % (file_url)]
        cmd = subprocess.Popen(cmdline, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        result, errors = cmd.communicate()
        # if errors: raise Exception(errors)
        return result

    def read_words(self, file_url):
        regex = re.compile('[^a-z0-9$]')
        text = self.read_file(file_url).lower()
        return [regex.sub('', word) for word in text.split()]
        # return [word for word in text.split()]

    # def write_data:
    #     pass

l = Learner(["http://textfiles.com/adventure/221baker.txt"])
tt = l.read_words("http://textfiles.com/adventure/221baker.txt")
for word in tt:
    print word

print "Total: %s words" % (len(tt))
s = Sources("config.cnf")
print s.get_sources()

# def download_files(source):
#     filenames=[]
#     return filenames

# def add_file_to_chains(files):
#     pass

# def learn(files):
#     for file in files:
#         add_file_to_chains(file)
