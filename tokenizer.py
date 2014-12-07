import sys
import argparse
from collections import Counter


#### This file defines the TweetTokenizer class, which is intended to parse
#### POS Tweet files into sentence/tweet tokens, containing word-tag tokens.



class TweetTokenizer:

  def __init__(self, filename):
    self.filename = filename
    self.sentence_list = []         # list of sentences, where each sentence is a tuple containing a (word, tag) tuple sequence

    self.word_counter = Counter()   # Counts words in sentence list
    self.tag_counter = Counter()    # Counts tags in sentence list

  def tokenize(self):
    """
    Populates TweetTokenizer's sentence_list, word_counter, and tag_counter
    :return: None
    """
    input_file = open(self.filename)

    reading_sentence = False
    current_sentence = []

    for line in input_file:
      line = line.strip()

      if line == '':
        if reading_sentence:    # just ended reading a sentence
          reading_sentence = False
          self.add_sentence(current_sentence)
          current_sentence = []
        continue

      reading_sentence = True
      token = line.split('\t')
      
      if len(token) < 2:
        token.append('')

      word = token[0]
      tag = token[1]

      self.word_counter[word] += 1
      self.tag_counter[tag] += 1

      current_sentence.append((word, tag))

    ## End of File

    if len(current_sentence) > 0:   # last line in file was not empty
      self.add_sentence(current_sentence)

  def add_sentence(self, token_sentence):
    sequence = tuple(token_sentence)
    self.sentence_list.append(sequence)

  def total_words(self):
    return sum(self.word_counter.values())

  def total_tags(self):
    return sum(self.tag_counter.values()) - self.tag_counter['']

  def total_sentences(self):
    return len(self.sentence_list)


if __name__ == "__main__":
  sys.stdout.write("\n\n----- Beginning Tokenize -----\n\n")

  parser = argparse.ArgumentParser()

  parser.add_argument("-i", dest="input_filename", type=str, help="input tweetfile to be tokenized")

  args = parser.parse_args()

  tokenizer = TweetTokenizer(args.input_filename)
  tokenizer.tokenize()

  sys.stdout.write("\n\n----- Finished Tokenize -----\n\n")
