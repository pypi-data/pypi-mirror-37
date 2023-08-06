import pathlib
import re
import typing as typ
from datetime import date, datetime, time

from wdid.dt_util import AUCKLAND_TZ, UTC
from wdid.entrys import CombinedEntry, Entry

zsh_history = pathlib.Path("~/.zsh_history").expanduser().resolve()


def parse_zsh_history(today: date) -> typ.Collection[Entry]:
    data: typ.List[Entry] = []
    with zsh_history.open("rb") as hist:
        item = None
        for line in hist:
            match = re.match(br"^: (\d+):\d;(.*)$", line)
            if match:
                if item:
                    time, cmd = item
                    item = None
                    data.append(Entry(time, "zsh", str(cmd)))
                timestamp, cmd = match.group(1, 2)
                time = datetime.fromtimestamp(int(timestamp), AUCKLAND_TZ)
                time = time.replace(tzinfo=None)
                if time.date() != today:
                    continue
                item = (time, cmd)
            else:
                if item:
                    item = (item[0], item[1] + line)
    return data
