"""Lab 7: fixed (hardened) version of movie_tickets.py.

Every function validates its input and returns None for anything invalid
instead of raising an exception.
"""

GST_RATE = 1.18
MIN_RATING = 1
MAX_RATING = 5


def _is_plain_number(text):
    """True only for non-empty ASCII digit strings like '150' (no sign, no
    spaces, no Unicode digits such as '١٢')."""
    return text.isascii() and text.isdigit()


def parse_seat(seat):
    """'H12' -> ('H', 12). Returns None for invalid seats."""
    if not isinstance(seat, str):
        return None
    seat = seat.strip()
    if len(seat) < 2:                      # need a row letter and a number
        return None
    row, number = seat[0], seat[1:]
    if not (row.isascii() and row.isalpha()):   # 'ß'.upper() == 'SS', '1' etc.
        return None
    if not _is_plain_number(number):       # rejects '', '-1', ' 12', '1.5'
        return None
    number = int(number)
    if number <= 0:                        # seat 0 does not exist
        return None
    return row.upper(), number


def total_price(prices_csv):
    """'150,250,400' -> total incl. 18% GST. Returns None for invalid input."""
    if not isinstance(prices_csv, str):
        return None
    parts = [p.strip() for p in prices_csv.split(",")]
    if not parts or any(not _is_plain_number(p) for p in parts):
        return None                        # empty field, negatives, letters
    prices = [int(p) for p in parts]
    return round(sum(prices) * GST_RATE, 2)


def average_rating(ratings):
    """'4 5 3' -> 4.0. Ratings must be whole numbers from 1 to 5.
    Returns None for invalid input."""
    if not isinstance(ratings, str):
        return None
    parts = ratings.split()
    if not parts:                          # avoids ZeroDivisionError
        return None
    if any(not _is_plain_number(p) for p in parts):
        return None
    values = [int(p) for p in parts]
    if any(v < MIN_RATING or v > MAX_RATING for v in values):
        return None
    return round(sum(values) / len(values), 1)


def _show(label, result):
    if result is None:
        print(f"{label}: Invalid input")
    else:
        print(f"{label}:", result)


def main():
    print("==== Running parse_seat ====")
    user_input = input("Enter a seat number (e.g. H12): ")
    _show("Row and Seat", parse_seat(user_input))

    print("\n==== Running total_price ====")
    user_input = input("Enter ticket prices as CSV (e.g. 150,250,400): ")
    _show("Total with GST", total_price(user_input))

    print("\n==== Running average_rating ====")
    user_input = input("Enter ratings separated by spaces (e.g. 4 5 3): ")
    _show("Average Rating", average_rating(user_input))


if __name__ == "__main__":
    main()
