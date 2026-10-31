"""US-08 kabul senaryoları (AT-22 ... AT-30), ADR-002 kuralına göre."""
from datetime import date

from app.domain.renewal import Period
from app.domain.reminders import DueReminder, due_reminders

START = date(2026, 1, 15)          # aylık, yenileme her ayın 15'i
CREATED = date(2026, 1, 15)
R = date(2026, 11, 15)             # test günlerindeki sonraki yenileme


def days(items):
    return [(r.days_before, r.renewal_date, r.remind_on) for r in items]


def test_three_day_reminder_on_renewal_minus_3():            # AT-22
    result = due_reminders(START, Period.MONTHLY, CREATED, today=date(2026, 11, 12))
    assert days(result) == [(3, R, date(2026, 11, 12))]


def test_one_day_reminder_on_renewal_minus_1():              # AT-23
    result = due_reminders(START, Period.MONTHLY, CREATED, today=date(2026, 11, 14))
    # 3 günlük hatırlatma da vadesi gelmiş sayılır; çift kaydı veritabanı kısıtı eler.
    assert days(result) == [(3, R, date(2026, 11, 12)), (1, R, date(2026, 11, 14))]


def test_same_input_gives_same_output_idempotent():          # AT-24 (saf fonksiyon)
    args = (START, Period.MONTHLY, CREATED, date(2026, 11, 14))
    assert due_reminders(*args) == due_reminders(*args)


def test_added_two_days_before_renewal_gets_only_one_day_reminder():   # AT-25
    created = date(2026, 11, 13)
    assert due_reminders(START, Period.MONTHLY, created, today=date(2026, 11, 13)) == []
    result = due_reminders(START, Period.MONTHLY, created, today=date(2026, 11, 14))
    assert days(result) == [(1, R, date(2026, 11, 14))]


def test_nothing_due_on_renewal_day():
    assert due_reminders(START, Period.MONTHLY, CREATED, today=R) == []


def test_next_cycle_gets_its_own_two_reminders():            # AT-27
    after = due_reminders(START, Period.MONTHLY, CREATED, today=date(2026, 11, 16))
    assert after == []
    r2 = date(2026, 12, 15)
    result = due_reminders(START, Period.MONTHLY, CREATED, today=date(2026, 12, 14))
    assert days(result) == [(3, r2, date(2026, 12, 12)), (1, r2, date(2026, 12, 14))]


def test_added_after_one_day_reminder_date_gets_nothing_that_cycle():  # AT-30
    created = date(2026, 11, 14)  # 09:00'dan sonra eklendi, iş o gün zaten çalıştı
    assert due_reminders(START, Period.MONTHLY, created, today=date(2026, 11, 15)) == []
    assert due_reminders(START, Period.MONTHLY, created, today=date(2026, 11, 16)) == []


def test_month_end_renewal():
    start = date(2027, 1, 31)  # 31 Ocak -> 28 Şubat
    result = due_reminders(start, Period.MONTHLY, start, today=date(2027, 2, 25))
    assert days(result) == [(3, date(2027, 2, 28), date(2027, 2, 25))]


def test_yearly_reminder():
    start = date(2025, 3, 10)
    result = due_reminders(start, Period.YEARLY, start, today=date(2027, 3, 7))
    assert days(result) == [(3, date(2027, 3, 10), date(2027, 3, 7))]


def test_dataclass_is_hashable_value_object():
    a = DueReminder(date(2026, 11, 15), 3, date(2026, 11, 12))
    assert a == DueReminder(date(2026, 11, 15), 3, date(2026, 11, 12))
    assert len({a, a}) == 1
