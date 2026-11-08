# me/1 — a professional identity that is a file

**Thesis.** The unit of professional identity should be an object you hold, not an account you access.
One HTML document, one signed profile, no server, no feed, no chat, no search. Two of them meet, run a
pure function, and produce a co-signed agreement. The platform is the manual; delete it.

**Non-goals.** No accounts, no directory, no hosting, no messaging, no discovery service, no ranking.
If a feature needs a round trip, it is out of scope. The merge must work with the network off.

---

## 1. The profile file — `me/1`

A JSON document. Default filename `<handle>.me.json`. It is self-contained: everything needed to verify
it, and to merge it, travels inside it.

| field | type | meaning |
|---|---|---|
| `format` | `"me/1"` | version tag |
| `id` | string | `me:` + first 32 hex of `sha256(canon(public_key))` |
| `public_key` | JWK `{crv:"P-256",kty:"EC",x,y}` | verification key, embedded |
| `handle` | string | short name, used in terms text |
| `name`, `headline`, `building` | string | framing prose, unsigned meaning but signed integrity |
| `good_at`, `looking_for` | string[] | capability and ask |
| `claims` | `{id, text, evidence}[]` | assertions; `evidence` is `sha256:<64 hex>` |
| `availability` | string[] | ISO-8601 intervals `start/end` (UTC) |
| `policy` | object | see below |
| `issued_at`, `expires_at` | ISO-8601 | validity window |
| `signature` | base64url | ECDSA P-256 / SHA-256 over the canonical body |

`policy`:

| field | meaning |
|---|---|
| `kinds` | subset of `review`, `intro`, `pair`, `advice` — what merges you pre-authorise |
| `min_overlap_minutes` | shortest session you will accept |
| `max_per_day` | capacity; `0` closes the file to merges |
| `require_evidence` | every claim must carry a well-formed `sha256:` evidence field |

### Canonicalisation

`canon(v)`: objects serialised with keys sorted lexicographically, no whitespace, `undefined` dropped,
arrays in order, strings JSON-escaped. Signature is computed over `UTF-8(canon(body))` where
`body = profile` minus `signature`. This is what makes verification independent of formatting, key
order, and the JSON serialiser that wrote the file.

### Identity

The `id` is the key thumbprint, so an identity cannot be claimed twice without the private key, and a
renamed handle does not create a new identity. Losing the key loses the identity — that is the honest
cost of having no account recovery desk.

---

## 2. The agreement — `agreement/1`

```json
{
  "format": "agreement/1",
  "parties": [{"id": "me:…", "handle": "alex", "public_key": {…}}, {"id": "me:…", …}],
  "terms":  {"kind": "review", "minutes": 30, "text": "alex offers review to sam", "a": "me:…", "b": "me:…"},
  "slot":   {"start": "2026-11-09T18:00:00.000Z", "end": "2026-11-09T18:30:00.000Z"},
  "inputs": {"a": "sha256:…", "b": "sha256:…"},
  "issued_at": "2026-11-07T23:40:00.000Z",
  "digest": "sha256:…",
  "signatures": [{"id": "me:…", "sig": "base64url", "at": "2026-11-07T23:40:02.000Z"}]
}
```

- `digest = sha256(canon(agreement without digest and signatures))`
- each signature signs the **digest string bytes**, not the document, so signatures can be added in any
  order without invalidating earlier ones.
- `inputs.a` / `inputs.b` bind the agreement to the exact profile bodies that produced it. Change one
  claim in either file and the digests no longer line up.
- Validity = digest recomputes to the stored value **and** every party's signature verifies over it.
  One missing signature is `E_UNSIGNED`, not a partial agreement.

---

## 3. The merge — a pure function, so there is no protocol

The interesting constraint: two parties with no server, no session, no message exchange still produce
the *same* agreement. That only works if the merge is deterministic — a function of the two signed
inputs and nothing else. There are no negotiation messages, no nonces, no ordering. **The protocol is
the absence of a protocol.**

```
proposal(a, b) =
  kinds := [review, intro, pair, advice] ∩ a.policy.kinds ∩ b.policy.kinds   -- fixed order
  slot  := earliest interval in a.availability × b.availability
           with length ≥ max(a.min_overlap_minutes, b.min_overlap_minutes)
           (tie: earliest start, then longest)
  minutes := min(floor(slot.length / 15) * 15, 45)
  terms := {kind: kinds[0], minutes, text: `${a.handle} offers ${kind} to ${b.handle}`, a, b}
```

Both sides compute this independently and get byte-identical output; the digest is therefore the same
before either has spoken to the other.

### Gates

Evaluated in order; the first failure names the reason.

| # | gate | check | failure |
|---|---|---|---|
| 1 | `format` | both declare `me/1`, carry `id`, `handle`, `public_key` | `E_FORMAT` |
| 2 | `signature` | self-signature verifies against the embedded key | `E_SIG` |
| 3 | `fresh` | `issued_at ≤ now + 5min` and `expires_at ≥ now` | `E_EXPIRED` |
| 4 | `evidence` | claims carry well-formed `sha256:` where policy demands | `E_EVIDENCE` |
| 5 | `policy` | kind intersection non-empty, both capacities > 0 | `E_POLICY` |
| 6 | `overlap` | a shared window meets both minimums | `E_NO_OVERLAP` |
| 7 | `digest` (agreement) | recomputed digest equals stored | `E_DIGEST` |
| 8 | `signatures` (agreement) | each party signed the digest | `E_SIG` / `E_UNSIGNED` |

### States

```
IDLE ──load a,b──▶ PRESENTED ──format,sig,fresh,evidence,policy,overlap──▶ COMPATIBLE
                        │                                                     │
                        └───────────── any gate fails ──▶ REJECTED(code)       │
                                                                               ▼
                                                     PROPOSED ──sign a──▶ SIGNED_1
                                                         ▲                   │
                                                         └──sign b───────────┴──▶ CO_SIGNED
```

`CO_SIGNED` is the only state that yields a calendar hold. `REJECTED` is a first-class outcome and is
shown to the user with its code — a merge that silently degrades is worse than one that refuses.

### Idempotency

The agreement is a function of `(inputs.a, inputs.b, proposal)`. Re-running the same merge yields the
same `digest`, so duplicates collapse by digest and no server needs a dedupe table.

---

## 4. What the crypto proves, and what it does not

**Proves:** the holder of the private key authored this exact body (integrity, authorship), the two
profiles that produced this agreement were these exact bytes (binding), and both parties signed the
same terms (non-repudiation of the agreement).

**Does not prove:** that a claim is true. A `sha256:` evidence field shows a referenced artefact has
not changed; it says nothing about whether it supports the sentence above it. Self-signed claims are
claims. Third-party attestations (a signature over `sha256(canon(claim))` by a previous counterpart)
are the v2 answer and are not in this build.

**Storage caveat:** this build keeps exported private JWKs in `localStorage` so one browser can hold
both demo identities. That is demo-grade, not production-grade: no passphrase, no hardware key, no
isolation. Say so before a judge asks.

**Freshness:** `expires_at` bounds replay of an old file; re-issuing requires the key, so a "current"
file cannot be forged by editing dates.

---

## 5. Demo script (90 seconds, network off)

1. Airplane mode on, one laptop, both demo identities already in this browser's vault (two keys,
two files on the desktop — in the field that is two machines; say so once). Show `curl` failing if
anyone doubts it.
2. Load `alex.me.json` and `sam.me.json` — six gates turn green, the deterministic proposal appears.
3. Sign as alex, then co-sign as sam. `CO_SIGNED`. Download `.ics`, drag it into a calendar, the hold exists.
4. Tamper: edit one byte of sam's `handle` in a text editor, re-run. `E_SIG`. Nothing is created.

Beat 4 is the one judges remember: it proves the thing can say no.

---

## 6. Build state

Shipped in `me.html` (~1 file, no dependencies): identity generation, signing, export, merge with all
six gates, proposal, agreement, co-signing, offline verification, `.ics` export.

Cut for time: third-party attestations, revocation, multi-interval availability beyond one window,
two-device relay (the second signature needs the second key present), any directory at all.
