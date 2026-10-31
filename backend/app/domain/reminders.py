"""Hatırlatma hesabı (ADR-002, adım 2 ve 4). Saf fonksiyon: veritabanı, zamanlayıcı ve web yok.

Günlük iş bu fonksiyonu her aktif abonelik için çağırır; dönen listeden veritabanında
zaten kayıtlı olanları `(subscription_id, renewal_date, days_before)` benzersiz kısıtı
eler, kalanları kaydedip gönderir.
"""
from dataclasses import dataclass
from datetime import date, timedelta

from app.domain.renewal import Period, next_renewal

# Yenilemeden kaç gün önce hatırlatılır (PO kararı D-01: 3 gün ve 1 gün).
REMINDER_OFFSETS: tuple[int, ...] = (3, 1)


@dataclass(frozen=True)
class DueReminder:
    renewal_date: date  # hatırlatılan yenileme günü
    days_before: int    # 3 veya 1
    remind_on: date     # renewal_date - days_before


def due_reminders(
    start_date: date,
    period: Period,
    created_on: date,
    today: date,
    offsets: tuple[int, ...] = REMINDER_OFFSETS,
) -> list[DueReminder]:
    """Bugün için vadesi gelmiş hatırlatmaları verir.

    R = bugünden kesinlikle sonraki ilk yenileme günü. Her `d` için
    `remind_on = R - d` ve kayıt yalnızca şu iki koşul birlikte doğruysa üretilir:
      - `remind_on <= today`      (vadesi gelmiş; kaçırılan günler telafi edilir),
      - `remind_on >= created_on` (abonelik eklenmeden önceki eşik için üretilmez).
    Yenileme günü geldiğinde R bir sonraki döneme kaydığı için o gün hatırlatma çıkmaz.
    """
    renewal = next_renewal(start_date, period, today)
    result: list[DueReminder] = []
    for days_before in offsets:
        remind_on = renewal - timedelta(days=days_before)
        if created_on <= remind_on <= today:
            result.append(DueReminder(renewal, days_before, remind_on))
    return result
