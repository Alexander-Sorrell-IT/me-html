# me.html — professional identity as a signed file

Built at the **Anything Applied Agentic Hackathon** (SF, Nov 7 2026).

Generate a key in your browser, sign your profile, hand someone a `.me.json`.
Two files merge offline: six gates decide whether the two people can agree at
all, a deterministic function proposes the terms, and both parties sign the
same digest. The result verifies with the network off. No account, no server,
no app — one HTML file, because the agreement is a pure function of the two
signed objects rather than a conversation between clients.

## Run it

Open `me.html` in a browser (works from `file://`, airplane mode on).
No build step, no dependencies, zero network calls (`grep -c 'fetch(' me.html` → 0).

## Test it

Open `test.html` — 26 assertions covering canon, sha256, ECDSA P-256, all six
merge gates and every rejection code, plus the agreement/ICS flow. All green.
Rebuild after editing the core: `python3 build_test.py`

## Files

- `me.html` — the app (build / merge / verify tabs), ~30 KB, single file
- `SPEC.md` — format spec `me/1` + `agreement/1`, threat model, what was cut
- `PITCH.md` — stage card: 20-second pitch, demo click order, judge Q&A
- `test.html` — offline test harness (26 assertions)
- `build_test.py` + `_tpl_*.html` — regenerates `test.html` from the shipped core
