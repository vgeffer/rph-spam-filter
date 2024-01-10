from confmat import BinaryConfusionMatrix
from filter.utils import read_classification_from_file
from filter.filter import MyFilter
from shutil import copyfile
from os import mkdir, stat
from random import sample
from os.path import join
from time import time
from math import ceil


def quality_score(tp, tn, fp, fn):
    return (tp + tn) / (tp + tn + 10*fp + fn)

def compute_quality_for_corpus(corpus_dir):
    bcm = BinaryConfusionMatrix(pos_tag="SPAM", neg_tag="OK")

    truths = read_classification_from_file(join(corpus_dir, "!truth.txt"))
    preds = read_classification_from_file(join(corpus_dir, "!prediction.txt"))
    bcm.compute_from_dicts(truth_dict=truths, pred_dict=preds)

    return quality_score(bcm.TP, bcm.TN, bcm.FP, bcm.FN)


if __name__ == '__main__':
    dataset_dir = input("Please provide path to dataset: ")
    train_size = float(input("How much of that dataset should be allocated to training? (0 < n < 1): "))
    itters = int(input("How many itterations you wish to do? (0 < n): "))

    avg_quality = 0

    try:
        stat(dataset_dir)
    except:
        print("Invalid dataset path!")
        exit()

    if train_size <= 0 or train_size >= 1:
        print("Invalid training dataset size")
        exit()

    if (itters < 1):
        print("Invalid number of itterations")
        exit()

    for i in range(itters):

        # Get labels of current dataset
        truths = read_classification_from_file(join(dataset_dir, "!truth.txt"))

        hams = [ham[0] for ham in truths.items() if ham[1] == "OK"]
        spams = [spam[0] for spam in truths.items() if spam[1] == "SPAM"]

        train_hams = sample(hams, ceil(len(hams) * train_size))
        train_spams = sample(spams, ceil(len(spams) * train_size))

        verify_hams = [ham for ham in hams if not ham in train_hams]
        verify_spams = [spam for spam in spams if not spam in train_spams]


        # Create dirs
        tmp_dirpath = join('/tmp', 'filter-train-' + str(time()))
        mkdir(tmp_dirpath)
        mkdir(join(tmp_dirpath, "train"))
        mkdir(join(tmp_dirpath, "verify"))

        # Write out !truth.txt files
        with open(join(tmp_dirpath, "train", "!truth.txt"), "wt", encoding="utf-8") as p:
            for tag in train_hams:
                p.write(tag + " " + "OK" + "\n")
            for tag in train_spams:
                p.write(tag + " " + "SPAM" + "\n")


        with open(join(tmp_dirpath, "verify", "!truth.txt"), "wt", encoding="utf-8") as p:
            for tag in verify_hams:
                p.write(tag + " " + "OK" + "\n")
            for tag in verify_spams:
                p.write(tag + " " + "SPAM" + "\n")

        # Copy out files
        for f in [*train_hams, *train_spams]:
            copyfile(join(dataset_dir, f), join(tmp_dirpath, "train", f))
        for f in [*verify_hams, *verify_spams]:
            copyfile(join(dataset_dir, f), join(tmp_dirpath, "verify", f))

        print()
        filter = MyFilter()

        print("(" + str(i + 1) + "/" + str(itters) + ")", "Staritng training")
        filter.train(join(tmp_dirpath, "train"))
        print("Training done, starting verification")
        filter.test(join(tmp_dirpath, "verify"))

        quality = compute_quality_for_corpus(join(tmp_dirpath, "verify"))
        avg_quality += quality
        # Print out quality
        print("Final quality is: ", quality)
    print("All done! Average quality is", str(avg_quality / itters))