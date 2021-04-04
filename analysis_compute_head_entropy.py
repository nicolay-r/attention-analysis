import numpy as np
from analysis_common import data_iterator, n_docs, heads

uniform_attn_entropy = 0  # entropy of uniform attention
entropies = np.zeros((heads, heads))  # entropy of attention heads
entropies_cls = np.zeros((heads, heads))  # entropy of attention from [CLS]

print("Computing entropy stats")
for tokens, attns in data_iterator():
  attns = 0.9999 * attns + (0.0001 / attns.shape[-1])  # smooth to avoid NaNs
  uniform_attn_entropy -= np.log(1.0 / attns.shape[-1])
  entropies -= (attns * np.log(attns)).sum(-1).mean(-1)
  entropies_cls -= (attns * np.log(attns))[:, :, 0].sum(-1)

uniform_attn_entropy /= n_docs
entropies /= n_docs
entropies_cls /= n_docs