# -*- coding: utf-8 -*-


class WordFromTokens:

    def __init__(self, token, pos):
        assert(isinstance(token, str))
        assert(isinstance(pos, int))
        self.__tokens = [token]
        self.__positions = [pos]

    @property
    def Pos(self):
        return self.__positions

    def get_word(self):
        return "".join([t[2:] if WordFromTokens.is_inner(t) else t
                        for t in self.__tokens])

    def append(self, token):
        assert(WordFromTokens.is_inner(token))
        self.__tokens.append(token)
        self.__positions.append(self.__positions[-1] + 1)

    @staticmethod
    def is_inner(token):
        if len(token) < 2:
            return False

        return token[0] == token[1] == "#"


class ContextWordWindow:

    def __init__(self):
        self.__wft_list = []

    def __clear_seq(self):
        self.__wft_list = []

    def __iter__(self):
        return iter(self.__wft_list)

    def list_len(self):
        return len(self.__wft_list)

    def add_token(self, token, pos):
        assert(isinstance(token, str))
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

        # appending a new token.
        new_token = WordFromTokens(token=token, pos=pos)
        self.__wft_list.append(new_token)

    def try_get_indices_if_matched(self, phrase, retrieve=True):
        words = phrase.split(' ')

        # words won't enough
        if len(self.__wft_list) < len(words):
            return None

        wft_to_match = self.__wft_list[:len(words)]

        matched_result = [wft_to_match[ind].get_word() == words[ind]
                          for ind in range(len(wft_to_match))]

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

    def compose_from_first(self, k):

        # pick the related part.
        wft_part = self.__wft_list[:k]

        # compose phrase.
        phrase = " ".join([w.get_word() for w in wft_part])

        # compose token positions list.
        positions = []
        for w in wft_part:
            positions.extend(w.Pos)

        return phrase, positions


def process_tokens(tokens, vocabs, handle=None, k=6):
    assert(isinstance(vocabs, dict))

    cww = ContextWordWindow()

    for position, token in enumerate(tokens):
        cww.add_token(token=token, pos=position)

    entries_stat = {}
    for vocab_name in vocabs.keys():
        entries_stat[vocab_name] = 0

    while cww.list_len() > 0:
        is_matched = False
        for w_count in reversed(range(k)):
            phrase, positions = cww.compose_from_first(w_count)
            for vocab_name, vocab in vocabs.items():
                if phrase.lower() in vocab:
                    if handle is not None:
                        handle(positions, phrase, vocab_name)
                    entries_stat[vocab_name] += 1
                    break
            if is_matched:
                break

        # Force remove the last token if nothing was matched.
        if not is_matched:
            cww.del_last()

    return entries_stat


def iter_from_file(filepath):
    with open(filepath, 'r') as f:
        for line in f.readlines():
            yield line.strip()


def read_lexicon(filepath):
    l = []
    for line in iter_from_file(filepath):
        w = line.split(u',')[0]
        l.append(w)
    return l

