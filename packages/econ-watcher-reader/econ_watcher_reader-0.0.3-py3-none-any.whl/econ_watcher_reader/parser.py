import numpy as np
import pandas as pd
from econ_watcher_reader.settings import TOKYO_FLAG_VALUE_IN_RAW_DATA
from logging import getLogger
logger = getLogger(__name__)


def eliminate_rows_with_na_in_economic_status(watcher_file: pd.DataFrame,
                                              iloc_economic_status_score: int
                                              ) -> pd.DataFrame:
    """
    Eliminate rows do not contain economic stats score from data.

    :param pd.DataFrame watcher_file: DataFrame downloaded by scraper.get_watcher_file.
    :param int iloc_economic_status_score: integer index of economic status score
    :return pd.DataFrame : eliminated DataFrame
    """

    watcher_file = watcher_file[~watcher_file.iloc[:, iloc_economic_status_score].isnull()]
    return watcher_file


def eliminate_newline_code(watcher_file: pd.DataFrame) -> pd.DataFrame:
    """
    Eliminate newline code '\n' and '\r' from data.

    :param pd.DataFrame watcher_file: DataFrame downloaded by scraper.get_watcher_file.
    :return: eliminated DataFrame
    """

    watcher_file = watcher_file.apply(
        lambda x:x.str.replace('\n', '').str.replace('\r','') if x.dtype == np.object else x
    )
    return watcher_file


def build_is_tokyo_flag(watcher_file: pd.DataFrame, iloc_is_tokyo_flag: int) -> pd.DataFrame:
    """
    Add flag to rows about Tokyo.

    :param pd.DataFrame watcher_file: DataFrame downloaded by scraper.get_watcher_file.
    :param iloc_is_tokyo_flag: the column number of tokyo flag in raw data.
    :return:
    """
    watcher_file = watcher_file.assign(
        is_tokyo=lambda x: ~x.iloc[:, iloc_is_tokyo_flag].isnull() & x.iloc[:, iloc_is_tokyo_flag].str.contains(TOKYO_FLAG_VALUE_IN_RAW_DATA)
    )
    return watcher_file


def make_field_column(watcher_file: pd.DataFrame, iloc_field: int) -> pd.DataFrame:
    """
    Make field column.
    Fill na value in field column using ffill method in pandas.

    :param pd.DataFrame watcher_file: DataFrame downloaded by scraper.get_watcher_file.
    :param int iloc_field: the column number of field in raw data.
    :return: DataFrame with field column
    """
    watcher_file = watcher_file.assign(
        field=lambda x: x.iloc[:, iloc_field].fillna(method='ffill')
    )
    return watcher_file


def clean_field_column(watcher_file_with_field: pd.DataFrame) -> pd.DataFrame:
    """
    Clean string in field column. It Removes '(Prefecture name)'.
    This method should be called after creating 'region' column,
    because the part '(Prefecture name)' in field column is used to make 'region' column.
    If you do not need 'region' column, you do not have to care about it.

    :param pd.DataFrame watcher_file_with_field: DataFrame object with field column created by make_field_column.
    :return: DataFrame with cleaned field column.
    """
    if not 'region' in watcher_file_with_field.columns:
        logger.warning('Passed DataFrame does not have `region`. '
                       'This method assumed to be called after creating `region` column.')

    watcher_file_with_field = watcher_file_with_field.assign(
        field=lambda x: x.field.str.replace(r'(\(.*?\))','').str.strip()
    )
    return watcher_file_with_field


def make_region_column(watcher_file_with_field: pd.DataFrame) -> pd.DataFrame:
    """
    Make region column from field column.
    Because the values in the field column have region name in parenthesis like `Field Name`(),
    this method extracts string in the parenthesis.
    So, this method might not work if the format of raw data would be changed.

    :param watcher_file_with_field: DataFrame object with field column created by make_field_column.
    :return: DataFrame with region column.
    """
    watcher_file = watcher_file_with_field.assign(
        region=lambda x: x.field.str.extract(r'((?<=\().*?(?=\)))')
    )
    return watcher_file


def convert_economic_state_score_into_integer(watcher_file: pd.DataFrame,
                                              iloc_economic_status_score: int,
                                              hash_map_for_score_symbol
                                              ) -> pd.DataFrame:
    """
    Convert economic state score into integer.

    :param pd.DataFrame watcher_file: DataFrame downloaded by scraper.get_watcher_file.
    :param int iloc_economic_status_score: the column number of economic status score in raw data.
    :return: DataFrame with integer economic score column.
    """
    def _convert(value):
        try:
            return hash_map_for_score_symbol[value]
        except KeyError:
            return np.nan

    watcher_file = watcher_file.assign(
        score=lambda x: x.iloc[:, iloc_economic_status_score].apply(_convert)
    )
    return watcher_file


def eliminate_rows_without_sentence(watcher_file: pd.DataFrame, iloc_reason_sentence: int) -> pd.DataFrame:
    """
    Remove rowa with no sentence in sentence reason column.

    :param pd.DataFrame watcher_file: DataFrame downloaded by scraper.get_watcher_file.
    :return: DataFrame without na value in reason sentence.
    """
    watcher_file = watcher_file.dropna(subset=['score'])
    including_sentence = watcher_file.iloc[:, iloc_reason_sentence].apply(lambda x: len(x) > 1)

    return watcher_file[including_sentence]


def clean_sentence_reason(watcher_file: pd.DataFrame, iloc_reason_sentence: int) -> pd.DataFrame:
    """
    Delete center dot at the head of the sentences.

    :param watcher_file: watcher data, na in the sentence must be eliminated before call this function.
    :param iloc_reason_sentence: index number of reason sentence column
    :return: cleaned date
    """
    watcher_file = watcher_file.assign(
        reason_sentence=lambda x: x.iloc[:, iloc_reason_sentence].str.replace('・', '', n=1)
    )
    return watcher_file
