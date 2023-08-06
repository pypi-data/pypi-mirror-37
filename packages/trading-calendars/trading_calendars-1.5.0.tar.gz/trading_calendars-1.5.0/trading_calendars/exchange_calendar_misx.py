from datetime import time
import pandas as pd
from pytz import timezone
from .trading_calendar import TradingCalendar, HolidayCalendar
from .common_holidays import new_years_day
from pandas.tseries.holiday import (
  Holiday,
  next_monday,
)

MoscowNewYears = Holiday(
  'Moscow New Years Day',
  month=1,
  day=1,
  observance=next_monday
)

OrthodoxChristmas = Holiday(
  'Orthodox Christmas',
  month=1,
  day=7,
  observance=next_monday
)

DefenderOfTheFatherland = Holiday(
  'Defender of the Fatherland Day',
  month=2,
  day=23,
  observance=next_monday
)

InternationalWomensDay = Holiday(
  "International Women's Day",
  month=3,
  day=28,
  observance=next_monday
)

SpringAndLaborDay = Holiday(
  "Spring and Labor Day",
  month=5,
  day=1,
  observance=next_monday
)

VictoryDay = Holiday(
  "Victory Day",
  month=5,
  day=9,
  observance=next_monday
)

RussiaDay = Holiday(
  "Russia Day",
  month=6,
  day=12,
  observance=next_monday
)

UnityDay = Holiday(
  "Unity Day",
  month=11,
  day=4,
  observance=next_monday
)


class MISXExchangeCalendar(TradingCalendar):
    """
    Exchange calendar for the Moscow Stock Exchange (MISX, MOEX).

    Open time: 10:00 Europe/Moscow
    Close time: 18:45 Europe/Moscow
    """
    name = "MISX"
    tz = timezone("Europe/Moscow")
    open_times = (
      (None, time(10)),
    )
    close_times = (
      (None, time(18, 45)),
    )

    @property
    def regular_holidays(self):
      return HolidayCalendar([
        MoscowNewYears,
        OrthodoxChristmas,
        DefenderOfTheFatherland,
        InternationalWomensDay,
        SpringAndLaborDay,
        VictoryDay,
        RussiaDay,
        UnityDay
      ])
