from pymystem3 import Mystem


class MystemWrapper(object):
    """ Yandex MyStem wrapper
        part of speech description:
        https://tech.yandex.ru/mystem/doc/grammemes-values-docpage/
    """

    def __init__(self, entire_input=True):
        """
        entire_input: bool
            Mystem parameter that allows to keep all information from input (true) or
            remove garbage characters
        """
        self.__mystem = Mystem(entire_input=entire_input)

    # region properties

    @property
    def MystemInstance(self):
        return self.__mystem

    # endregion

    # region public methods

    def lemmatize_to_list(self, text):
        return self.__lemmatize_core(text)

    def lemmatize_to_str(self, text):
        result = u" ".join(self.__lemmatize_core(text))
        return result if len(result) != 0 else self.__process_original_text(text)

    @staticmethod
    def filter_whitespaces(terms):
        return [term.strip() for term in terms if term.strip()]

    # endregion

    # region private methods

    def __lemmatize_core(self, text):
        result_list = self.__mystem.lemmatize(self.__process_original_text(text))
        return self.filter_whitespaces(result_list)

    @staticmethod
    def __process_original_text(text):
        return text.lower()

    # endregion
