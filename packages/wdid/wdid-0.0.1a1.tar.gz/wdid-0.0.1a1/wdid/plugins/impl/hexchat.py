import os
import subprocess
import typing as typ
from datetime import date, datetime, time

from wdid.dt_util import parse_date_string
from wdid.entrys import CombinedEntry, Entry

XCHAT_TIME_FORMAT = ("%b %d %H:%M:%S",)
XCHAT_USERNAME = "opal"

xchat_dirs = [
    os.path.expanduser("~/.config/hexchat/logs/"),
    os.path.expanduser("~/.xchat2/xchatlogs/"),
]


def output_lines(command: typ.Sequence[str], **kwargs: typ.Any) -> typ.Collection[str]:
    return subprocess.run(
        command, universal_newlines=True, check=True, stdout=subprocess.PIPE, **kwargs
    ).stdout.splitlines()


def parse_xchat_logs(today: date) -> typ.Collection[Entry]:
    xchat_date = today.strftime("%b %d")
    dirs = filter(os.path.exists, xchat_dirs)
    if not dirs:
        return []
    data: typ.List[Entry] = []
    try:
        for file in output_lines(
            [
                "grep",
                "--text",
                "-irl",
                xchat_date + " .* <" + XCHAT_USERNAME + ">",
                *dirs,
            ]
        ):
            _, _, channel = file.rpartition("/")
            channel, _, _ = channel.rpartition(".")
            for line in output_lines(["grep", "--text", "-i", xchat_date, file]):
                if "opal" not in line:
                    if (
                        " has quit (" in line
                        or ") has joined " + channel in line
                        or "chanserv gives channel operator status to " in line
                    ):
                        continue
                    if "#" in channel:
                        continue
                try:
                    dt = parse_date_string(line[:15], XCHAT_TIME_FORMAT)
                    dt = dt.replace(year=today.year)
                    e = Entry(timestamp=dt, owner=channel, entry=line[16:])
                    if e not in data:
                        data.append(e)
                except ValueError:
                    pass
    except subprocess.CalledProcessError:
        pass
    return data
