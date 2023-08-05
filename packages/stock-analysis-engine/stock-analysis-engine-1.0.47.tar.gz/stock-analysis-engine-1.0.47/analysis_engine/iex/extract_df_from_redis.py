"""
Extract an IEX dataset from Redis (S3 support coming soon) and
load it into a ``pandas.DataFrame``

Supported environment variables:

::

    # verbose logging in this module
    export DEBUG_EXTRACT=1

    # verbose logging for just Redis operations in this module
    export DEBUG_REDIS_EXTRACT=1

    # verbose logging for just S3 operations in this module
    export DEBUG_S3_EXTRACT=1

"""

import analysis_engine.extract_utils as extract_utils
from spylunking.log.setup_logging import build_colorized_logger
from analysis_engine.iex.consts import DATAFEED_DAILY
from analysis_engine.iex.consts import DATAFEED_MINUTE
from analysis_engine.iex.consts import DATAFEED_STATS
from analysis_engine.iex.consts import DATAFEED_PEERS
from analysis_engine.iex.consts import DATAFEED_NEWS
from analysis_engine.iex.consts import DATAFEED_FINANCIALS
from analysis_engine.iex.consts import DATAFEED_EARNINGS
from analysis_engine.iex.consts import DATAFEED_DIVIDENDS
from analysis_engine.iex.consts import DATAFEED_COMPANY
from analysis_engine.iex.consts import get_datafeed_str

log = build_colorized_logger(
    name=__name__)


def extract_daily_dataset(
        work_dict,
        scrub_mode='sort-by-date'):
    """extract_daily_dataset

    Fetch the IEX daily data for a ticker and
    return it as a pandas Dataframe

    :param work_dict: dictionary of args
    :param scrub_mode: type of scrubbing handler to run
    """
    label = work_dict.get('label', 'extract')
    df_type = DATAFEED_DAILY
    df_str = get_datafeed_str(df_type=df_type)

    log.info(
        '{} - {} - start'.format(
            label,
            df_str))

    return extract_utils.perform_extract(
        df_type=df_type,
        df_str=df_str,
        work_dict=work_dict,
        scrub_mode=scrub_mode)
# end of extract_daily_dataset


def extract_minute_dataset(
        work_dict,
        scrub_mode='sort-by-date'):
    """extract_minute_dataset

    Fetch the IEX minute intraday data for a ticker and
    return it as a pandas Dataframe

    :param work_dict: dictionary of args
    :param scrub_mode: type of scrubbing handler to run
    """
    label = work_dict.get('label', 'extract')
    df_type = DATAFEED_MINUTE
    df_str = get_datafeed_str(df_type=df_type)

    log.info(
        '{} - {} - start'.format(
            label,
            df_str))

    return extract_utils.perform_extract(
        df_type=df_type,
        df_str=df_str,
        work_dict=work_dict,
        scrub_mode=scrub_mode)
# end of extract_minute_dataset


def extract_stats_dataset(
        work_dict,
        scrub_mode='sort-by-date'):
    """extract_stats_dataset

    Fetch the IEX statistics data for a ticker and
    return it as a pandas Dataframe

    :param work_dict: dictionary of args
    :param scrub_mode: type of scrubbing handler to run
    """
    label = work_dict.get('label', 'extract')
    df_type = DATAFEED_STATS
    df_str = get_datafeed_str(df_type=df_type)

    log.info(
        '{} - {} - start'.format(
            label,
            df_str))

    return extract_utils.perform_extract(
        df_type=df_type,
        df_str=df_str,
        work_dict=work_dict,
        scrub_mode=scrub_mode)
# end of extract_stats_dataset


def extract_peers_dataset(
        work_dict,
        scrub_mode='sort-by-date'):
    """extract_peers_dataset

    Fetch the IEX peers data for a ticker and
    return it as a pandas Dataframe

    :param work_dict: dictionary of args
    :param scrub_mode: type of scrubbing handler to run
    """
    label = work_dict.get('label', 'extract')
    df_type = DATAFEED_PEERS
    df_str = get_datafeed_str(df_type=df_type)

    log.info(
        '{} - {} - start'.format(
            label,
            df_str))

    return extract_utils.perform_extract(
        df_type=df_type,
        df_str=df_str,
        work_dict=work_dict,
        scrub_mode=scrub_mode)
# end of extract_peers_dataset


def extract_news_dataset(
        work_dict,
        scrub_mode='sort-by-date'):
    """extract_news_dataset

    Fetch the IEX news data for a ticker and
    return it as a pandas Dataframe

    :param work_dict: dictionary of args
    :param scrub_mode: type of scrubbing handler to run
    """
    label = work_dict.get('label', 'extract')
    df_type = DATAFEED_NEWS
    df_str = get_datafeed_str(df_type=df_type)

    log.info(
        '{} - {} - start'.format(
            label,
            df_str))

    return extract_utils.perform_extract(
        df_type=df_type,
        df_str=df_str,
        work_dict=work_dict,
        scrub_mode=scrub_mode)
# end of extract_news_dataset


def extract_financials_dataset(
        work_dict,
        scrub_mode='sort-by-date'):
    """extract_financials_dataset

    Fetch the IEX financial data for a ticker and
    return it as a pandas Dataframe

    :param work_dict: dictionary of args
    :param scrub_mode: type of scrubbing handler to run
    """
    label = work_dict.get('label', 'extract')
    df_type = DATAFEED_FINANCIALS
    df_str = get_datafeed_str(df_type=df_type)

    log.info(
        '{} - {} - start'.format(
            label,
            df_str))

    return extract_utils.perform_extract(
        df_type=df_type,
        df_str=df_str,
        work_dict=work_dict,
        scrub_mode=scrub_mode)
# end of extract_financials_dataset


def extract_earnings_dataset(
        work_dict,
        scrub_mode='sort-by-date'):
    """extract_earnings_dataset

    Fetch the IEX earnings data for a ticker and
    return it as a pandas Dataframe

    :param work_dict: dictionary of args
    :param scrub_mode: type of scrubbing handler to run
    """
    label = work_dict.get('label', 'extract')
    df_type = DATAFEED_EARNINGS
    df_str = get_datafeed_str(df_type=df_type)

    log.info(
        '{} - {} - start'.format(
            label,
            df_str))

    return extract_utils.perform_extract(
        df_type=df_type,
        df_str=df_str,
        work_dict=work_dict,
        scrub_mode=scrub_mode)
# end of extract_earnings_dataset


def extract_dividends_dataset(
        work_dict,
        scrub_mode='sort-by-date'):
    """extract_dividends_dataset

    Fetch the IEX dividends data for a ticker and
    return it as a pandas Dataframe

    :param work_dict: dictionary of args
    :param scrub_mode: type of scrubbing handler to run
    """
    label = work_dict.get('label', 'extract')
    df_type = DATAFEED_DIVIDENDS
    df_str = get_datafeed_str(df_type=df_type)

    log.info(
        '{} - {} - start'.format(
            label,
            df_str))

    return extract_utils.perform_extract(
        df_type=df_type,
        df_str=df_str,
        work_dict=work_dict,
        scrub_mode=scrub_mode)
# end of extract_dividends_dataset


def extract_company_dataset(
        work_dict,
        scrub_mode='NO_SORT'):
    """extract_company_dataset

    Fetch the IEX company data for a ticker and
    return it as a pandas Dataframe

    :param work_dict: dictionary of args
    :param scrub_mode: type of scrubbing handler to run
    """
    label = work_dict.get('label', 'extract')
    df_type = DATAFEED_COMPANY
    df_str = get_datafeed_str(df_type=df_type)

    log.info(
        '{} - {} - start'.format(
            label,
            df_str))

    return extract_utils.perform_extract(
        df_type=df_type,
        df_str=df_str,
        work_dict=work_dict,
        scrub_mode=scrub_mode)
# end of extract_company_dataset
