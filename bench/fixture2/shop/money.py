from decimal import ROUND_HALF_UP, Decimal


def round_money(value):
    """Round half up to two decimals."""
    return float(Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def fmt(value):
    return f"{value:.2f}"
