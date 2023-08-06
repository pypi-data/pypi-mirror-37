import typing as typ
from datetime import date, datetime, timedelta
from functools import partial

import click

from .dt_util import (
    TODAY,
    ensure_date,
    to_month_end,
    to_month_start,
    to_smart_month_start,
    to_smart_week_start,
    to_week_end,
    to_week_start,
)
from .entrys import Entry, compact_data, group_data
from .plugins import load_data_for_all_dates

DATE_FORMATS = ("%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y", "%d/%m/%Y")


def create_cli(sub_fn=None):
    @click.option(
        "--round-summary/--noround-summary", "-r/-R", "round_summary", default=True
    )
    @click.option("--color/--no-color", "-c/-C", "color", default=None)
    @click.pass_context
    def cli(ctx, round_summary, color, **kwargs):
        ctx.ensure_object(dict)
        if color in [True, False]:
            ctx.color = color
        if sub_fn:
            sub_fn(ctx, **kwargs)
        else:
            assert kwargs == {}

    if not sub_fn:
        return click.group()(cli)
    return cli


def create_ranged(sub_fn):
    month_start = to_smart_month_start(TODAY)

    @click.argument(
        "start", default=month_start, type=click.DateTime(formats=DATE_FORMATS)
    )
    @click.argument(
        "end",
        default=to_month_end(month_start),
        type=click.DateTime(formats=DATE_FORMATS),
    )
    @click.option("--inclusive/--exclusive", "-i/-e", "inclusive", default=False)
    @click.pass_context
    def ranged(ctx, start, end, inclusive, **kwargs):
        summary = ctx.obj["summary"]
        detail = ctx.obj["detail"]
        if detail is None:
            detail = False
        if inclusive:
            end += timedelta(days=1)
        start, end = ensure_date(start), ensure_date(end)
        days = [
            start + timedelta(days=day_offset)
            for day_offset in range((end - start).days)
        ]
        progress_load_data(days)
        sub_fn(ctx, days, **kwargs)

    return ranged


def print_entries(*a, **k):
    click.echo(stringify_entries(*a, **k))


def stringify_entries(
    entries: typ.Collection[Entry],
    indent: str = "  ",
    colors: typ.Union[None, bool, str, typ.Tuple[str, str, str]] = True,
):
    output = ""
    if colors is True:
        name_color, ts_color, val_color = ("green", "blue", "")
    if not colors or isinstance(colors, bool):  # isinstance to make mypy happy
        name_color, ts_color, val_color = ("", "", "")
    elif isinstance(colors, str):
        name_color, ts_color, val_color = colors, colors, colors
    else:
        name_color, ts_color, val_color = colors
    for entry in sorted(entries):
        name, ts, val = entry.to_line_parts()
        output += (
            indent
            + click.style(f"{name:<14}", fg=name_color)
            + click.style(f"{ts:<20}", fg=ts_color)
            + click.style(f"{val}", fg=val_color)
            + "\n"
        )
    return output.rstrip("\n")


def progress_load_data(days: typ.Collection[date]) -> typ.List[typ.Collection[Entry]]:
    with click.progressbar(label="Pre-loading data", length=len(days) + 1) as bar:
        bar.update(1)
        data = []
        for idx, dat in enumerate(load_data_for_all_dates(days)):
            bar.update(idx + 1)
            data.append(dat)
        return data


def tks_entries(
    day: date,
    data: typ.Collection[Entry],
    *,
    summary: bool,
    detail: bool,
    compact_detail: bool = True,
) -> str:
    output = ""
    if summary or detail:
        output += (
            click.style(day.strftime("%Y-%m-%d"), fg="green", bold=True)
            + " # "
            + click.style(day.strftime("%A"), fg="cyan")
            + "\n"
        )
    if summary:
        grouped = group_data(data)
        if not grouped:
            output += "# " + click.style("Day blank", fg="yellow") + "\n"
        else:
            output += stringify_entries(grouped, indent="") + "\n"
    if detail:
        if summary:
            output += click.style(("#" * 40) + "\n", dim=True) + "\n"
        if compact_detail:
            output += stringify_entries(compact_data(data)) + "\n"
        else:
            output += stringify_entries(data) + "\n"
    return output.rstrip("\n")


def attach_aliases(cli, single, ranged=None):  # typing: ignore
    if ranged is None:

        def simple_ranged_impl():
            progress_load_data(days)
            for day in days:
                ctx.forward(single, date=day)

        ranged = cli.command(name="range")(simple_ranged_impl)

    @cli.command()
    @click.pass_context
    def today(ctx):
        ctx.forward(single, date=TODAY)

    @cli.command()
    @click.pass_context
    def yesterday(ctx):
        ctx.forward(single, date=(TODAY - timedelta(days=1)))

    @cli.command()
    @click.pass_context
    def week(ctx):
        week_start = to_smart_week_start(TODAY)
        ctx.forward(
            ranged, start=week_start, end=to_week_end(week_start), inclusive=True
        )

    @cli.command()
    @click.pass_context
    def this_week(ctx):
        ctx.forward(
            ranged, start=to_week_start(TODAY), end=to_week_end(TODAY), inclusive=True
        )

    @cli.command()
    @click.pass_context
    def last_week(ctx):
        week_start = to_week_start(TODAY - timedelta(days=7))
        ctx.forward(
            ranged, start=week_start, end=to_week_end(week_start), inclusive=True
        )

    @cli.command()
    @click.pass_context
    def month(ctx):
        month_start = to_smart_month_start(TODAY)
        ctx.forward(
            ranged, start=month_start, end=to_month_end(month_start), inclusive=True
        )

    @cli.command()
    @click.pass_context
    def this_month(ctx):
        ctx.forward(
            ranged, start=to_month_start(TODAY), end=to_month_end(TODAY), inclusive=True
        )

    @cli.command()
    @click.pass_context
    def last_month(ctx):
        month_end = to_month_start(TODAY) - timedelta(days=1)
        ctx.forward(
            in_range, start=to_month_start(month_end), end=month_end, inclusive=True
        )
