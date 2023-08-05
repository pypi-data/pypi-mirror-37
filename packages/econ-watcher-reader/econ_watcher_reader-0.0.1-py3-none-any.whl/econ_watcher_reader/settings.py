from enum import Enum

TOP_MENU_PAGE = 'http://www5.cao.go.jp/keizai3/watcher_index.html'
OLD_MENU_PAGE = 'http://www5.cao.go.jp/keizai3/kako_watcher.html'
WATCHER_DISTRIBUTE_DIRECTORY = 'http://www5.cao.go.jp/keizai3/'
TOKYO_FLAG_VALUE_IN_RAW_DATA = '東京都'


class WatcherType(Enum):
    Current = ('watcher4.csv', 2, 1, 0, 3, 4, 5)
    Future = ('watcher5.csv', 2, 1, 0, 3, None, 4)
    CurrentKoshinetsu = ('watcher6.csv', 0, None, 0, 3, 4, 5)
    FutureKoshinetsu = ('watcher7.csv', 0, None, 0, 3, 4, 5)

    def __init__(self,
                 file_name:str,
                 iloc_economic_status_score:int,
                 iloc_is_tokyo_flag: int,
                 iloc_field: int,
                 iloc_industry: int,
                 iloc_reason_type: int,
                 iloc_reason_sentence: int
                 ):
        self.__file_name = file_name
        self.__iloc_economic_status_score = iloc_economic_status_score
        self.__iloc_is_tokyo_flag = iloc_is_tokyo_flag
        self.__iloc_field = iloc_field
        self.__iloc_industry = iloc_industry
        self.__iloc_reason_type = iloc_reason_type
        self.__iloc_reason_sentence = iloc_reason_sentence

    def get_name_from_iloc(self, iloc:int):
        """
        Mapper method to get name from iloc.

        :param int iloc: number of index.
        :return: column name
        """
        if iloc == self.iloc_economic_status_score:
            return 'score'
        elif iloc == self.iloc_is_tokyo_flag:
            return 'is_tokyo'
        elif iloc == self.iloc_field:
            return 'field'
        elif iloc == self.iloc_industry:
            return 'industry'
        elif iloc == self.iloc_reason_type:
            return 'reason_type'
        elif iloc == self.iloc_reason_sentence:
            return 'reason_sentence'
        else:
            return None

    @property
    def score_map(self) ->dict:
        if self in [WatcherType.Current, WatcherType.Future]:
            return {'◎': 4, '○': 3 , '□': 2, '▲': 1, '×': 0}
        elif self in [WatcherType.CurrentKoshinetsu, WatcherType.FutureKoshinetsu]:
            return {} # TODO

    @property
    def file_name(self):
        return self.__file_name

    @property
    def iloc_economic_status_score(self):
        return self.__iloc_economic_status_score

    @property
    def iloc_is_tokyo_flag(self):
        return self.__iloc_is_tokyo_flag

    @property
    def iloc_field(self):
        return self.__iloc_field

    @property
    def iloc_industry(self):
        return self.__iloc_industry

    @property
    def iloc_reason_type(self):
        return self.__iloc_reason_type

    @property
    def iloc_reason_sentence(self):
        return self.__iloc_reason_sentence

    @property
    def is_future(self):
        return 'Future' in self.name

    @property
    def is_koshinetsu(self):
        return 'Koshinetsu' in self.name