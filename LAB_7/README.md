# Lab 7: Fuzz Testing (Hypothesis)

Assigned repo: `SETAPESU26/L6_L7_15_movie_tickets` (Lab 7)

| File | Description |
|------|-------------|
| `movie_tickets.py` | Fixed application (all inputs validated, returns `None` for invalid input) |
| `test_movie_tickets.py` | Completed Hypothesis fuzz tests (9 tests) |
| `Lab7_FuzzTesting_PES1UG24AM197.pdf` | Report with screenshots for steps 2, 4, 5 and 6 |
| `screenshots/` | Screenshots used in the report |

Run:
```
pip install hypothesis pytest
python movie_tickets.py
python -m pytest test_movie_tickets.py -v
```
