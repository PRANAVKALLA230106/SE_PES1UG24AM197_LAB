# Reflection — Static Code Analysis Lab

## 1. Which issues were the easiest and hardest to fix, and why?

**Easiest:** the purely mechanical ones. Deleting the unused `datetime` import
(W0611 / F401), changing `total=0` to `total = 0` (E225), removing an extra blank line
(E303), and removing the `else` after `return` (R1705) each took one small edit, could
not change behaviour, and the tool message said exactly what to do.

**Hardest:** two kinds of issue needed more thought than the message suggested.

- **The SQL injection (B608).** This was the most important fix, but it needed an
  understanding of *why* string concatenation is dangerous and how parameter binding
  works in `sqlite3`. The rewrite also had to keep the same behaviour: the original
  converted `value` and `on_display` with `str()`, while the parameterised version passes
  the integers directly, which SQLite stores the same way.
- **Line length (C0301 / E501).** This took two passes. Pylint's limit is 100
  characters and Flake8's is 79, so the lines I wrapped to satisfy Pylint were still too
  long for Flake8. Wrapping SQL strings readably (implicit string concatenation,
  breaking `conn.execute(...)` calls across lines) was more fiddly than any other style
  fix.

The renames (C0103) and the removed `curator` parameter (W0613) were simple to type
but change the module's public interface, so every caller had to be checked. In this
project the only caller was `main()`; in a larger codebase that would be a bigger job.

## 2. Did the tools report any false positives or issues you chose not to fix?

I fixed every reported issue, but several Bandit findings were low risk *in this
specific code*:

- **B602 / B607 (`shell=True`, partial path):** the command was a fixed string,
  `"echo catalog backup complete"`, with no user input, so there was no real injection
  path today. Bandit itself says the call "seems safe". I still removed it, because
  starting a shell just to print a line is unnecessary, and `print()` gives the same
  output.
- **B404 (`import subprocess`):** this is informational. Importing the module is not a
  vulnerability; it only marks the file for review.
- **B105 (hardcoded password):** `CURATOR_PASSWORD` is never actually used by the
  program, so nothing was exposed at runtime. It was still a real problem, because the
  secret would be committed to version control.

There are also things the tools **did not** catch, which I deliberately left alone to
keep behaviour unchanged:

- `CURATOR_PASSWORD` is still unused. No tool flags an unused module-level constant.
- `display_status()` crashes with a `TypeError` if the artifact ID does not exist,
  because `fetchone()` returns `None`. This is a logic bug that static analysis does not
  detect.

## 3. How would you integrate static analysis into your regular development workflow?

- **Editor:** enable Pylint and Flake8 in the IDE so problems are underlined while
  typing, which is the cheapest moment to fix them.
- **Pre-commit hooks:** use the `pre-commit` framework to run Flake8 and Bandit (fast)
  on staged files before every commit, so badly styled or obviously insecure code never
  enters the history.
- **CI pipeline:** run all three tools on every push or pull request (for example in a
  GitHub Actions job) and fail the build if Bandit reports any Medium/High issue,
  Flake8 reports anything, or the Pylint score falls below a threshold such as 9.5
  (`pylint --fail-under=9.5`).
- **Shared configuration:** keep the settings in one committed file
  (`pyproject.toml` or `setup.cfg`). In particular, set the same maximum line length for
  Pylint and Flake8, which would have avoided the two-pass line-length fix in this lab.
- **Saved reports:** keep before/after reports, as in this lab, so improvements can be
  tracked over time and a regression is easy to spot.

## 4. What tangible improvements did you observe after the fixes?

- **Security:** the SQL injection hole is closed; user-supplied titles and eras are now
  treated as data, never as SQL. The password is no longer in the source code, and the
  program no longer starts a shell. Bandit went from 5 issues (1 Medium, 4 Low) to 0.
- **Readability:** PEP 8 snake_case names, a docstring on the module and on every
  function, and lines short enough to read without scrolling. Removing the redundant
  `else` makes `display_status` shorter and its logic clearer.
- **Maintainability:** dead code is gone (the `datetime` import and the `curator`
  argument), and the `if __name__ == "__main__":` guard means the functions can be
  imported and tested without running the demonstration.
- **Measured results:** Pylint went from 4.85/10 to 10.00/10, Flake8 from 8 issues to 0,
  and the program's output (`on display`, `135000`, `catalog backup complete`) is
  unchanged.
