"""Integration points, all mocked for the demo.

Each adapter has the method signature the real integration would use, so a
real OTP gateway, DBT payment rail or Revenue/TNeGA/PMFBY lookup can replace
the stub without touching the routers.
"""

import logging
import uuid

log = logging.getLogger("meetpu.adapters")


class OtpAdapter:
    """Mock: no SMS is sent. The fixed code from settings.mock_otp_code is accepted."""

    def send(self, phone: str) -> None:
        log.info("MOCK OTP requested for %s", phone)


class NotifyAdapter:
    """Mock SMS/WhatsApp: logs the message only."""

    def send(self, phone: str | None, message: str) -> None:
        log.info("MOCK SMS to %s: %s", phone, message)


class PaymentAdapter:
    """Mock DBT transfer: returns a fake reference. No money moves."""

    def pay(self, report_id: uuid.UUID, amount_inr: int | None = None) -> str:
        ref = f"MOCKPAY-{uuid.uuid4().hex[:10].upper()}"
        log.info("MOCK payment %s for report %s (amount %s)", ref, report_id, amount_inr)
        return ref


class RevenueAdapter:
    """Mock Revenue/TNeGA/PMFBY record lookup by ration or survey number."""

    def lookup(self, ration_id: str | None) -> dict | None:
        return None


otp = OtpAdapter()
notify = NotifyAdapter()
payment = PaymentAdapter()
revenue = RevenueAdapter()
