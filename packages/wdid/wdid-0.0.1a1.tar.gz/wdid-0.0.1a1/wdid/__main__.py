#!/usr/bin/env python3
import itertools
from datetime import date, datetime, timedelta
from functools import partial

import click

from .dt_util import (
    ensure_date,
    next_month_start,
    to_month_end,
    to_month_start,
    to_week_end,
    to_week_start,
    TODAY,
)
from .cli import create_cli, print_entries, attach_aliases, DATE_FORMATS, tks_entries
from .plugins import load_data_for_date
from .ts.__main__ import cli as ts_cli


@click.group()
@click.option("--summary/--no-summary", "-s/-S", "summary", default=True)
@click.option("--detail/--no-detail", "-d/-D", "detail", default=None)
@create_cli
def cli(ctx, summary, detail):
    ctx.obj["summary"] = summary
    ctx.obj["detail"] = detail


@cli.command()
@click.argument("date", default=TODAY, type=click.DateTime(formats=DATE_FORMATS))
@click.pass_context
def date(ctx, date):
    summary = ctx.obj["summary"]
    detail = ctx.obj["detail"]
    day = ensure_date(date)
    data = load_data_for_date(day)
    click.echo(tks_entries(day, data, summary=summary, detail=detail))


cli.add_command(ts_cli, name="ts")
attach_aliases(cli, date)

if __name__ == "__main__":
    cli()
