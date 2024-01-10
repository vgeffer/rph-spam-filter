def read_classification_from_file(file):

    with open(file, "rt", encoding="utf-8") as f:
        out_tags = dict()
        lines = f.readlines()
        for line in lines:
           key = line.strip().split()[0]
           tag = line.strip().split()[1]
           out_tags[key] = tag
        return out_tags

def get_usage_frequencies(words, freqs):
    for word in words:
        if (not word in freqs):
            freqs[word] = 0;
        freqs[word] += 1
    return freqs
