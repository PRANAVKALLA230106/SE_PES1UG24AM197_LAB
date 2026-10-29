import pytest
from movie_tickets import SEAT_PRICE, ticket_price, group_discount, snack_combo


# ---------- ticket_price: invalid inputs ----------

@pytest.mark.parametrize("seat", ["vip", "", "Regular", None])
def test_unknown_seat_raises(seat):
    with pytest.raises(ValueError, match="unknown seat"):
        ticket_price(seat, 25, 15, False)


@pytest.mark.parametrize("hour", [-1, 24, -100, 100])
def test_invalid_show_hour_raises(hour):
    with pytest.raises(ValueError, match="invalid show time"):
        ticket_price("regular", 25, hour, False)


def test_seat_checked_before_hour():
    with pytest.raises(ValueError, match="unknown seat"):
        ticket_price("vip", 25, 99, False)


# ---------- ticket_price: base prices and time of day ----------

@pytest.mark.parametrize("seat", list(SEAT_PRICE))
def test_afternoon_base_price(seat):
    assert ticket_price(seat, 25, 15, False) == SEAT_PRICE[seat]


@pytest.mark.parametrize("seat,expected", [("regular", 100), ("premium", 200), ("recliner", 350)])
def test_morning_discount(seat, expected):
    assert ticket_price(seat, 25, 10, False) == expected


@pytest.mark.parametrize("seat,expected", [("regular", 180), ("premium", 280), ("recliner", 430)])
def test_evening_surcharge(seat, expected):
    assert ticket_price(seat, 25, 20, False) == expected


@pytest.mark.parametrize("hour,expected", [
    (0, 100),   # lowest valid hour -> morning
    (11, 100),  # last morning hour
    (12, 150),  # first afternoon hour
    (17, 150),  # last afternoon hour
    (18, 180),  # first evening hour
    (23, 180),  # highest valid hour
])
def test_show_hour_boundaries(hour, expected):
    assert ticket_price("regular", 25, hour, False) == expected


# ---------- ticket_price: weekend ----------

def test_weekend_afternoon():
    assert ticket_price("regular", 25, 15, True) == 190


def test_weekend_morning():
    assert ticket_price("premium", 25, 9, True) == 240


def test_weekend_evening():
    assert ticket_price("recliner", 25, 21, True) == 470


# ---------- ticket_price: age rules ----------

@pytest.mark.parametrize("age", [0, 1, 2])
def test_infants_free(age):
    assert ticket_price("recliner", age, 20, True) == 0


def test_negative_age_is_free():
    assert ticket_price("regular", -5, 15, False) == 0


@pytest.mark.parametrize("age", [3, 12])
def test_child_half_price_boundaries(age):
    assert ticket_price("regular", age, 15, False) == 75


@pytest.mark.parametrize("age", [13, 59])
def test_adult_full_price_boundaries(age):
    assert ticket_price("regular", age, 15, False) == 150


@pytest.mark.parametrize("age", [60, 85])
def test_senior_half_price(age):
    assert ticket_price("regular", age, 15, False) == 75


def test_half_price_uses_floor_division():
    # premium morning weekend: 250 - 50 + 40 = 240 -> 120
    assert ticket_price("premium", 8, 9, True) == 120
    # regular morning: 100 -> 50; regular evening weekend: 220 -> 110
    assert ticket_price("regular", 70, 5, False) == 50
    assert ticket_price("regular", 70, 19, True) == 110


def test_float_age_just_below_three_is_free():
    assert ticket_price("regular", 2.9, 15, False) == 0


# ---------- group_discount ----------

@pytest.mark.parametrize("tickets", [0, -1, -10])
def test_group_no_tickets_raises(tickets):
    with pytest.raises(ValueError, match="no tickets"):
        group_discount(tickets, False)


@pytest.mark.parametrize("tickets", [1, 2, 4])
def test_small_group_no_discount(tickets):
    assert group_discount(tickets, False) == 0


@pytest.mark.parametrize("tickets", [1, 4])
def test_small_student_group_gets_no_bonus(tickets):
    assert group_discount(tickets, True) == 0


@pytest.mark.parametrize("tickets", [5, 9])
def test_medium_group(tickets):
    assert group_discount(tickets, False) == 10


@pytest.mark.parametrize("tickets", [5, 9])
def test_medium_student_group(tickets):
    assert group_discount(tickets, True) == 15


@pytest.mark.parametrize("tickets", [10, 50])
def test_large_group(tickets):
    assert group_discount(tickets, False) == 15


@pytest.mark.parametrize("tickets", [10, 50])
def test_large_student_group(tickets):
    assert group_discount(tickets, True) == 20


# ---------- snack_combo ----------

@pytest.mark.parametrize("size,expected", [("small", 120), ("medium", 180), ("large", 250)])
def test_snack_without_coupon(size, expected):
    assert snack_combo(size, False) == expected


@pytest.mark.parametrize("size,expected", [("small", 70), ("medium", 130), ("large", 200)])
def test_snack_with_coupon(size, expected):
    assert snack_combo(size, True) == expected


@pytest.mark.parametrize("size", ["", "Small", "extra-large", None])
def test_snack_unknown_size_defaults_to_large(size):
    assert snack_combo(size, False) == 250
