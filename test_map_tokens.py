from map_tokens import read_lexicon, iter_from_file, process_tokens


def handle(token_positions, vocab_word, vocab_name):
    print(u"{pos} found by vw {vw} - ['{vn}']".format(pos=token_positions, vw=vocab_word, vn=vocab_name))


if __name__ == '__main__':

    tokens = ["ма", "##ма", "вы", "##го", "##ражи", "##вание",
              "за", "что", "##бы", "все", '#', 's', '#']

    ordered_vocabs = {
        'sent': set(read_lexicon("data/rusentilex.csv")),
        'a0-a1': set(iter_from_file("data/rusentiframes_a0_to_a1.txt"))
    }

    # Register completed words in vocabulary.
    process_tokens(tokens=tokens, vocabs=ordered_vocabs, handle=handle)
