import requests
from econ_watcher_reader.settings import WATCHER_DISTRIBUTE_DIRECTORY
from bs4 import BeautifulSoup
import pandas as pd
import os.path
import re
from typing import List
import datetime
from logging import getLogger
logger = getLogger(__name__)


def get_watcher_directory(menu_page: str) -> List[str]:
    """
    Get links that distribute monthly economy watcher file from top page of economy watcher.
    Now it supports for only latest page, not for archive.

    :param str menu_page: link of top page of economywatcher survey in Cabinet Office web site.
    :return: list of link strings.
    """
    response = requests.get(menu_page)

    logger.info('get watcher links from %s' % response.url)

    soup = BeautifulSoup(response.content, features="html.parser")
    links_ = soup.find_all('a', class_='bulletLink')
    links_watcher = [os.path.dirname(link_.get('href')) + '/' for link_ in links_ if 'menu' in link_.get('href')]

    logger.info('done')
    return links_watcher


def get_watcher_file(link_: str, file_name: str) -> pd.DataFrame:
    """
    Download watcher file by Cabinet Office web site.
    It returns pandas.DaraFrame object, although the raw file is csv.

    :param str link_: url of the economy watcher survey file.
    :param str file_name: file name to get. This should be defined in settings.WatcherType.
    :return: downloaded file as DataFrame
    """
    file_url = WATCHER_DISTRIBUTE_DIRECTORY + link_ + file_name

    logger.info('get watcher file from %s' % file_url)

    data = pd.read_csv(file_url, header=None, encoding='cp932')
    return data


def get_publish_date_from_url(link_: str) -> datetime.datetime:
    """
    Get publish date from url.
    The urls of monthly economy watcher survey are seemed like 'yyyy/mm' of the publish date of the survey.

    :param str link_: the url of monthly economy watcher survey.
    :return: publish date of the survey
    """
    yyyymmdd = ''.join(re.findall(r'\d{4}', link_))
    pub_date = datetime.datetime.strptime(yyyymmdd, '%Y%m%d')

    logger.debug('yyyymmdd: {0}, date: {1:}'.format(*[yyyymmdd, pub_date]))
    return pub_date
