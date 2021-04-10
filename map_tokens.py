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
        return "".join([t[2:] if WordFromTokens.is_inner(t) else t for t in self.__tokens])

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

        # appending a new token.
        new_token = WordFromTokens(token=token, pos=pos)
        self.__wft_list.append(new_token)

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


def process_tokens(tokens, vocabs, handle):
    assert(isinstance(vocabs, dict))
    # NOTE: in vocabs everything should be ordered by decreasing length.

    for position, token in enumerate(tokens):
        cww.add_token(token=token, pos=position)

    while cww.list_len() > 0:
        is_matched = False
        for vocab_name, vocab in vocabs.iteritems():
            for vocab_word in vocab:
                positions = cww.try_get_indices_if_matched(phrase=vocab_word)

                if positions is None:
                    continue

                handle(positions, vocab_word, vocab_name)
                is_matched = True
                break
            if is_matched:
                break

        # Force remove the last token if nothing was matched.
        if not is_matched:
            cww.del_last()


def handle(token_positions, vocab_word, vocab_name):
    print u"{pos} found by vw {vw} - ['{vn}']".format(pos=token_positions, vw=vocab_word, vn=vocab_name)


def order_vocab(vocab):
    return list(reversed(sorted(vocab, key=lambda x: len(x.split(' ')))))


#########################################
# TEST
#########################################
match_list1 = [u"мама", u'чтобы']
match_list2 = [u"s"]
tokens = [u"ма", u"##ма", u"не", u"за", u"что", u"##бы", u"все", u'#', u's', u'#']
vocabs = [match_list1]
ordered_vocabs = {
    u'test': order_vocab(match_list1),
    u'subj': order_vocab(match_list2)
}
# Register completed words in vocabulary.
cww = ContextWordWindow()
process_tokens(tokens=tokens, vocabs=ordered_vocabs, handle=handle)
