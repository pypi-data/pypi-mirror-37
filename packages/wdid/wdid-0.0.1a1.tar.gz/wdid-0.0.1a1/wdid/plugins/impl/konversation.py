import pathlib
import re
import typing as typ
from datetime import date, datetime, time, timedelta
from functools import lru_cache

from wdid.bisect import bisect_matches_get_range
from wdid.dt_util import AUCKLAND_TZ, parse_date_string
from wdid.entrys import CombinedEntry, Entry

DATE_FORMATS = ("[%A, %d %B %Y]",)
TIME_FORMATS = ("[%I:%M:%S %p %Z]",)
logs_dir = pathlib.Path("~/logs/").expanduser().resolve()
DATE_RE = re.compile(r"^\[.*?\]")
REST_RE = re.compile("(\[.*?\]) (<.*>|Away)?\s+(.*)$")


def parse_line(line: str) -> typ.Tuple[typ.Optional[str], str]:
    match = DATE_RE.match(line)
    if not match:
        return None, line
    return match.group(0), line[match.endpos :]


def bisect_cmp(min_date: date, max_date: date, line: str) -> typ.Optional[int]:
    date_str, _ = parse_line(line)
    if not date_str:
        return None
    date = parse_date_string(date_str, DATE_FORMATS).date()
    if date < min_date:
        return -1
    elif date > max_date:
        return 1
    else:
        return 0


def parse_konversation_chat_history(today: date) -> typ.Collection[Entry]:
    min_date = today - timedelta(days=1)
    max_date = today + timedelta(days=1)
    data: typ.List[Entry] = []
    for file in logs_dir.iterdir():
        if file.suffix == ".log":
            stem = file.stem
            if not stem.startswith("catalyst_"):
                continue
            room = stem[len("catalyst_") :]

            room_data = []
            keep_room = room[0] != "#"
            with file.open("r") as f:
                lines = list(f)
                matched_lines = bisect_matches_get_range(
                    lines, lambda line: bisect_cmp(min_date, max_date, line)
                )
                for line in matched_lines:
                    date_str, rest = parse_line(line)
                    if not date_str:
                        continue
                    match = REST_RE.fullmatch(line)
                    if not match:
                        continue
                    time_str, user, message = match.groups()
                    time = (
                        datetime.combine(
                            parse_date_string(date_str, DATE_FORMATS).date(),
                            parse_date_string(time_str, TIME_FORMATS).time(),
                        )
                        .astimezone(AUCKLAND_TZ)
                        .replace(tzinfo=None)
                    )
                    if time.date() != today:
                        continue
                    if user == "Away":
                        if "no longer" in message:
                            user = "Back"
                        else:
                            time = time - timedelta(minutes=10)
                        room_data.append(Entry(time, user, ""))
                        continue
                    if user is not None:
                        message = "{:<12}{}".format(user, message)
                        if "opal" in user:
                            keep_room = True
                    room_data.append(Entry(time, room, message))
            if keep_room:
                data += room_data
    return data
