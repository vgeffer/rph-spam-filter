from corpus import Corpus
from trainingcorpus import TrainingCorpus
from utils import get_usage_frequencies
from math import log

ALPHA = 1

class MyFilter:
    
    def __init__(self):

        # Naive-Bayes lists
        self.ham_vocab = list()
        self.spam_vocab = list()

        self.ham_word_freq = dict()
        self.spam_word_freq = dict()

        # Naive-Bayes statistical params (precomputed for speed)
        self.ham_words_total = 0
        self.spam_words_total = 0
        self.len_total = 0

        self.p_ham = 0
        self.p_spam = 0

        self.vocab_len = 0

    def train(self, train_data_dir):

        corpus = TrainingCorpus(train_data_dir)
        for email in corpus.get_emails():
        
            words = corpus.get_email_words(email)
            self.len_total += len(words)

            tag = corpus.get_class(email["filename"])
            if tag == 'OK':
                self.ham_vocab += words
                self.ham_words_total += len(words)
                self.ham_word_freq = get_usage_frequencies(words, self.ham_word_freq)
            else:
                self.spam_vocab += words
                self.spam_words_total += len(words)
                self.spam_word_freq = get_usage_frequencies(words, self.spam_word_freq)

        self.ham_vocab = list(set(self.ham_vocab))
        self.spam_vocab = list(set(self.spam_vocab))
        
        self.vocab_len = len(self.ham_vocab) + len(self.spam_vocab)

    def test(self, class_data_dir):
        
        # If model hasn't been prepared, exit imideatly
        if self.len_total == 0:
            return

        corpus = Corpus(class_data_dir)
        tags = dict()

        for email in corpus.get_emails():

            prob_ham = log(self.ham_words_total / self.len_total)
            prob_spam = log(self.spam_words_total / self.len_total)

            for word in corpus.get_email_words(email):    

                # Multinomial Naive-Bayes, logarithms used (so we don't converge to something rapidly, but slowly) 
                word_occurences_spam = self.spam_word_freq.get(word, 0)
                word_occurences_ham = self.ham_word_freq.get(word, 0)
                
                w_spam = log((word_occurences_spam + ALPHA) / (self.spam_words_total + ALPHA * self.vocab_len))
                w_ham = log((word_occurences_ham + ALPHA) / (self.ham_words_total + ALPHA * self.vocab_len))
                
                prob_ham += w_ham
                prob_spam += w_spam

                tags[email["filename"]] = ("SPAM" if prob_ham < prob_spam else "OK")
        corpus.write_predicted_tags(tags)