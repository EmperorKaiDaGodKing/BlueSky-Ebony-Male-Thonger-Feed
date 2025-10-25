```markdown
# BlueSky — Ebony Male Thonger Feed

Purpose
- Centralized repo for feed configuration: tag lists, description & alt-text rules, sample post metadata, and a small validator.
- Goal: help curate an age‑restricted feed focused on consensual adult-oriented content about men's micro‑underwear, mature anime, programming, blogging, and Black creators, while muting politics, religion, and spam.

Safety & policy notes
- Do NOT store explicit media or private/personal data in this repo. Only include metadata (tags, descriptions, alt-text).
- This project is for filter templates and tooling only. Respect platform terms and local law.
- Filters assume 18+ content; implement age confirmation tokens (e.g., "18+") in posts.

Repo layout
- filters/
  - tags.json — whitelist & blacklist tags
  - description_regex.json — allow/block regex for descriptions
  - alttext_rules.json — required/blacklist rules for alt text
- examples/
  - sample_post_ok.json — non-explicit sample that should pass filters
  - sample_post_block.json — sample that should be blocked/demoted
- lists/
  - personal_lists.md — suggested personal list names and descriptions
- scripts/
  - validate.py — Python validator for sample metadata
- CONTRIBUTING.md — how to contribute safely
- LICENSE — MIT

How to use
1. Review and adapt the JSON rules in filters/ to match your client’s expected syntax and regex flavor.
2. Run the validator to confirm sample metadata passes/blocks as expected:
   - python3 scripts/validate.py
3. Import tag lists / filters into your BlueSky client where possible (client-dependent). If client doesn't accept imports, use lists as manual lookup and copy/paste.

Contributing
- Add new non-explicit sample posts to examples/ for testing.
- Submit improvements to regex patterns, tag lists, or test cases.
- Keep contributions non-explicit and privacy-safe.

Contact
- Repo owner: @drkskndudenthongs (use platform messaging; do not include explicit attachments here)
```