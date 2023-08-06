# Changelog

All notable changes to this project will be documented in this file.

The format mostly follows [Keep a Changelog](http://keepachangelog.com/en/1.0.0/).

## [Unreleased]


## [2.15] -- 2018-10-23

### Added
- Support for Mailgun regions (by Daniel Peukert, PR#280)
- CLI: Allow multiple occurences of 'filter' when adding jobs (PR#278)

### Changed
- Fixed incorrect name for chat_id config in the default config (by Robin B, PR#276)


## [2.14] -- 2018-08-30

### Added
- Filter to pretty-print JSON data: `format-json` (by Niko Böckerman, PR#250)
- List active Telegram chats using `--telegram-chats` (with fixes by Georg Pichler, PR#270)
- Support for HTTP `ETag` header in URL jobs and `If-None-Match` (by Karol Babioch, PR#256)
- Support for filtering HTML using XPath expressions, with `lxml` (PR#274, Fixes #226)
- Added `install_dependencies` to `setup.py` commands for easy installing of dependencies
- Added `ignore_connection_errors` per-job configuration option (by Karol Babioch, PR#261)

### Changed
- Improved code (HTTP status codes, by Karol Babioch PR#258)
- Improved documentation for setting up Telegram chat bots
- Allow multiple chats for Telegram reporting (by Georg Pichler, PR#271)


## [2.13] -- 2018-06-03

### Added
- Support for specifying a `diff_tool` (e.g. `wdiff`) for each job (Fixes #243)
- Support for testing filters via `--test-filter JOB` (Fixes #237)

### Changed
- Moved ChangeLog file to CHANGELOG.md and using Keep a Changelog format.
- Force version check in `setup.py`, to exclude Python 2 (Fixes #244)
- Remove default parameter from internal `html2text` module (Fixes #239)
- Better error/exception reporting in `--verbose` mode (Fixes #164)

### Removed
- Old ChangeLog entries


## [2.12] -- 2018-06-01

### Fixed
- Bugfix: Do not 'forget' old data if an exception occurs (Fixes #242)


## [2.11] -- 2018-05-19

### Fixed
- Retry: Make sure `tries` is initialized to zero on load (Fixes #241)

### Changed
- html2text: Make sure the bs4 method strips HTML tags (by Louis Sautier)


## [2.10] -- 2018-05-17

### Added
- Browser: Add support for browser jobs using `requests-html` (Fixes #215)
- Retry: Add support for optional retry count in job list (by cmichi, fixes #235)
- HTTP: Add support for specifying optional headers (by Tero Mononen)

### Changed
- File editing: Fix issue when `$EDITOR` contains spaces (Fixes #220)
- ChangeLog: Add versions to recent ChangeLog entries (Fixes #235)


## [2.9] -- 2018-03-24

### Added
- E-Mail: Add support for `--smtp-login` and document GMail SMTP usage
- Pushover: Device and sound attribute (by Tobias Haupenthal)

### Changed
- XDG: Move cache file to `XDG_CACHE_DIR` (by Maxime Werlen)
- Migration: Unconditionally migrate urlwatch 1.x cache dirs (Fixes #206)

### Fixed
- Cleanups: Fix out-of-date debug message, use https (by Jakub Wilk)


## [2.8] -- 2018-01-28

### Changed
- Documentation: Mention `appdirs` (by e-dschungel)

### Fixed
- SMTP: Fix handling of missing `user` field (by e-dschungel)
- Manpage: Fix documentation of XDG environment variables (by Jelle van der Waa)
- Unit tests: Fix imports for out-of-source-tree tests (by Maxime Werlen)


## [2.7] -- 2017-11-08

### Added
- Filtering: `style` (by gvandenbroucke), `tag` (by cmichi)
- New reporter: Telegram support (by gvandenbroucke)
- Paths: Add `XDG_CONFIG_DIR` support (by Jelle van der Waa)

### Changed
- ElementsByAttribute: look for matching tag in handle_endtag (by Gaetan Leurent)
- HTTP: Option to avoid 304 responses, `Content-Type` header (by Vinicius Massuchetto)
- html2text: Configuration options (by Vinicius Massuchetto)

### Fixed
- Issue #127: Fix error reporting
- E-Mail: Fix encodings (by Seokjin Han), Allow `user` parameter for SMTP (by Jay Sitter)


## [2.6] -- 2016-12-04

### Added
- New filters: `sha1sum`, `hexdump`, `element-by-class`
- New reporters: pushbullet (by R0nd); mailgun (by lechuckcaptain)

### Changed
- Improved filters: `BeautifulSoup` support for `html2txt` (by lechuckcaptain)
- Improved handlers: HTTP Proxy (by lechuckcaptain); support for `file://` URIs
- CI Integration: Build configuration for Travis CI (by lechuckcaptain)
- Consistency: Feature list is now sorted by name

### Fixed
- Issue #108: Fix creation of example files on first startup
- Issue #118: Fix match filters for missing keys
- Small fixes by: Jakub Wilk, Marc Urben, Adam Dobrawy and Louis Sautier


Older ChangeLog entries can be found in the
[old ChangeLog file](https://github.com/thp/urlwatch/blob/2.12/ChangeLog),
or with `git show 2.12:ChangeLog` on the command line.
