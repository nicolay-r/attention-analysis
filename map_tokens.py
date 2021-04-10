# -*- coding: utf-8 -*-

class WordFromTokens:

    def __init__(self, token, pos):
        assert(isinstance(token, unicode))
        assert(isinstance(pos, int))
        self.__tokens = [token]
        self.__positions = [pos]

    @property
    def Pos(self):
        return self.__positions

    def get_word(self):
        return "".join([t[2:] if WordFromTokens.is_inner(t) else t for t in tokens])

    def append(self, token):
        assert(WordFromTokens.is_inner(token))
        self.__tokens.append(token)
        self.__positions.append(self.__positions[-1] + 1)

    @staticmethod
    def is_inner(token):
        return token[0] == token[1] == "#"


class ContextWordWindow:

    def __init__(self, max_seq_len=5):
        self.__wft_list = []
        self.__max_seq_len = max_seq_len

    def __clear_seq(self):
        self.__wft_list = []

    def list_len(self):
        return len(self.__wft_list)

    def add_token(self, token, pos):
        assert(isinstance(token, unicode))
        assert(isinstance(pos, int))

        # When list is empty.
        if len(self.__wft_list) == 0:
            self.__wft_list.append(WordFromTokens(token=token, pos=pos))
            return

        wft_last = self.__wft_list[-1]

        # complete the last existed.
        if WordFromTokens.is_inner(token):
            wft_last.append(token)
            return

        # buffer is full -- releasing the first element from it.
        if len(self.__wft_list) == self.__max_seq_len:
            self.__wft_list = self.__wft_list[1:]

        # appending a new token.
        self.__wft_list.append(WordFromTokens(token=token, pos=pos))

    def try_get_indices_if_matched(self, phrase, retrieve=True):
        assert(isinstance(phrase, unicode))
        words = phrase.split(' ')

        # words won't enough
        if len(self.__wft_list) < len(words):
            return None

        wft_to_match = self.__wft_list[:len(words)]

        matched_result = [wft_to_match[ind].get_word() == words[ind] for ind in range(len(wft_to_match))]

        for r in matched_result:
            if r is False:
                return None

        token_inds = []
        for wft in wft_to_match:
            for p_ind in wft.Pos:
                token_inds.append(p_ind)

        # Update the wft_list after we pick the existed result.
        if retrieve:
            self.__wft_list = self.__wft_list[len(words):]

        return token_inds

    def del_last(self):
        self.__wft_list = self.__wft_list[1:]


#########################################
# TEST
#########################################



def process_tokens(tokens, vocabs, handle):
    # NOTE: in vocabs everything should be ordered by decreasing length.

    for position, token in enumerate(tokens):
        cww.add_token(token=token, pos=position)

    while (cww.list_len() > 0):
        is_matched = False
        for index, vocab in enumerate(vocabs):
            for vocab_word in vocab:
                positions = cww.try_get_indices_if_matched(phrase=vocab_word)

                if positions is None:
                    continue

                handle(positions, vocab_word, index)
                is_matched = True
                break
            if is_matched:
                break

        # Force remove the last token if nothing was matched.
        if not is_matched:
            cww.del_last()


match_list = [u"мама"]
tokens = [u"ма", u"##ма", u"не", u"за", u"что", u"##бы"]

def handle(token_positions, vocab_word, vocab_index):
    print u"{pos} found by vw {vw} - [{vi}]".format(pos=token_positions, vw=vocab_word, vi=vocab_index)

# Register completed words in vocabulary.
cww = ContextWordWindow(5)
process_tokens(tokens=tokens, vocabs=[match_list],
               handle=lambda pos, vw, vi: handle(pos, vw, vi))
