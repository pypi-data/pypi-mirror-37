import itertools
import subprocess
import typing as typ
from datetime import date, datetime, timedelta
from multiprocessing import TimeoutError
from multiprocessing.pool import AsyncResult, Pool

from wdid.dt_util import Dateish, ensure_date
from wdid.entrys import Entry as _Entry  # Use `_` to prevent it's use in plugins

loaded_data = {}


def load_data_for_date(dateish: Dateish) -> typ.Collection[_Entry]:
    date = ensure_date(dateish)
    if date not in loaded_data:
        data = _load_data_for_date(date)
        loaded_data[date] = data
        return data
    else:
        return loaded_data[date]


def _load_data_for_date(date: date) -> typ.Collection[_Entry]:
    from .impl import hamster, hexchat, konversation, local_history, polari, zsh

    data: typ.List[_Entry] = []
    data += local_history.parse_local_history(date)
    data += hexchat.parse_xchat_logs(date)
    data += polari.parse_polari_chat_history(date)
    data += zsh.parse_zsh_history(date)
    data += konversation.parse_konversation_chat_history(date)
    data += hamster.parse_hamster(date)
    data = sorted(data)
    return tuple(data)


def _mp_pool_load(date: date):
    return date, _load_data_for_date(date)


def load_data_for_all_dates(
    dates: typ.Iterable[date]
) -> typ.Iterable[typ.Collection[_Entry]]:
    days = list(dates)
    del dates
    uniq_days = set(days)
    with Pool(processes=8) as pool:
        missing_days = set(filter(lambda day: day not in loaded_data, uniq_days))
        missing_iter = pool.imap_unordered(_mp_pool_load, missing_days)
        for day in days:
            if day in missing_days:
                for l_day, l_date in missing_iter:
                    loaded_data[l_day] = l_date
                    missing_days.discard(l_day)
                    if l_day == day:
                        break
            yield loaded_data[day]
