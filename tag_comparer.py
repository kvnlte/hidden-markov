import argparse
from tokenizer import TweetTokenizer


def compare_tokenized(test_file, ref_file):
  total_sentences = test_file.total_sentences()

  if total_sentences != ref_file.total_sentences():
    raise RuntimeError("Mismatched Files")

  total_matches = 0
  total_words = ref_file.total_words()

  for i in xrange(total_sentences):
    test_sentence = test_file.sentence_list[i]
    ref_sentence = ref_file.sentence_list[i]
    total_matches += count_tag_matches(test_sentence, ref_sentence)

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

  parser.add_argument("-a", dest="filename_a", type=str, help="Filename A")
  parser.add_argument("-b", dest="filename_b", type=str, help="Filename B")

  args = parser.parse_args()

  file_a = TweetTokenizer(args.filename_a)
  file_b = TweetTokenizer(args.filename_b)

  file_a.tokenize()
  file_b.tokenize()

  score, total = compare_tokenized(file_a, file_b)

  print
  print "Found %d matches out of %d words" % (score, total)
  print "Match Percentage: %f %%" % ( (100*float(score)) / total )
  print

