

class BinaryConfusionMatrix:

    def __init__(self, pos_tag, neg_tag):
        self.TP = 0
        self.FP = 0
        self.TN = 0
        self.FN = 0
        self.ptag = pos_tag
        self.ntag = neg_tag

    def as_dict(self):
        return {
            "tp": self.TP,
            "fp": self.FP,
            "tn": self.TN,
            "fn": self.FN
        }


    def update(self, truth, pred):
        
        if truth == pred:
            if pred == self.ptag:
                self.TP += 1
            else:
                self.TN += 1
        else:
            if pred == self.ptag:
                self.FP += 1
            else:
                self.FN += 1 

    def compute_from_dicts(self, truth_dict, pred_dict):
        for key in list(truth_dict.keys()):
            if key in pred_dict:
                self.update(truth_dict[key], pred_dict[key])