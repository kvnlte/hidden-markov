import argparse
from tokenizer import TweetTokenizer



#### This script compares two Tweet data files in the given project format and
#### prints the number of tags that match between both files.

#### Note: tokenizer.py is a dependency, and must be in the same directory



def compare_tweet_files(test_filename, ref_filename):

  print 
  print "Comparing %s to %s..." % (test_filename, ref_filename)
  test_file = TweetTokenizer(test_filename)
  ref_file = TweetTokenizer(ref_filename)

  test_file.tokenize()
  ref_file.tokenize()

  total_sentences = test_file.total_sentences()

  if total_sentences != ref_file.total_sentences():
    raise RuntimeError("Mismatched Files")

  total_matches = 0
  total_words = ref_file.total_words()

  for i in xrange(total_sentences):
    test_sentence = test_file.sentence_list[i]
    ref_sentence = ref_file.sentence_list[i]
    total_matches += count_tag_matches(test_sentence, ref_sentence)
  
  print
  print "\tFound %d matches out of %d words" % (total_matches, total_words)
  print "\tMatch Percentage: %f %%" % ( (100*float(total_matches)) / total_words )
  print

  return total_matches, total_words


def count_tag_matches(test_sentence, ref_sentence):
  sentence_length = len(test_sentence)

  if sentence_length != len(ref_sentence):
    raise RuntimeError("Mismatched Sentences")

  match_count = 0

  for i in xrange(sentence_length):
    test_word, test_tag = test_sentence[i]
    ref_word, ref_tag = ref_sentence[i]
    if test_word != ref_word:
      raise RuntimeError("Mismatched Sentences")
    if test_tag == ref_tag:
      match_count += 1

  return match_count
    
###############################################################################


if __name__ == "__main__":
  parser = argparse.ArgumentParser()

  parser.add_argument("-i", dest="input_filename", type=str, help="Input Filename")
  parser.add_argument("-r", dest="reference_filename", type=str, help="Reference Filename")

  args = parser.parse_args()

  score, total = compare_tweet_files(args.input_filename, args.reference_filename)

  
