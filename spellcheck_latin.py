#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os, sys, re, getopt, io, argparse, subprocess

parser = argparse.ArgumentParser(description="", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-f", "--file", help="Input file")
parser.add_argument("-t", "--text", action="store_true", help="Plain text")
parser.add_argument("-g", "--gabc", action="store_true", help="GABC file")
parser.add_argument("-l", "--latex", action="store_true", help="LaTeX file")
parser.add_argument("-li", "--latexinput", action="store_true", help="LaTeX module file")
args = parser.parse_args()

if args.text == True:
  filetype = "text"
if args.gabc == True:
  filetype = "gabc"
if args.latex == True:
  filetype = "latex"
if args.latexinput == True:
  filetype = "latexinput"

filename = args.file
output = open('output.text', 'w')
script_dir = sys.path[0]
dict_file = script_dir + "/listall.txt"
dict_file_custom = script_dir + "/extras.txt"

num_of_lines = subprocess.getoutput("less " + filename + " | wc --lines")
num_of_lines = re.sub('\n','',num_of_lines)

if filetype == "text" or filetype == "latexinput":
  preamble = 0
else:
  preamble = 1

#Import Latin wordlist
latin_dict = []
with open(dict_file, 'r') as dictfile:
  for line in dictfile:
    curr_place = line[:-1]
    curr_place = curr_place.lower()
    latin_dict.append(curr_place)
with open(dict_file_custom, 'r') as dictfile2:
  for line in dictfile2:
    curr_place = line[:-1]
    curr_place = curr_place.lower()
    latin_dict.append(curr_place)

#Import words from file to be checked
#TODO eliminate HTML tags and euouae
line_number = 1
spellcheck_list = []
spelling = open(filename, 'r')
header = 1
for line in spelling:
  if preamble == 1:
    if filetype == "gabc":
      if "%%" in line:
        preamble = 0
      else:
        continue
    if filetype == "latex":
      if "begin{document}" in line:
        preamble = 0
      else:
        continue
  inline = line
  inline = re.sub('\n','',inline)
  if filetype == "latex" or filetype == "latexinput":
    #inline = re.sub('\\\\[^ {]*[ {]','',inline)
    #inline = re.sub('}','',inline)
    inline = re.sub('%.*$','',inline)
    inline = re.sub('\\\\[^ \[]*\[[^\]]*\][^{]*{[^}]*}','',inline)
    inline = re.sub('\\\\[^ {]*{[^}]*}','',inline)
    inline = re.sub('\\\\[^ ]* ',' ',inline)
    inline = re.sub('\\\\[^ ]*$',' ',inline)
  if filetype == "gabc":
    inline = re.sub('\([^\)]*\)','',inline)
    inline = re.sub('<[^>]*>','',inline)
  inline = re.sub('á','a',inline)
  inline = re.sub('é','e',inline)
  inline = re.sub('í','i',inline)
  inline = re.sub('ó','o',inline)
  inline = re.sub('ú','u',inline)
  inline = re.sub('ý','y',inline)
  inline = re.sub('ë','e',inline)
  inline = re.sub('æ','ae',inline)
  inline = re.sub('Æ','AE',inline)
  inline = re.sub('œ','oe',inline)
  inline = re.sub('Œ','OE',inline)
  inline = re.sub('ǽ','ae',inline)
  inline = re.sub('Ǽ','AE',inline)
  inline = re.sub('œ́','oe',inline)
  inline = re.sub('Œ́','OE',inline)
  words = inline.split(" ")
  words = list(filter(None, words))
  word_number = 1
  for i in words:
    i = i.lower()
    i = re.sub('[^a-z]','',i)
    spellcheck_list.append(i)
    if i not in latin_dict:
      output.write("line " + str(line_number) + " word " + str(word_number) + ": " + i + "\n")
    word_number = word_number + 1
  sys.stdout.write("\rProcessing line " + str(line_number) + "/" + num_of_lines)
  sys.stdout.flush()
  line_number = line_number+1

#Output unique fails
def get_difference(list_a, list_b):
  non_match_b  = set(list_b)-set(list_a)
  non_match = list(non_match_b)
  return non_match
non_match = list(get_difference(latin_dict, spellcheck_list))
output.write("\n\nUnique words not matching:\n")
output.write(str(non_match))

output.close()
dictfile.close()
spelling.close()
