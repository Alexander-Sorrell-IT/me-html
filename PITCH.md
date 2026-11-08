# me.html — stage card

## If you get 20 seconds

> "Your professional identity is a file you own, not a row in someone else's database. This is one
> HTML file: you generate a key, sign yourself, and get `alex.me.json`. Two of those files meet —
> six gates, a deterministic proposal, two signatures, one agreement. No account, no server, and it
> verifies with the network off. Watch it refuse."

## The sentence, one level deeper

The unit of professional identity should be an **object**, not an account. Everything else follows
from three prohibitions: no app to install, no account to create, no server to trust. If there is no
server, then agreement cannot be a protocol of messages — it has to be a pure function of two signed
files. That is why the merge state machine is the whole product, and why it can run on a plane.

## Why this is not the event's matchmaking feature

Mystery Match *suggests* people; it stops at "you two should meet." Consent is collected, then the
interesting object is missing: the thing after the introduction — a commitment with a kind, a time,
a duration, and two signatures that survive leaving the room. That object is what `me.html` makes,
and it makes it without a database to hold it.

It is also built for the case the room is actually about: an agent acting for a person. An agent can
carry a signed file and be refused. It cannot consent on your behalf, because it does not hold your
key. Consent stays with the human by construction, not by policy.

## Demo, click order (network off)

1. Airplane mode on. **Say the caveat once:** both keys live in this browser for the demo; in the
   field it is one key per machine.
2. Build tab: type `alex` → **fill example** → **generate key · sign · download**. Same for `sam`.
3. Merge tab: pick `alex.me.json` and `sam.me.json` → **run merge**. Six gates green,
   `COMPATIBLE 6/6`, proposal appears (kind, 30 minutes, earliest shared window).
4. **sign as alex** → pills show `alex signed / sam missing / OFFER`.
5. **co-sign as sam** → `CO-SIGNED`. Download the `.ics`, drop it in a calendar: the hold exists.
6. **The beat to end on:** open `sam.me.json` in a text editor, change one character of `handle`,
   re-run the merge. `REJECTED · E_SIG`. Nothing is created. A refusal is an outcome.

If asked to prove there is no backend: `grep -c 'fetch(' me.html` → 0.

## Against the five published criteria

| Criterion | The line |
|---|---|
| Working demo | It runs from `file://` with the network off, end to end, in under a minute. |
| Technical depth | Canonical JSON, ECDSA P-256 over the digest bytes so signatures append in any order, an 8-code gate ladder, and an agreement that is a pure function of two files. 26 assertions in `test.html` cover the crypto paths. |
| Originality | Not another agent that writes text. The claim is a format: identity as a signed object, agreement with no protocol because there is no server to talk to. |
| Usefulness | The same file works for two humans at a hackathon, a contractor and a client, or two agents that need a machine-checkable consent gate before they act. |
| Progress made today | Spec, app, verifier and test harness written today. `SPEC.md` is in the repo with the threat model and what was deliberately cut. |

## Questions you will get

**"Isn't this a business card?"** A card cannot say no, cannot expire, cannot bind two people to the
same bytes, and cannot be checked without a phone book. This is a card with a key and a state machine.

**"Where are the keys?"** In `localStorage`, unencrypted, so one browser can hold both demo
identities. Demo-grade: no passphrase, no hardware key. Production is one key per device behind the
OS keychain. Say it before a judge asks — it is in `SPEC.md` under storage caveat.

**"What stops someone lying about a claim?"** Nothing. Signatures prove authorship and binding, never
truth. The `sha256:` field only proves a referenced artifact has not changed. v2 is third-party
attestations: a signature over the claim from a previous counterpart, which is evidence a stranger
cannot manufacture alone.

**"Why not an app / QR code / wallet?"** Those are the easy versions. The prohibitions are the design
constraint that forced the interesting part — no server means agreement must be a pure function.

**"What if two files can't agree?"** Then there is no agreement, and the reason code says why:
`E_POLICY`, `E_NO_OVERLAP`, `E_EVIDENCE`, `E_EXPIRED`. Refusal with a reason is the feature, not the
error path.

**"Multi-party? Revocation?"** Cut. `expires_at` plus reissue covers staleness; revocation needs a
place to publish a list, which is a server, which is the thing this replaces.

**"What did you actually build today?"** Everything in the folder: spec, canonicalisation, signing,
merge, verifier, calendar export, and the harness. No framework, no dependency, no build step.

## What is cut, and why that is honest

Third-party attestations, revocation, multi-interval availability, two-device relay, any directory.
Each one needs either another key holder or a server. The first is v2; the second would undo the
premise.

## If you have to post a blurb

> **me.html** — professional identity as a signed file. Generate a key in your browser, sign your
> profile, and hand someone a `.me.json`. Two files merge offline: six gates decide whether the two
> people can agree at all, a deterministic function proposes the terms, and both parties sign the
> same digest. The result verifies with the network off. No account, no server, no app — one HTML
> file, 30 KB, because the agreement is a pure function of the two signed objects rather than a
> conversation between clients.
