import typing as typ
from datetime import date, datetime, timedelta
from functools import lru_cache

from pytz import UTC, timezone

Dateish = typ.Union[date, datetime]

AUCKLAND_TZ = timezone("Pacific/Auckland")
QUARTER_HOUR = timedelta(minutes=15)
TODAY = datetime.now().date()


@lru_cache(maxsize=2 << 10)
def parse_date_string(date_string: str, formats: typ.Iterable[str]) -> datetime:
    for fmt in formats:
        try:
            return datetime.strptime(date_string, fmt)
            break
        except ValueError:
            pass
    raise ValueError("none of the formats matched the given date string.")


@lru_cache(maxsize=128)
def round_dt(dt: datetime, resolution, round_type="half_up") -> datetime:
    if isinstance(resolution, timedelta):
        resolution = resolution.total_seconds()
    tz = dt.tzinfo
    secs = dt.timestamp()
    diff = secs % resolution
    root = secs - diff
    res = root
    if round_type in ("down", "floor"):
        res = root
    elif round_type in ("up", "ceil", "ceiling"):
        if diff > 0:
            res = root + resolution
    elif round_type in ("half_up", "round"):
        if diff >= resolution / 2:
            res = root + resolution
    elif round_type == "half_down":
        if diff > resolution / 2:
            res = root + resolution
    else:
        raise ValueError("Unsupported round_type argument.")
    return datetime.fromtimestamp(res, tz=tz)


def ensure_date(dt: Dateish) -> date:
    if isinstance(dt, datetime):
        return dt.date()
    return dt


def to_month_start(dt: Dateish) -> date:
    return ensure_date(dt).replace(day=1)


def next_month_start(dt: Dateish) -> date:
    return to_month_start(to_month_start(dt) + timedelta(days=32))


def to_month_end(dt: Dateish) -> date:
    return next_month_start(dt) - timedelta(days=1)


def to_smart_month_start(dt: Dateish) -> date:
    d = ensure_date(dt)
    if d.day == 1:  # 1st of the month
        return to_month_start(d - timedelta(days=1))
    else:
        return to_month_start(d)


def to_week_start(dt: Dateish) -> date:
    # Week starts an Monday, and `weekday()` for monday == 0.
    d = ensure_date(dt)
    return d - timedelta(days=d.weekday())


def to_week_end(dt: Dateish) -> date:
    return to_week_start(dt) + timedelta(days=6)


def to_smart_week_start(dt: Dateish) -> date:
    d = ensure_date(dt)
    if d.weekday() == 0:
        return to_week_start(d - timedelta(days=1))
    else:
        return to_week_start(d)
