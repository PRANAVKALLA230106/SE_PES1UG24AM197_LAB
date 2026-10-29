"""Branch coverage tests for movie_tickets.py.

Every decision is exercised for both its True and False outcome, with
boundary values placed exactly on (and just either side of) each threshold.
"""
import pytest
from movie_tickets import SEAT_PRICE, ticket_price, group_discount, snack_combo


# ======================= ticket_price =======================

# --- Decision 1: seat not in SEAT_PRICE ---

@pytest.mark.parametrize("seat", ["vip", "", "Regular", "REGULAR", " regular", None, 0])
def test_seat_unknown_true_raises(seat):
    with pytest.raises(ValueError, match="unknown seat"):
        ticket_price(seat, 25, 15, False)


@pytest.mark.parametrize("seat", list(SEAT_PRICE))
def test_seat_unknown_false_known_seats(seat):
    assert ticket_price(seat, 25, 15, False) == SEAT_PRICE[seat]


def test_seat_is_checked_before_show_hour():
    with pytest.raises(ValueError, match="unknown seat"):
        ticket_price("vip", 25, -5, False)


def test_unhashable_seat_raises_type_error():
    with pytest.raises(TypeError):
        ticket_price(["regular"], 25, 15, False)


# --- Decision 2: show_hour < 0 or show_hour > 23 ---

@pytest.mark.parametrize("hour", [-1, -100])
def test_show_hour_below_zero_raises(hour):
    # first operand True (short-circuits)
    with pytest.raises(ValueError, match="invalid show time"):
        ticket_price("regular", 25, hour, False)


@pytest.mark.parametrize("hour", [24, 100])
def test_show_hour_above_23_raises(hour):
    # first operand False, second operand True
    with pytest.raises(ValueError, match="invalid show time"):
        ticket_price("regular", 25, hour, False)


@pytest.mark.parametrize("hour,expected", [(0, 100), (23, 180)])
def test_show_hour_boundaries_are_valid(hour, expected):
    # both operands False at the exact edges
    assert ticket_price("regular", 25, hour, False) == expected


def test_non_numeric_show_hour_raises_type_error():
    with pytest.raises(TypeError):
        ticket_price("regular", 25, "noon", False)


# --- Decision 3/4: show_hour < 12 / elif show_hour >= 18 / implicit else ---

@pytest.mark.parametrize("hour", [0, 6, 11])
def test_morning_branch(hour):
    assert ticket_price("regular", 25, hour, False) == 100


@pytest.mark.parametrize("hour", [12, 15, 17])
def test_afternoon_neither_branch(hour):
    # hour < 12 False and hour >= 18 False
    assert ticket_price("regular", 25, hour, False) == 150


@pytest.mark.parametrize("hour", [18, 20, 23])
def test_evening_branch(hour):
    assert ticket_price("regular", 25, hour, False) == 180


@pytest.mark.parametrize("seat,morning,afternoon,evening", [
    ("regular", 100, 150, 180),
    ("premium", 200, 250, 280),
    ("recliner", 350, 400, 430),
])
def test_time_of_day_for_every_seat(seat, morning, afternoon, evening):
    assert ticket_price(seat, 25, 11, False) == morning
    assert ticket_price(seat, 25, 12, False) == afternoon
    assert ticket_price(seat, 25, 18, False) == evening


# --- Decision 5: is_weekend ---

@pytest.mark.parametrize("weekend,expected", [(True, 190), (False, 150), (1, 190), (0, 150)])
def test_weekend_true_and_false(weekend, expected):
    assert ticket_price("regular", 25, 15, weekend) == expected


@pytest.mark.parametrize("hour,expected", [(10, 140), (15, 190), (20, 220)])
def test_weekend_combined_with_time_of_day(hour, expected):
    assert ticket_price("regular", 25, hour, True) == expected


# --- Decision 6: age < 3 ---

@pytest.mark.parametrize("age", [0, 1, 2])
def test_infant_is_free(age):
    assert ticket_price("recliner", age, 20, True) == 0


def test_age_three_is_not_free():
    # age < 3 False at the boundary; falls into child half price
    assert ticket_price("regular", 3, 15, False) == 75


def test_negative_age_is_free():
    assert ticket_price("regular", -1, 15, False) == 0


# --- Decision 7: age <= 12 or age >= 60 ---

@pytest.mark.parametrize("age", [3, 5, 12])
def test_child_half_price(age):
    # first operand True
    assert ticket_price("regular", age, 15, False) == 75


@pytest.mark.parametrize("age", [60, 75, 100])
def test_senior_half_price(age):
    # first operand False, second True
    assert ticket_price("regular", age, 15, False) == 75


@pytest.mark.parametrize("age", [13, 30, 59])
def test_adult_full_price(age):
    # both operands False
    assert ticket_price("regular", age, 15, False) == 150


def test_half_price_uses_floor_division():
    # 150 - 50 + 40 = 140 -> 70 ; 250 + 30 + 40 = 320 -> 160
    assert ticket_price("regular", 10, 9, True) == 70
    assert ticket_price("premium", 65, 19, True) == 160
    # odd total: recliner 400 - 50 = 350 -> 175
    assert ticket_price("recliner", 12, 11, False) == 175


def test_all_flags_combined_adult():
    assert ticket_price("recliner", 40, 23, True) == 470


# ======================= group_discount =======================

# --- Decision 1: tickets < 1 ---

@pytest.mark.parametrize("tickets", [0, -1, -50])
def test_no_tickets_raises(tickets):
    with pytest.raises(ValueError, match="no tickets"):
        group_discount(tickets, False)


def test_no_tickets_raises_even_for_student_group():
    with pytest.raises(ValueError, match="no tickets"):
        group_discount(0, True)


def test_non_numeric_tickets_raises_type_error():
    with pytest.raises(TypeError):
        group_discount("five", False)


# --- Decision 2/3: tickets >= 10 / elif tickets >= 5 / else ---

@pytest.mark.parametrize("tickets,expected", [
    (1, 0), (4, 0),        # else branch, boundary just below 5
    (5, 10), (9, 10),      # elif branch, edges
    (10, 15), (50, 15),    # first branch, boundary at 10
])
def test_discount_tiers_non_student(tickets, expected):
    assert group_discount(tickets, False) == expected


# --- Decision 4: is_student_group and discount > 0 ---

@pytest.mark.parametrize("tickets,expected", [(5, 15), (9, 15), (10, 20), (100, 20)])
def test_student_bonus_applied(tickets, expected):
    # both operands True
    assert group_discount(tickets, True) == expected


@pytest.mark.parametrize("tickets", [1, 4])
def test_student_no_bonus_without_base_discount(tickets):
    # first operand True, second False
    assert group_discount(tickets, True) == 0


@pytest.mark.parametrize("tickets,expected", [(4, 0), (5, 10), (10, 15)])
def test_non_student_never_gets_bonus(tickets, expected):
    # first operand False (short-circuits)
    assert group_discount(tickets, False) == expected


# ======================= snack_combo =======================

# --- Decision 1/2: size == "small" / elif "medium" / else ---

@pytest.mark.parametrize("size,expected", [
    ("small", 120),
    ("medium", 180),
    ("large", 250),
])
def test_snack_sizes_no_coupon(size, expected):
    assert snack_combo(size, False) == expected


@pytest.mark.parametrize("size", ["Small", "MEDIUM", "", "xl", None, 1])
def test_unrecognised_size_falls_to_else(size):
    assert snack_combo(size, False) == 250


# --- Decision 3: has_coupon ---

@pytest.mark.parametrize("size,expected", [
    ("small", 70),
    ("medium", 130),
    ("large", 200),
])
def test_snack_sizes_with_coupon(size, expected):
    assert snack_combo(size, True) == expected


def test_coupon_on_unknown_size():
    assert snack_combo("jumbo", True) == 200
