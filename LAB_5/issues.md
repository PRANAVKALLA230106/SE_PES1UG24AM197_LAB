# Static Analysis Issues — Museum Artifact Catalog

Line numbers refer to the original file, `before/museum_catalog_original.py`.
Issues are ordered by severity: Bandit Medium, then Bandit Low, then Pylint
warnings/refactors, then style conventions. No tool reported a High-severity issue.
Where Pylint and Flake8 reported the same problem, both codes are listed in one row.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| SQL injection (Bandit B608, Medium) | Security | 11 | `addArtifact` built the `INSERT` statement by concatenating `title` and `era` into the SQL string, so a title such as `x'); DROP TABLE artifacts; --` could alter the query. | Replaced string building with a parameterised query: `VALUES (?, ?, ?, ?)` with the values passed as a tuple to `conn.execute`. |
| Hardcoded password (Bandit B105, Low) | Security | 7 | `CURATOR_PASSWORD = "m4seum!"` stored a credential in source code, where it ends up in version control. | Read it from the environment instead: `os.environ.get("CURATOR_PASSWORD", "")`. |
| Subprocess with `shell=True` (Bandit B602, Low) | Security | 37 | `subprocess.call("echo ...", shell=True)` runs the command through a shell, which becomes command injection if any input is ever added to the string. | Removed the subprocess call; `backup_note()` now uses `print("catalog backup complete")`, which produces the same output. |
| Process started with partial path (Bandit B607, Low) | Security | 37 | `echo` was resolved via `PATH`, so a malicious executable earlier on `PATH` could be run instead. | Fixed by the same change as B602: no external process is started any more. |
| `subprocess` import (Bandit B404, Low) | Security | 3 | Importing `subprocess` flags the module for review because of its command-execution risks. | Removed the import once `subprocess` was no longer used (replaced by `import os` for the environment lookup). |
| Unused argument `curator` (Pylint W0613) | Warning | 15 | `displayStatus(artifact_id, curator)` never used `curator`. | Removed the parameter and updated the only caller in `main()`. |
| Unused import `datetime` (Pylint W0611, Flake8 F401) | Warning | 2 | `datetime` was imported but never used. | Deleted the import. |
| Unnecessary `else` after `return` (Pylint R1705) | Refactor | 17–20 | The `else:` branch in `displayStatus` was redundant because the `if` branch returns. | Removed the `else` and de-indented `return "in storage"`. |
| Function names not snake_case (Pylint C0103) | Convention | 10, 15, 24, 31, 36 | `addArtifact`, `displayStatus`, `totalValue`, `moveToDisplay`, `backupNote` used camelCase, contrary to PEP 8. | Renamed to `add_artifact`, `display_status`, `total_value`, `move_to_display`, `backup_note` and updated every call. |
| Missing module docstring (Pylint C0114) | Convention | 1 | The file had no description of its purpose. | Added a one-line module docstring. |
| Missing function docstrings (Pylint C0116) | Convention | 10, 15, 24, 31, 36, 40 | None of the six functions were documented. | Added a one-line docstring to each function. |
| Line too long (Pylint C0301, Flake8 E501) | Style | 6, 11, 16, 26, 32 | Lines were up to 158 characters (Pylint limit 100, Flake8 limit 79). Pylint flagged lines 6 and 11; Flake8 flagged all five. | Split long SQL strings using implicit string concatenation, wrapped `conn.execute(...)` calls across lines, and stored the query result in a `rows` variable in `total_value`. |
| Too many blank lines (Flake8 E303) | Style | 24 | Three blank lines before `totalValue` instead of two. | Reduced to the standard two blank lines between top-level definitions. |
| Missing whitespace around operator (Flake8 E225) | Style | 25 | `total=0` had no spaces around `=`. | Changed to `total = 0`. |

One further change was made that no tool required: the bare `main()` call at the end
of the file was wrapped in `if __name__ == "__main__":` so the module can be imported
without running the demonstration.

## Before vs after

| Metric | Before | After |
|--------|--------|-------|
| Pylint score | 4.85/10 (17 messages) | 10.00/10 (0 messages) |
| Bandit issues | 5 (Medium: 1, Low: 4; High: 0) | 0 |
| Flake8 issues | 8 | 0 |
| Program output | `on display`, `135000`, `catalog backup complete` | Same |

Full reports are in `before/` and `after/`; the final code is also saved as
`after/museum_catalog_fixed.py`.
