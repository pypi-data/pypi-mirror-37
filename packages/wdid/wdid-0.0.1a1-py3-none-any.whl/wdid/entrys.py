import typing as typ
from datetime import datetime, timedelta

import attr

from .dt_util import QUARTER_HOUR, round_dt

FIVE_MINUTES = timedelta(minutes=5)


@attr.s(frozen=True)
class Entry:

    timestamp: datetime = attr.ib()
    owner: str = attr.ib()
    entry: str = attr.ib()

    def to_line_parts(self) -> typ.Tuple[str, str, str]:
        return (self.owner, self.timestamp.strftime("%H:%M"), self.entry)

    def to_line(self):
        return "{:<14}{:<20}{}".format(*self.to_line_parts())


@attr.s(frozen=True)
class CombinedEntry(Entry):

    end_timestamp: datetime = attr.ib()
    original_entries: typ.Collection[Entry] = attr.ib()

    @classmethod
    def from_entries(
        cls, owner: str, entry_name: str, original_entries: typ.Collection[Entry]
    ) -> "CombinedEntry":
        assert len(original_entries) >= 2
        sorted_entries = sorted(original_entries)
        first_ts = sorted_entries[0].timestamp
        last_ts = sorted_entries[-1].timestamp
        return cls(first_ts, owner, entry_name, last_ts, tuple(sorted_entries))

    def to_line_parts(self) -> typ.Tuple[str, str, str]:
        et = self.end_timestamp.strftime("%H:%M")
        if self.timestamp != self.end_timestamp and et == "00:00":
            et = "24:00"
        ts = self.timestamp.strftime("%H:%M")
        return self.owner, f"{ts}-{et}", self.entry


def round_combined(
    entries: typ.Iterator[Entry], resolution: timedelta = QUARTER_HOUR
) -> typ.Iterator[Entry]:
    round_type = "down"
    for entry in entries:
        if isinstance(entry, CombinedEntry):
            start = round_dt(entry.timestamp, resolution, round_type)
            end = round_dt(entry.end_timestamp, resolution)
            yield attr.evolve(entry, timestamp=start, end_timestamp=end)
            round_type = "half_up"
        else:
            yield entry


def combine_close_entrys(
    data: typ.Collection[Entry]
) -> typ.Mapping[typ.Tuple[datetime, datetime], typ.Collection[Entry]]:
    grouping_len = timedelta(minutes=15)
    last_end = datetime.fromtimestamp(0)
    prev_data: typ.List[Entry] = []
    grouped = {}
    for entry in data:
        ts = entry.timestamp
        if entry.owner in ("Away", "Back") or ((last_end + grouping_len) < ts):
            if prev_data:
                first = prev_data[0].timestamp
                transformed = compact_data(prev_data)
                grouped[(first, last_end)] = tuple(transformed)
            prev_data = []
        if entry.owner not in ("#sysadmin", "#catalyst"):
            last_end = ts
        prev_data.append(entry)
    if prev_data:
        first = prev_data[0].timestamp
        transformed = compact_data(prev_data)
        grouped[(first, last_end)] = tuple(transformed)
    return grouped


def group_data(data: typ.Collection[Entry]) -> typ.Collection[Entry]:
    grouped_data = sorted(combine_close_entrys(data).items())
    out_data: typ.Iterator[Entry] = (
        CombinedEntry(start, "grouped", "🤷", end, ())
        for (start, end), _ in grouped_data
    )
    if round:
        out_data = round_combined(out_data)
    return sorted(out_data)


def compact_data(data: typ.Collection[Entry]) -> typ.Collection[Entry]:
    compacted_data: typ.List[Entry] = []
    prev_entry = ("", "")
    prev_ts = datetime.fromtimestamp(0)
    prev_entries: typ.List[Entry] = []

    def _commit() -> None:
        nonlocal prev_entry, prev_ts, prev_entries
        if len(prev_entries) <= 1:
            compacted_data.extend(prev_entries)
        else:
            new_entry = CombinedEntry.from_entries(
                prev_entry[0], prev_entry[1], prev_entries
            )
            compacted_data.append(new_entry)
        prev_entry = ("", "")
        prev_ts = datetime.fromtimestamp(0)
        prev_entries = []

    for entry in data:
        if (entry.owner, entry.entry) != prev_entry:
            _commit()
        elif (prev_ts + FIVE_MINUTES) < entry.timestamp:
            _commit()
        prev_entry = (entry.owner, entry.entry)
        prev_ts = entry.timestamp
        prev_entries.append(entry)
    _commit()

    return compacted_data
