import pathlib
import sqlite3
import typing as typ
from datetime import date, datetime, time

from wdid.entrys import CombinedEntry

DATABASE = pathlib.Path("~/.local/share/hamster-gtk/hamster-gtk.sqlite").expanduser()


ACTIVITIES_QUERY = """
SELECT activities.name as name,
       "start", "end"
  FROM facts LEFT JOIN activities ON (facts.activity_id = activities.id)
 WHERE "start" > ? AND "start" < ? AND "end" IS NOT NULL
 ORDER BY "start"
"""


def parse_datetime(dt_str: typ.Union[str, bytes]) -> datetime:
    if isinstance(dt_str, bytes):
        dt_str = dt_str.decode("utf-8")
    return datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S.%f")


sqlite3.register_converter("DATETIME", parse_datetime)
# sqlite3.register_converter(datetime, datetime.isoformat)


def parse_hamster(today: date) -> typ.Collection[CombinedEntry]:
    if not DATABASE.exists():
        return []
    conn = sqlite3.connect(
        "file:%s?mode=ro" % DATABASE, uri=True, detect_types=sqlite3.PARSE_COLNAMES
    )
    conn.row_factory = sqlite3.Row
    start = datetime.combine(today, time.min).isoformat(" ")
    end = (datetime.combine(today, time.max)).isoformat(" ")
    cur = conn.execute(ACTIVITIES_QUERY, (start, end))
    data = []
    for row in cur:
        data.append(
            CombinedEntry(
                timestamp=parse_datetime(row["start"]),
                owner="hamster",
                entry=row["name"],
                end_timestamp=parse_datetime(row["end"]),
                original_entries=(),
            )
        )
    return data
