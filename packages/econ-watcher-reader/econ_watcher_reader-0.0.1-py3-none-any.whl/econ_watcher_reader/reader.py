from econ_watcher_reader.settings import TOP_MENU_PAGE, WatcherType
import pandas as pd
import datetime
from econ_watcher_reader import scraper, parser
from logging import getLogger
logger = getLogger(__name__)


class EconomyWatcherReader(object):
    """
    Data reader for Economy Watcher provided from Cabinet Office of Japan.

    Logic:
    ======
    1. Initialization
        1. get available period from index page of the watcher survey.
    1. Get Raw data
        1. Get raw data from the we site of Cabinet Office
    1. Parsing
        1. Eliminate rows without economic status score. [done]
        1. Delete newline code, such as `\n` or `\r`. [done]
        1. Flag rows about Tokyo. [done]
        1. Make field column. Fill value field column of raw data. [done]
        1. Make Region column. [done] # TODO: Koshinetsu specific function
        1. Clean field column. [done]
        1. Convert economic state score to integer, from 0 to 4. [done] # TODO: Koshinetsu specific function
        1, Eliminate rows without sentence. [done]
        1. Clean reason sentence. delete center dot at the head. [done]
    1. Organizing
        1. Name column to use. [done]
            - For industry, reason_type, raw data are used.
            - For score, reason_sentence, field, region, columns defined in parse module used.
        1. Make date columns. This is not the same as publish date. [done]
    """

    def __init__(self):
        """
        Initialize Data Reader.
        """
        self.__set_available_period()

    def __set_available_period(self) -> None:
        """
        Attribute setter method for available period.

        :return: None
        """
        links_of_monthly_economy_watcher = scraper.get_watcher_directory(TOP_MENU_PAGE)
        logger.debug('links_of_monthly_economy_watcher: {}'.format(links_of_monthly_economy_watcher))
        publish_date_list = [
            scraper.get_publish_date_from_url(link_) for link_ in links_of_monthly_economy_watcher
        ]
        logger.debug('publish_date_list: {}'.format(publish_date_list))

        self.__AVAILABLE_PERIOD = pd.Series(
            [self.__set_datetime_month_to_one(month) - pd.offsets.MonthBegin(2) for month in publish_date_list]
        )
        logger.debug('AVAILABLE_PERIOD: {}'.format(self.__AVAILABLE_PERIOD.tolist()))

        self.__map_month_to_url = {
            month: url for month, url in zip(self.__AVAILABLE_PERIOD, links_of_monthly_economy_watcher)
        }
        logger.debug('map_month_to_url: {}'.format(self.__map_month_to_url))

        self.__LATEST_MONTH = max(self.__AVAILABLE_PERIOD)
        self.__EARLIEST_MONTH = min(self.__AVAILABLE_PERIOD)
        logger.debug('LATEST_MONTH: {0}, EARLIEST_MONTH: {1}'.format(
            *[self.__LATEST_MONTH, self.__EARLIEST_MONTH])
        )

    def get_data(self, kind_: str, start=None, end=None) -> pd.DataFrame:
        """
        The method to read economy watcher data.

        :param str kind_: The kind of the economy watcher data, future or current.
        :param datetime start: The first month of data to get. If None passed, returns all of the available data.
        :param datetime end: The last month of data to get. If None passed, returns data only on 'start' month. The default is None.
        :return pd.DataFrame: The DataFame of the Economy Watcher Survey.
        """
        # if both period parameters are None, get all available data.
        if start is None and end is None:
            start = self.__EARLIEST_MONTH
            end = self.__LATEST_MONTH

        # round passed datetime objects
        start = self.__set_datetime_month_to_one(start)
        if end is None:
            end = start
        end = self.__set_datetime_month_to_one(end)

        # raise if passed values are invalid.
        if start > end:
            raise ValueError('`start` date must be before `end` date.')

        if start < self.__EARLIEST_MONTH:
            raise ValueError('Data on {start:%B-%y} is not available. '
                             'Available period: [{earliest:%B-%y} - {latest:%B-%y}]'.format(
                start=start, earliest=self.__EARLIEST_MONTH, latest=self.__LATEST_MONTH
            ))

        if end > self.__LATEST_MONTH:
            raise ValueError('Data on {end:%B-%y} is not available. '
                             'Available period: [{earliest:%B-%y} - {latest:%B-%y}]'.format(
                end=end, earliest=self.__EARLIEST_MONTH, latest=self.__LATEST_MONTH
            ))

        # set range to get data
        available_period = self.__AVAILABLE_PERIOD
        data_range_to_get = available_period[(start <= available_period) & (available_period <= end)]
        logger.debug('data_range_to_get: {}'.format(data_range_to_get.tolist()))

        data_list=[]
        watcher_types = self.__define_watcher_type(kind_)
        for watcher_type in watcher_types:
            for month in data_range_to_get:
                logger.info('read data at: {:%B-%y}'.format(month))

                # Get raw data from the we site of Cabinet Office
                data_to_parse = scraper.get_watcher_file(
                    self.__map_month_to_url[month],
                    watcher_type.file_name
                )

                # Parsing
                parsed_data = self.__parse_data(data_to_parse, watcher_type)
                logger.debug('parsed_data at {month}: {data}'.format(
                    month=month ,data=parsed_data.head(),
                ))
                logger.debug('columns: %s' % parsed_data.columns)

                # Organize data
                data = self.__organize_parsed_data(parsed_data, watcher_type, month)
                data_list.append(data)

        data = pd.concat(data_list)

        return data

    @staticmethod
    def __define_watcher_type(kind_: str):
        if kind_ == 'current':
            return [WatcherType.Current]
        elif kind_ == 'future':
            return [WatcherType.Future]
        else:
            raise ValueError('Invalid parameter was passed as `kind_`.'
                             'It must be `current` or `future.`')

    @staticmethod
    def __set_datetime_month_to_one(month:datetime.datetime):
        return datetime.datetime(month.year, month.month, 1)

    @staticmethod
    def __parse_data(data_to_parse: pd.DataFrame, watcher_type: WatcherType):
        data = parser.eliminate_rows_with_na_in_economic_status(data_to_parse, watcher_type.iloc_economic_status_score)
        data = parser.eliminate_newline_code(data)
        data = parser.build_is_tokyo_flag(data, watcher_type.iloc_is_tokyo_flag)
        data = parser.make_field_column(data, watcher_type.iloc_field)
        data = parser.make_region_column(data)
        data = parser.clean_field_column(data)
        data = parser.convert_economic_state_score_into_integer(data, watcher_type.iloc_economic_status_score, watcher_type.score_map)
        data = parser.eliminate_rows_without_sentence(data, watcher_type.iloc_reason_sentence)
        data = parser.clean_sentence_reason(data, watcher_type.iloc_reason_sentence)
        return data

    @staticmethod
    def __organize_parsed_data(parsed_data: pd.DataFrame, watcher_type: WatcherType, date_point:datetime.datetime):
        """

        :param parsed_data:
        :param watcher_type:
        :return:
        """
        raw_data_column = list(parsed_data.columns[[watcher_type.iloc_industry, watcher_type.iloc_reason_type]])
        columns_made_in_parser = ['region', 'is_tokyo', 'field', 'score', 'reason_sentence']
        columns_to_use = raw_data_column + columns_made_in_parser

        parsed_data = parsed_data[columns_to_use].assign(
            date=pd.to_datetime(date_point)
        )

        # rename raw data column
        # parsed_data.rename(columns={raw_data_column[0]: 'industry', raw_data_column[1]: 'reason_type'}, inplace=True)
        parsed_data.rename(columns={iloc:watcher_type.get_name_from_iloc(iloc) for iloc in raw_data_column}, inplace=True)
        logger.debug('{}'.format(parsed_data.dtypes))
        return parsed_data

    @property
    def AVAILABLE_PERIOD(self) -> pd.Series:
        return self.__AVAILABLE_PERIOD

    @property
    def LATEST_MONTH(self) -> pd.Timestamp:
        return self.__LATEST_MONTH

    @property
    def EARLIEST_MONTH(self) -> pd.Timestamp:
        return self.__EARLIEST_MONTH
