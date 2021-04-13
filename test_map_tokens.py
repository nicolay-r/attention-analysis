from map_tokens import read_lexicon, iter_from_file, process_tokens
from mystem_wrapper import MystemWrapper


def handle(token_positions, vocab_word, vocab_name):
    print(u"{pos} found by vw {vw} - ['{vn}']".format(pos=token_positions, vw=vocab_word, vn=vocab_name))


if __name__ == '__main__':

    stemmer = MystemWrapper()

    tokens = ["ма", "##ма", "вы", "##го", "##ражи", "##вание",
              "за", "что", "##бы", "быть", "спон", "##сором", "глу", "##пышка",
              "выделение", "финансовых" ,"средств",
              "все", '#', 's', '#']

    ordered_vocabs = {
        'sent': set(read_lexicon("data/rusentilex.csv", stemmer)),
        'a0-a1': set(iter_from_file("data/rusentiframes_a0_to_a1.txt", stemmer))
    }

    # Register completed words in vocabulary.
    entries_stat = process_tokens(
            tokens=tokens,
            vocabs=ordered_vocabs,
            handle=handle,
            mystem=stemmer)

    # Stat
    print(entries_stat)
