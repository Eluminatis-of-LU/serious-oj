# Good First Issues for Serious-OJ Contributors

This document collects beginner-friendly issues for new contributors to get started with the Serious-OJ project. Each issue is well-scoped and provides a clear entry point into the codebase.

---

## Table of Contents

1. [Bug Fixes](#bug-fixes)
2. [Frontend / UI Improvements](#frontend--ui-improvements)
3. [Backend / Python Improvements](#backend--python-improvements)
4. [Documentation](#documentation)
5. [Tests](#tests)
6. [Code Quality](#code-quality)

---

## Bug Fixes

### 1. Fix Duplicate Class Name in `misc.py`
- **File:** `vj4/handler/misc.py`
- **Description:** There are two handler classes both named `AboutHandler`. The second one (line 13) handles `/wiki/help` and should be renamed to `WikiHelpHandler` to avoid shadowing and confusion.
- **Skills:** Python
- **Difficulty:** Very Easy

### 2. Fix `timeago_locale` in Bengali Translation
- **File:** `vj4/locale/bn.yaml`
- **Description:** The Bengali locale file has `timeago_locale: en_US` (line 62). It should be updated to a proper Bengali locale code if available, or documented why it falls back to `en_US`.
- **Skills:** YAML, i18n
- **Difficulty:** Very Easy

---

## Frontend / UI Improvements

### 3. Implement Keyboard Navigation for Autocomplete
- **File:** `vj4/ui/components/autocomplete/index.js`
- **Description:** The `onKeyDown()` method (line 78) is empty with a `// TODO: Implement keyboard navigation` comment. Add keyboard support (Up/Down arrows to navigate items, Enter to select, Escape to close) for better accessibility and UX.
- **Skills:** JavaScript, ES6
- **Difficulty:** Easy

### 4. Add User Notification on Star/Vote Failure
- **Files:** `vj4/ui/components/star/star.page.js` (line 25), `vj4/ui/components/vote/vote.page.js` (line 32)
- **Description:** Both star and vote actions have `// TODO: notify failure` in their `.catch()` handlers. When the API request fails, the UI silently reverts. Add a toast/notification to inform the user that the action failed.
- **Skills:** JavaScript
- **Difficulty:** Easy

### 5. Replace Raw HTML Forms with `form_builder` in Templates
- **Files:** `vj4/ui/templates/problem_main.html` (line 49), `vj4/ui/templates/record_main.html` (line 21)
- **Description:** Both templates have `<!-- TODO: replace with form_builder -->` comments where raw HTML form inputs are used. Refactor them to use the project's `form_builder` component for consistency.
- **Skills:** HTML, Jinja2
- **Difficulty:** Easy

### 6. Remove or Implement Placeholder TODO in `training_detail.html`
- **File:** `vj4/ui/templates/training_detail.html` (line 51)
- **Description:** There is a commented-out block with `TODO(twd2): twd2 todo` showing training section statistics (submission count, completion rank). Either implement the feature by passing the required data from the handler, or remove the dead code if it's no longer planned.
- **Skills:** HTML, Jinja2, Python
- **Difficulty:** Medium

---

## Backend / Python Improvements

### 7. Add Missing Validation Check Tests
- **File:** `vj4/test/test_validator.py`
- **Description:** The test file covers `is_*` functions but does not test the corresponding `check_*` functions that raise `ValidationError`. Add tests for:
  - `check_uid`
  - `check_uname`
  - `check_password`
  - `check_mail`
  - `check_domain_id`
  - `check_title`
  - `check_name`
  - `check_content`
  - `check_intro`
  - `check_description`
  - `check_bulletin`
  - `check_category_name`
  - `check_node_name`
  - `check_role`
  - `check_domain_invitation_code`
  - `check_lang`
  - `check_lang_alltime`
- **Skills:** Python, `unittest`
- **Difficulty:** Easy

### 8. Complete Rejudge Test Case in `test_job.py`
- **File:** `vj4/test/test_job.py` (line 32)
- **Description:** There is a comment `# first judge, WA. rejudge, TODO(twd2)` indicating that a test scenario for rejudging a record (WA → AC) is missing. Add a test that creates a record, judges it as WA, then rejudges it as AC and verifies the updated statistics.
- **Skills:** Python, `unittest`, async/await
- **Difficulty:** Medium

### 9. Add Tests for Missing Handler Modules
- **Description:** There are ~125 handler classes but tests only exist for a subset. Consider adding tests for handlers that currently have no coverage:
  - `vj4/handler/ranking.py`
  - `vj4/handler/rating.py`
  - `vj4/handler/fs.py`
  - `vj4/handler/misc.py`
  - `vj4/handler/training.py`
  - `vj4/handler/homework.py`
- **Skills:** Python, `unittest`, async/await
- **Difficulty:** Medium

---

## Documentation

### 10. Fill in TODO Placeholders in UI Framework README
- **File:** `vj4/ui/README.md`
- **Description:** The UI framework documentation has many `TODO` placeholders for undocumented components:
  - Media Object (line 54)
  - Number Box Object (line 58)
  - Balancer Object (line 62)
  - Button `inverse` modifier (line 199)
  - Input `material` modifier (line 211)
  - Input `inverse` modifier (line 213)
  - Paginator (line 217)
  - Dropdown (line 322)
  - Navigation (line 326)
  - Star (line 330)
  - Tab (line 334)
  - Comment List (line 399)
- **Skills:** Markdown, UI/UX
- **Difficulty:** Easy

### 11. Document Problem Categories
- **File:** `vj4/model/builtin.py` (lines 537–551)
- **Description:** The `PROBLEM_CATEGORIES` dict defines the problem taxonomy. Add a brief comment or documentation explaining how to add new categories/sub-categories and what constraints apply (no spaces, no commas, uniqueness).
- **Skills:** Python
- **Difficulty:** Very Easy

---

## Code Quality

### 12. Remove or Verify Outdated FIXME in `fs.py`
- **File:** `vj4/handler/fs.py` (line 26)
- **Description:** There is a `# FIXME(iceboy): For some reason setting response.content_length doesn't work in aiohttp 2.0.6.` comment. The project now uses `aiohttp>=3.13.4`. Verify whether this workaround is still needed; if not, remove the comment and use the proper aiohttp API.
- **Skills:** Python, aiohttp
- **Difficulty:** Easy

### 13. Investigate Multi-Machine Cache TODOs
- **Files:** `vj4/handler/domain.py` (line 138), `vj4/model/adaptor/contest.py` (line 745)
- **Description:** There are `TODO(twd2): This does not work on multi-machine environment.` comments regarding `functools.lru_cache()` on `datetime.datetime.utcnow()`. Investigate whether using a distributed cache or removing the cache is appropriate, or document the limitation.
- **Skills:** Python, caching
- **Difficulty:** Medium

### 14. Filter Username by Keywords
- **File:** `vj4/model/user.py` (line 25)
- **Description:** `# TODO(iceboy): Filter uname by keywords.` — Add a check during user registration to prevent usernames from matching reserved keywords (e.g., "admin", "system", "support").
- **Skills:** Python
- **Difficulty:** Easy

---

## How to Contribute

1. Pick an issue from the list above.
2. Open a **draft PR** early if you want feedback.
3. Follow the existing code style (2-space indentation, max 100 columns).
4. Run the test suite: `python -m unittest`.
5. Ensure frontend builds pass: `yarn build`.

If you have questions, feel free to ask in the issue or PR comments. Happy coding!
