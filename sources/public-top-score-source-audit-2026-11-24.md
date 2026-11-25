# Public 0.24 source audit — 2026-11-24

## Result

No currently identified, licensed agent bundle is both hash-linked to a public 0.24 submission and decision-grade for another quota-limited comparison. The public leaderboard exposes team score and submission date, but no submission ID or archive hash; an author’s 0.24 report therefore does not by itself identify which bundle earned that row.

## Leaderboard evidence

The Kaggle CLI public leaderboard snapshot downloaded at 2026-11-24 17:05 UTC contains 6,638 rows. Seventeen teams tie at 0.24. The highest row is Yike Xu, submitted 2026-11-22; the second is MUHAMMED IDRIS BIN YACOOB (`muhammedidris28`), submitted 2026-11-07. The snapshot ZIP is archived under ignored `data/local/leaderboard-2026-11-24-1704utc/` with SHA-256 `FFA0B49FD4BE1249DCB673DF3E9C689825FD6B8AF7C65EDB5083773C1AF9B11B`. The official [leaderboard](https://www.kaggle.com/competitions/gemma-4-developer-agent/leaderboard) does not provide per-submission bundle hashes.

## Tie-break check

At 2026-11-24 20:00 UTC, `kaggle competitions team-submissions <team_id> --format json` returned Yike Xu's public-score entry (team `17019455`, submission `56897294`, `dateSubmitted=2026-10-07T02:06:25.257000`, score 0.24) and Idris's entry (team `16972967`, submission `57402375`, `dateSubmitted=2026-10-19T16:22:17.737000`, score 0.24). Kaggle's [rules, section 7(b)](https://www.kaggle.com/competitions/gemma-4-developer-agent/rules) say a tied winner is the submission entered first. Yike's score-bearing public submission predates Idris's, consistent with Yike appearing first among these tied rows. The snapshot's `LastSubmissionDate` values (November 22 for Yike and November 7 for Idris) differ from these score-bearing submission dates; I found no official definition for that field, so do not use it alone to infer tie priority. Kaggle's [CLI documentation](https://github.com/Kaggle/kaggle-cli/blob/main/skills/references/competitions.md#kaggle-competitions-team-submissions) documents `team-submissions` as the command to retrieve a team's public leaderboard submission. This resolves the apparent public-row ordering mismatch, but it does not establish private-leaderboard rank.

## Identifiable source bundles

- **Idris v24 — reproducible and Apache-2.0, but not an exact leaderboard artifact match.** The official leaderboard has `muhammedidris28` at 0.24. The author's [Gemma 4 agent runs dataset](https://www.kaggle.com/datasets/muhammedidris28/gemma4-agent-runs) declares Apache-2.0 and records `v24: [0.24]` in `leaderboard.json`; the author's [reproduction notebook](https://www.kaggle.com/code/arsen123/gemma-4-budget-fit-reproduction-notes) exposes the v24 ZIP. The downloaded archive hash is `474e9cdd5389c1501757e1f21d36fbaf661a1c991604b67e1ec0f08fe9ec7d51`, and its four runtime files match the dataset's v24 source byte-for-byte. However, neither the official leaderboard row nor the public source maps a Kaggle submission ID to that ZIP hash. Our paired 44-task local run resolved 19/44, one fewer than V5's 20/44; this is training-task evidence, not a leaderboard reproduction. Keep the already tested, licensed source, but do not add another v24 run to the first post-reset wave. See the broader [source audit](public-agent-source-audit-2026-11-20.md).
- **Hong Hanh v6 — not eligible for reuse from current evidence.** The [baseline notebook](https://www.kaggle.com/code/honghanhhh/gemma-4-baseline) and [exact-source audit notebook](https://www.kaggle.com/code/saudmasaud/gemma4-exact-hong-024-baseline) describe a reported 0.24 baseline, but no public record maps a specific competition submission to its extracted files. The archived notebook metadata and bundle declare no redistribution license. Independent same-byte reports show lower scores and a timeout, so the single 0.24 report is noisy. Do not redistribute or evaluate these files without established permission; the audit and historical hashes are documented in the [source audit](public-agent-source-audit-2026-11-20.md).
- **Pınar Aksoy / xpinara — no agent bundle.** The leaderboard row is at 0.24, but the linked [Collapsed Code Embeddings Reproduction](https://www.kaggle.com/code/xpinara/collapsed-code-embeddings-reproduction) is a CPU retrieval benchmark on public training tasks, not an agent ZIP or competition scoring run. It cannot be used as a submission candidate.

Kaggle CLI searches scoped to the other handles on the 0.24 rows did not surface a public agent bundle. This search is not proof that no source exists: the competition leaderboard itself lacks a bundle identifier, so any newly found candidate still needs a direct source, license, and score-to-archive link before it can be treated as an exact 0.24 reproduction.

## New 0.24 row — checked 2026-11-25 08:38 UTC

The 08:38:40 UTC public leaderboard snapshot has 18 teams at 0.24, up from 17 in the 2026-11-24 17:05 UTC snapshot. The new row is team `Ant` (`anthonytrevino`, team ID `17158342`), with a last submission date of 2026-11-23 and 11 submissions. Kaggle CLI searches for that user returned no public competition kernels, datasets, or models. No bundle or submission ID is linked to the score, so this row adds no reproducible candidate.

## Decision

Keep the reset-week order in [`milestone/PLAN.md`](../milestone/PLAN.md): run the one-task validation-contract probe, then the seeded V5/Patchsmith 53-task comparison and paired unseen holdout as quota allows. No newly audited 0.24 bundle changes that queue. The 0.24 reports are public-split evidence only; they do not establish the final private-leaderboard rank.
