from finntk.emb.autoextend import vecs as fiwn_vecs, mk_lemma_vec
import numpy as np
from .lesk_emb import MultilingualLesk


class LeskPP:

    def __init__(self, multispace, aggf, wn_filter=False, expand=False):
        self.multispace = multispace
        self.aggf = aggf
        self.wn_filter = wn_filter
        self.expand = expand
        self.ml_lesk = MultilingualLesk(multispace, aggf, wn_filter, expand)

    def mk_defn_vec(self, item):
        return self.ml_lesk.mk_defn_vec(item)

    def mk_ctx_vec(self, sent_lemmas, exclude_idx=None):
        #print("Make ctx vec")
        fiwn_space = fiwn_vecs.get_vecs()

        def gen():
            for lemma_str, lemmas in sent_lemmas:
                yielded = False
                if len(lemmas) == 1:
                    try:
                        #print("Lemma vec", lemmas[0], mk_lemma_vec(lemmas[0]))
                        yield lemma_str, mk_lemma_vec(lemmas[0])
                    except KeyError:
                        pass
                    else:
                        yielded = True
                if not yielded:
                    try:
                        #print("Surface form vec", lemma_str, fiwn_space.get_vector(lemma_str))
                        yield lemma_str, fiwn_space.get_vector(lemma_str)
                    except KeyError:
                        pass

        words, vecs = zip(*gen())
        mat = np.stack(vecs)
        if hasattr(self.aggf, "needs_words"):
            return self.aggf(mat, words, "fi")
        else:
            return self.aggf(mat)
