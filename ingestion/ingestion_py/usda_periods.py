from __future__ import annotations

import calendar
import re
from dataclasses import dataclass
from datetime import date
from typing import Literal

PeriodType = Literal["year", "quarter", "month"]


@dataclass(frozen=True)
class CanonicalPeriod:
    time_id: str
    period_type: PeriodType
    year: int
    quarter: int | None
    month: int | None
    period_start: date
    period_end: date


_QUARTER_LABELS = {
    "jan_mar": 1,
    "apr_jun": 2,
    "jul_sep": 3,
    "oct_dec": 4,
    "q1": 1,
    "q2": 2,
    "q3": 3,
    "q4": 4,
}


def _quarter_bounds(year: int, quarter: int) -> tuple[date, date]:
    start_month = 1 + (quarter - 1) * 3
    end_month = start_month + 2
    start = date(year, start_month, 1)
    end_day = calendar.monthrange(year, end_month)[1]
    end = date(year, end_month, end_day)
    return start, end


def parse_year_period(year: int, period_raw: str | None) -> CanonicalPeriod:
    """
    Convert notebook-like (year, period) into canonical (time_id, period_type, bounds).

    Supported period values:
    - annual / year / y / "" / None -> year
    - jan_mar, apr_jun, jul_sep, oct_dec, q1..q4 -> quarter
    - YYYY-MM or MM (with optional month names) can be added later when you ingest monthly series.
    """
    period = (period_raw or "").strip().lower()

    if period in ("", "annual", "year", "y"):
        start = date(year, 1, 1)
        end = date(year, 12, 31)
        return CanonicalPeriod(
            time_id=f"{year:04d}",
            period_type="year",
            year=year,
            quarter=None,
            month=None,
            period_start=start,
            period_end=end,
        )

    if period in _QUARTER_LABELS:
        q = _QUARTER_LABELS[period]
        start, end = _quarter_bounds(year, q)
        return CanonicalPeriod(
            time_id=f"{year:04d}-Q{q}",
            period_type="quarter",
            year=year,
            quarter=q,
            month=None,
            period_start=start,
            period_end=end,
        )

    m = re.fullmatch(r"(\d{4})-([a-zA-Z]{3})", period)
    if m:
        y = int(m.group(1))
        mo_str = m.group(2).title()
        month_map = {name: i for i, name in enumerate(calendar.month_abbr) if i > 0}
        if mo_str in month_map:
            mo = month_map[mo_str]
            end_day = calendar.monthrange(y, mo)[1]
            return CanonicalPeriod(
                time_id=f"{y:04d}-{mo:02d}",
                period_type="month",
                year=y,
                quarter=None,
                month=mo,
                period_start=date(y, mo, 1),
                period_end=date(y, mo, end_day),
            )

    raise ValueError(f"Unsupported period '{period_raw}' for year={year}.")

