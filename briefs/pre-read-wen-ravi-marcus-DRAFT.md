# DRAFT, not sent: pre-read for Wen, Ravi and Marcus

Send as three short messages (or one thread). Each person gets only their own asks. Brief: `briefs/dispatch-quiet-responder-brief.md`.

## Context line for all three

I'm asking Helen to approve phase 1 of the quiet-responder work: 90s ping wait, a score rebuilt from the ping log (share of the last 30 home-area pings taken), and a roster alarm on the 7-day missed-ping rate. Her yes depends on three checks, and each of you holds one. A few days would be enough.

## Wen: replay and Supply check

1. Does Dispatch know each responder's home area (A1)? Is `_scores` in memory and reset on deploy (A2)?
2. Can you replay the rebuilt score (last 30 home-area pings, neutral 0.5 below 5 pings)? I expect the four at 0.67 to 0.80 (A3). Callouts 41006, 41017, 41039 and 41042 are the ones I most need.
3. Does the change leave everything the Responder Availability Record reads unchanged, so Supply's maintenance windows don't move (A18)?
4. Could the four be repaired before the release by a one-time rebuild from the ping log (A20)? Is that safe?
5. Why do chains never exceed 4 pings (A19)?
6. Travel minutes and location used for callouts 40981, 40983, 40987, 40990, 40992, 40998, 41006, 41023, 41043, 41050, 41054.

## Ravi: current data

1. Ping and callout data after 6 Sep. Are the four (Farlight, Meteor Mite, The Undertow, Vesper) still getting few pings? Has unanswered-callout rate moved from 11.2% (A7)?
2. Why did night callouts roughly halve after 4.2 (A19)?
3. Is unanswered callouts a fair stand-in for cost, or is there a real cost figure (A8)?
4. Would you add a weekly "pings down 50% against their own norm" line?

## Marcus: slot, push, response

1. Which release can the fix go in, and could a hotfix go sooner (A6)?
2. Can the push channel carry a non-ping message (A4), and can we get push receipts (A5)? Phase 2 and 3 only, no rush.
3. If the roster alarm fires, can your team look within one working day (A17)? Is 5% a sensible threshold?
4. What was the 60s ping wait in 4.2 meant to achieve (A16)? I'll ask Helen too.
5. Can you be the delivery owner on the brief?
