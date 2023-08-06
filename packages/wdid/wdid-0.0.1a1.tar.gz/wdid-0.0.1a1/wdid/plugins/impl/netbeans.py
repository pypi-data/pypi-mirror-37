import pathlib
import subprocess
import typing as typ
from datetime import date, datetime, time, timedelta

from wdid.dt_util import AUCKLAND_TZ, UTC, parse_date_string
from wdid.entrys import CombinedEntry, Entry
from .local_history import PROJECT_CONTAINING_FOLDERS

FIVE_MINUTES = timedelta(minutes=5)


local_history_dir = pathlib.Path("~").expanduser() / ".netbeans/"

ATOM_TIME_FORMATS = ["%Y-%m-%d_%I-%M-%S %p", "%Y-%m-%d_%H-%M-%S"]


def parse_local_history(today: date) -> typ.Collection[Entry]:
    if not local_history_dir.is_dir():
        return []
    data = []
    for line in subprocess.check_output(
        ["find", "-name", today.strftime("%Y-%m-%d") + "*"],
        cwd=str(local_history_dir),
        universal_newlines=True,
    ).splitlines():
        folder, _, filename = line.rpartition("/")
        time_end = filename.index("_", 15)
        time = filename[:time_end]
        dt = parse_date_string(time, ATOM_TIME_FORMATS)
        filename = folder[1:] + "/" + filename[time_end + 1 :]
        data.append(Entry(dt, "local-history", filename))
    return data


def compact_data(data):
    compacted_data = []
    prev_project_path = ""
    prev_project_ts = datetime.fromtimestamp(0)
    prev_project_entries = []

    def _commit():
        nonlocal compacted_data, prev_project_path, prev_project_ts
        nonlocal prev_project_entries
        if len(prev_project_entries) >= 2:
            compacted_data.append(
                CombinedEntry.from_entries(
                    "local-history", prev_project_path, prev_project_entries
                )
            )
        else:
            compacted_data += prev_project_entries
        prev_project_path = ""
        prev_project_ts = datetime.fromtimestamp(0)
        prev_project_entries = []

    for entry in data:
        if entry.owner != "local-history":
            _commit()
            compacted_data.append(entry)
            continue
        proj_path = to_project_path(entry.entry)
        if proj_path != prev_project_path:
            _commit()
        if (prev_project_ts + FIVE_MINUTES) < entry.timestamp:
            _commit()
        prev_project_path = proj_path
        prev_project_ts = entry.timestamp
        prev_project_entries.append(entry)
    _commit()

    return compacted_data


def to_project_path(filename):
    fpath = pathlib.Path(filename)
    for path in PROJECT_CONTAINING_FOLDERS:
        try:
            project_name = fpath.relative_to(path).parts[0]
            return path / project_name
        except ValueError:
            pass
    return str(fpath)
