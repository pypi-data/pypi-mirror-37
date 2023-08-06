import os
import pathlib
import subprocess
import typing as typ
from datetime import date, datetime, time, timedelta

from wdid.dt_util import AUCKLAND_TZ, UTC, parse_date_string
from wdid.entrys import CombinedEntry, Entry
from wdid.fs_util import riterdir

local_history_dirs = [
    pathlib.Path("~/.atom/local-history/").expanduser(),
    pathlib.Path("~/.vscode/.history/").expanduser(),
]

ATOM_TIME_FORMATS = ("%Y-%m-%d_%I-%M-%S %p", "%Y-%m-%d_%H-%M-%S")

PROJECT_CONTAINING_FOLDERS = []
for raw_path in [
    "~/Fairfax",
    "~/Scratchpad/Firefox-Dev/",
    "~/Scratchpad",
    "~/nativform",
    "~/catinternal",
    "~/piwik3/",
]:
    path = pathlib.Path(raw_path).expanduser()
    if path.is_dir():
        PROJECT_CONTAINING_FOLDERS.append(path.resolve())
    del path


def parse_local_history(today: date) -> typ.Collection[Entry]:
    root = pathlib.Path("/")
    data: typ.List[Entry] = []
    file_bases = {}
    for local_history_dir in local_history_dirs:
        if not local_history_dir.is_dir():
            return data
        prefix = today.strftime("%Y-%m-%d")
        for file in riterdir(local_history_dir):
            if not file.is_file() or not file.name.startswith(prefix):
                continue
            time_end = file.name.index("_", 15)
            time = file.name[:time_end]
            dt = parse_date_string(time, ATOM_TIME_FORMATS)
            if file.parent in file_bases:
                file_base = file_bases[file.parent]
            else:
                file_base = file_bases[file.parent] = root / file.parent.relative_to(
                    local_history_dir
                )
            filename = file_base / file.name[time_end + 1 :]
            data.append(Entry(dt, "local-history", to_project_path(filename)))
    print(f"LH done with {today}")
    return data


def to_project_path(fpath: pathlib.Path) -> str:
    for path in PROJECT_CONTAINING_FOLDERS:
        try:
            project_name = fpath.relative_to(path).parts[0]
            return str(path / project_name)
        except ValueError:
            pass
    return str(fpath)
