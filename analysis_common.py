import pickle

import numpy as np
import seaborn as sns


sns.set_style("darkgrid")

layers = 2
heads = 2


def load_pickle(fname):
    with open(fname, "rb") as f:
        return pickle.load(f)  # add, encoding="latin1") if using python3 and downloaded data


def data_iterator():
    for i, doc in enumerate(data):
        if i % 100 == 0 or i == len(data) - 1:
            print("{:.1f}% done".format(100.0 * (i + 1) / len(data)))
        yield doc["tokens"], np.array(doc["attns"])


def get_data_points(head_data):
    xs, ys, avgs = [], [], []
    for layer in range(layers):
        for head in range(layers):
            ys.append(head_data[layer, head])
            xs.append(1 + layer)
        avgs.append(head_data[layer].mean())
    return xs, ys, avgs


data = load_pickle("unlabeled_attn.pkl")
n_docs = len(data)
