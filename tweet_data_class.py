class TweetData():
  
  def __init__(self, sequence):
    """
    Returns new instance of the TweetData class.

    :param sequence: should be a list of tuples, containing word-tag pairs
    :return:
    """
    assert isinstance(sequence, list) or isinstance(sequence, tuple)

    self.sequence = tuple(pair for pair in sequence)    # keep things immutable
    self.length = len(sequence)