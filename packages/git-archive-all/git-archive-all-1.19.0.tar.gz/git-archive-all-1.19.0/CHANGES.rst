CHANGES
=======

1.19.0 (2018-10-31)
-------------------

- 🎃
- Use -0 ... -9 to explicitly specify compression level if format allows; if unset, lib's default is used
- Checking for file exclusion is optimized, the process is spawned only once per repo / submodule

1.18.3 (2018-09-27)
-------------------

- Fix broken support for zip files

1.18.2 (2018-09-19)
-------------------

- Fix redundant print
- Fix mismatch between dry-run and normal verbose logging
- Fix missing support for tbz2 files
- API: Raise ValueError instead of RuntimeError if output format is not recognized
- API: Conditionally import zipfile / tarfile depending on requested output format

1.18.1 (2018-09-01)
-------------------

- Improve support for special characters

1.18.0 (2018-08-14)
-------------------

- Add **CHANGES.rst** to track further changes
- Add tests
- Use `git check-attr` to test against export-ignore
- Better support for unicode file names
- Require Git >= 1.6.1
