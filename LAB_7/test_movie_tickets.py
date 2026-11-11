"""Lab 7: Hypothesis fuzz tests for movie_tickets.py."""
from hypothesis import given, settings, strategies as st

from movie_tickets import parse_seat, total_price, average_rating

# ---------------------------------------------------------------------------
# 1. "No crash" fuzz tests: random text (or None) must never raise.
# ---------------------------------------------------------------------------


@settings(max_examples=500)
@given(st.text() | st.none())
def test_parse_seat_no_crash(s):
    try:
        parse_seat(s)
    except Exception as e:
        assert False, f"parse_seat crashed on {s!r} with: {e!r}"


@settings(max_examples=500)
@given(st.text() | st.none())
def test_total_price_no_crash(s):
    try:
        total_price(s)
    except Exception as e:
        assert False, f"total_price crashed on {s!r} with: {e!r}"


@settings(max_examples=500)
@given(st.text() | st.none())
def test_average_rating_no_crash(s):
    try:
        average_rating(s)
    except Exception as e:
        assert False, f"average_rating crashed on {s!r} with: {e!r}"


# ---------------------------------------------------------------------------
# 2. Targeted fuzzing: inputs that *look* almost valid (the interesting
#    edge cases: empty fields, signs, spaces, odd separators, non-ASCII).
# ---------------------------------------------------------------------------

seat_like = st.from_regex(r"\A[A-Za-z0-9 \-+_.ßı١٢]{0,6}\Z")
csv_like = st.from_regex(r"\A[0-9,\- .a]{0,15}\Z")
ratings_like = st.from_regex(r"\A[0-9 \-.x]{0,12}\Z")


@given(seat_like)
def test_parse_seat_seat_like_inputs(s):
    result = parse_seat(s)
    if result is not None:
        row, num = result
        assert len(row) == 1 and "A" <= row <= "Z"
        assert isinstance(num, int) and num > 0


@given(csv_like)
def test_total_price_csv_like_inputs(s):
    result = total_price(s)
    if result is not None:
        assert result >= 0


@given(ratings_like)
def test_average_rating_ratings_like_inputs(s):
    result = average_rating(s)
    if result is not None:
        assert 1 <= result <= 5


# ---------------------------------------------------------------------------
# 3. Properties on valid inputs: the function must still give the right answer.
# ---------------------------------------------------------------------------


@given(
    st.sampled_from("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"),
    st.integers(min_value=1, max_value=999),
)
def test_parse_seat_valid(row, num):
    assert parse_seat(f"{row}{num}") == (row.upper(), num)


@given(st.lists(st.integers(min_value=0, max_value=10_000), min_size=1, max_size=20))
def test_total_price_valid(prices):
    csv = ",".join(str(p) for p in prices)
    assert total_price(csv) == round(sum(prices) * 1.18, 2)


@given(st.lists(st.integers(min_value=1, max_value=5), min_size=1, max_size=20))
def test_average_rating_valid(ratings):
    text = " ".join(str(r) for r in ratings)
    assert average_rating(text) == round(sum(ratings) / len(ratings), 1)
