# Brief: keeping a responder in the rotation

Rook Dispatch · for Helen Achebe (Director of Product) · written 9 Oct 2026 · ping data through 6 Sep 2026

Click-through: `dispatch-quiet-responder-concept.html`. Where I did not know something, I made an assumption and listed it in the Assumptions table, with who confirms it and what changes if it is wrong.

## The problem, and who it is for

**Meteor Mite**, a responder, and **Kip**, the handler who looks after them and The Gale.

Meteor Mite is one of four responders who dropped out of the rotation after 4.2 (12 Aug).

- Pings went from about 11 a week to about 4. In the last 7 days of data they had one.
- Of the 14 pings since 12 Aug, 3 were taken, 3 turned down and 8 missed. The last five (20 Aug to 5 Sep) were four missed and one turned down.
- Routing priority counts a missed ping the same as a turned-down one, and the score never recovers unless the responder is pinged and takes. Nobody was demoted for old history. New misses, mostly on out-of-area pings, did it.
- Nothing told Meteor Mite why the phone went quiet. Kip said "Mite thinks Mite's been forgotten" and could only text back. Meteor Mite filed no ticket, so Nadia Hoffmann's queue never showed it. Kip's other responder, The Gale, went from about 13 to 19 pings a week, and nothing on his console explained the gap.
- The cost: callouts nobody took went from 5.1% to 11.2% (four weeks to 6 Sep), about 85% of the rise from misses.

Meteor Mite exists in our systems as capability tags, availability and ping history. Nothing here uses anything else about them.

## The goal, and what we build

**The goal is to stop responders silently falling out of the rotation.** Understanding why they did comes second and waits.

| Phase | What | Solves | Depends on |
|---|---|---|---|
| 1 | 90s ping wait, rebuilt score, and a roster-level alarm | The four lockouts, bad scoring, recovery after a restart | Wen Li's replay |
| 2 | Quiet badge and check-in on Kip's card | Nobody saw it for five weeks | Phase 1, Sofia Marino's card design |
| 3 | Responder screens: recent pings, test ping, "back in rotation" | Helping a responder understand why | Push receipts, and a responder interview round |

**What changes for Kip (phase 2).** Each coverage card says how busy the responder is against their usual week: "1 ping in 7 days, usually 11", with the last five outcomes. When 3 of the last 5 pings are missed, the card shows a Quiet badge and says so in plain words. Kip gets a "Send check-in" button, which is the text he sends today, logged. The Gale's card says it is busier than usual.

**What changes for Meteor Mite.**
- Phase 1: routing priority is rebuilt from their own history and the wait is 90 seconds again. That is what puts them back in the rotation.
- Phase 3: the app shows their recent pings, answers the check-in, offers a test ping, and tells them when they are back in rotation.

**What Kip does when Quiet appears.** He gets in touch with the responder within 24 hours (a text today). He does not file a ticket, review routing history or change routing. After 14 days still Quiet, the responder shows as a line in the weekly report to Helen, and Kip has a conversation about whether they want work.

## What it deliberately does not do

- **It does not revert 4.2.** Proximity stays weighted up. Responders who cover wide areas asked for it.
- **It does not let anyone change a rank by hand**, and no one sees the score or rank. Handlers and responders see counts and outcomes.
- **It does not make misses free.** That rewards never answering. A miss still counts, but only against home-area pings, and it can be recovered.
- **It does not add a separate out-of-area score yet.** That is the next release, after Wen's replay. Out-of-area pings did most of the early damage (visitors took 0 of 186 before 4.2).
- **It does not write to the Responder Availability Record.** Supply reads that for maintenance windows.
- **It does not start mutual aid or shared cover.** Both are on the Q4 exploration list.
- **It does not touch identity.** Everything comes from the ping log and capability tags (Security Policy 4.1).
- **It does not claim to know why a ping was missed.** Missed means no answer inside the wait.
- **It does not take on Kip's console asks** (dark mode, a different alert sound per responder). They are real and separate.

## How it works

### Routing (phase 1)

Only these change, and nothing else in routing:
1. Ping wait 60 to 90 seconds for everyone.
2. Score = share of the responder's last 30 **home-area** pings that were taken. A miss counts as not taken. Fewer than 5 home pings: use the neutral 0.5. The four land at 0.67 to 0.80 on the data we have.
3. The score is rebuilt from the ping log on every start, so it survives a deploy. Weights are unchanged.

**Roster alarm:** alert Marcus Oyelaran when the 7-day missed-ping rate is above 5%, or when 25% of the roster is Quiet at once. That would have fired on 12 Aug, 5 to 6 days before the weekly report or the support escalation. If a deploy makes 30 responders miss pings, this fires first and Quiet is the wrong tool.

### When a responder is Quiet (phase 2)

Computed from the ping log directly, not from routing priority. On the rebuilt score the four would not have flagged at all, and an alarm tied to the thing we are fixing would hide the next failure.

| Question | Answer |
|---|---|
| Raises when | 3 or more of the responder's last 5 pings are **missed**, any area, with at least 5 pings of history. |
| Baseline | Their own last 5 pings. Weekly ping volume shows on the card as context but is not a trigger: requiring a volume drop made it fire after the lockout. |
| Evaluated | Each time a ping resolves, plus a daily sweep. |
| Clears when | 4 or more of their last 5 pings are **taken**. Automatic. Kip cannot dismiss it. He can mark "checked in", which adds a note and does not clear it. |
| Can it flap? | No. Recovery is deliberately harder than entry. Four clear rules tested on the same log: fewer than 3 missed (mirror of the trigger) gave 9 episodes, up to 3 for one responder. 1 miss or fewer gave 7, up to 2. 3 takes of 5 gave 7, up to 2. **4 takes of 5 gave 6, none more than 1.** The cost is a slower clear: Stormwrack's badge stayed up 6 days against 2 under the mirror rule. |
| Stuck Quiet | A Quiet responder gets few pings, so may take weeks to clear. After 14 days they show as a line in the weekly report. Never cleared by time alone. |

**Why 3 of 5.** Same log, 16 responders, 29 Jun to 6 Sep, each rule with a matching clear rule. Lead time is days before the old score locked the responder out.

| Rule | Four caught (Farlight, Meteor Mite, Undertow, Vesper) | Episodes | Others flagged |
|---|---|---|---|
| 2 of last 5 | 4 of 4: 0, 5 to 6, 2, 8 | 24 | 11 of 12 others |
| **3 of last 5 (chosen)** | 4 of 4: 0, 5, 2, 3 | 6 | Stormwrack, The Gale |
| 3 of last 7 | 4 of 4: 0, 5, 2, 6 | 8 | Nightwell, Stormwrack, The Gale |
| 4 of last 7 | 4 of 4, two a day late | 4 | None |

2 of 5 is noise. 4 of 7 is late for the two fastest collapses. 3 of 7 is the closest rival: one more day on Vesper and it catches Nightwell, at the cost of two more alerts. If Helen would rather catch Nightwell-type dips, that is the swap.

**What counts as a bad alert.** A *self-cleared alert*: a badge that cleared within 7 days with no action from Kip. In the log that is Stormwrack (6 days) and The Gale (1 day). Stormwrack missed 3 in a row on 12 and 13 Aug, then took its next 3. The alert was right and the clear was slow. Target: no more than one a fortnight.

**Why Nightwell did not flag.** Its dip was mostly turn-downs with takes in between, and it kept being pinged and recovered. The four had misses in a row and then the pings stopped. The rule looks for responders who stop being offered work. A turn-down is a choice and we are not policing it.

**Can someone fade without Quiet?** In this log every responder whose weekly pings fell to half their own norm for a week or more was one of the four, and all four flagged. That is one 10-week window before the fix. Backstop: Ravi Menon adds a weekly "pings down 50% against their own norm" line.

### Check-in and replies (phase 2 for Kip, phase 3 for the responder)

The check-in is a push to the responder's app. It is not a ping: no callout, no ping wait, no score effect. It is logged, limited to one per responder per 24 hours, and creates no task. Kip's card then shows "check-in sent, no reply", then the reply, then the badge clearing.

| Reply | What Kip sees | Effect on routing |
|---|---|---|
| "My phone isn't getting pings" | The reply, and the test ping result. | None |
| "I'm not available right now" | "Replied: not available". | **None in this version.** Writing it to the Responder Availability Record needs Wen and the Supply team first. |
| "I'm fine, keep pinging me" | The reply. Quiet stays until the clear rule is met. | None |

No reply in 24 hours shows as "no reply yet". It is not treated as any of the three.

### Responder numbers and test ping (phase 3)

- **Source:** the same ping log routing reads, last 30 days. The app can never disagree with the score. The app never shows score or rank.
- **Words:** taken, turned down, missed, as in the Glossary. We cannot tell undelivered from missed without push receipts, so the app does not say the phone rang.
- **If Wen's replay disagrees with the log:** the log wins, and the responder screen does not launch until the two agree for all 16.
- **Test ping:** not a ping. No ping record, no score effect, 3 a day at most. It says "sent, delivery not confirmed" until push receipts exist, then "delivered".
- **How Meteor Mite knows it worked:** the badge clears after 4 takes in 5, and they see "Back in rotation".

## Assumptions

Things I did not learn from the data, code or interviews. Each is my working assumption so the brief can be built from. If one is wrong, the last column says what changes.

| # | Assumption | Confirms | If wrong |
|---|---|---|---|
| A1 | Dispatch knows each responder's home area (the responder record has an area field). | Wen Li | The score cannot be home-area only. Fall back to all pings with a lower miss penalty, and the fix is weaker. |
| A2 | The score is held in memory and reset by a deploy. | Wen Li | No effect on the design, since it is rebuilt from the log, but the replay baseline changes. |
| A3 | The 0.5 fallback below 5 home pings and the 30-ping window are right. | Wen Li | Re-run the replay with other values. |
| A4 | The push channel can carry a non-ping message (the check-in). | Marcus Oyelaran | Check-in becomes a note on Kip's card only, and Kip still texts. |
| A5 | Push receipts can be produced for the test ping. | Marcus Oyelaran | The test ping stays "sent, delivery not confirmed" and phase 3 loses most of its value. |
| A6 | The routing fix goes into the next available release on the monthly train, with the badge one release behind. | Marcus Oyelaran | If a hotfix is possible, phase 1 ships earlier. |
| A7 | The four are still locked out after 6 Sep. I have no data past that date. | Ravi Menon | If they recovered by themselves, the urgency changes, though the mechanism does not. |
| A8 | Unanswered callouts is a fair stand-in for cost. I have no revenue or response-time figure. | Ravi or Helen | Use the real cost to re-weigh the threshold. |
| A9 | Support (Nadia Hoffmann) can take "my phone isn't getting pings" cases, with Marcus's team on the push side. | Nadia Hoffmann | Drop the reply, or route it to Marcus's team directly. |
| A10 | Card placement: a badge on the card and a "Quiet: n" count at the top of the console. No chime. | Sofia Marino | Redesign, but nothing in the rule changes. |
| A11 | Handlers want the badge. No handler asked for it. | Sofia Marino, with Kip and one other handler | Cut phase 2 and keep the roster alarm. |
| A12 | Responders will accept seeing their own ping outcomes. No responder has been interviewed. | Sofia Marino, with 2 or 3 responders | Cut phase 3. |
| A13 | A handler can act on a Quiet responder within 24 hours. | Helen Achebe | Change the follow-up window. |
| A14 | A 25% Quiet share is a sensible alarm threshold (4 of 16 hit it at the peak). | Marcus Oyelaran | Re-set after two weeks of live data. |

## Acceptance criteria

*Routing*
1. Ping wait is 90 seconds for every responder.
2. After deploy each score equals taken divided by the last 30 home-area pings from the log, and is the same after a restart. In Wen's replay the four land between 0.67 and 0.80.
3. The roster alarm fires when the 7-day missed-ping rate is above 5%, or when 25% of the roster is Quiet.

*Quiet*
4. At least 5 pings with 3 of the last 5 missed: Quiet after the next ping resolves, and at the latest after the daily sweep. 2 of 5: not Quiet.
5. Quiet with 4 of the last 5 taken: cleared automatically. Nothing else clears it, including Kip.
6. Replaying the rule over 29 Jun to 6 Sep produces exactly six episodes: Farlight, Meteor Mite, The Undertow, Vesper, Stormwrack, The Gale. This is the regression test.
7. Routing priority for any responder is identical with Quiet on and off.
8. Quiet, the check-in and every reply write nothing to the Responder Availability Record.

*Check-in and test ping*
9. One click sends one push, logged with time and delivery state. No second check-in within 24 hours. It creates no ping and no score change.
10. Each of the three replies is logged and shown on Kip's card.
11. At most 3 test pings a day, none recorded in the ping log. "Delivered" appears only with a push receipt.

*Responder numbers*
12. For all 16 responders the counts in the app equal the ping-log counts for the same 30 days, difference zero. The app never shows score or rank.

*Success measure*
13. Callouts nobody took, 4-week rolling, at or below 6.5% (11.2% now). At week 2 half the window is still pre-fix, so also report the weeks since release alone. Locked-out responders 4 to 0. Missed-ping rate at or below 5%. Median time-to-accept up by no more than 15 seconds. Self-cleared Quiet alerts at most one a fortnight.

## Have we actually solved the problem?

**We believe we have solved** the lockout mechanism, the scoring issue, recovery after a restart, early detection of the one pattern we have seen (misses in a row, then pings stop), and a handler-visible signal if it returns.

**We have not proven**
- That responders want the responder-facing screens. No responder has been interviewed.
- That check-in replies improve any outcome.
- That delivery failures are a meaningful cause of missed pings. The evidence leans the other way: misses spiked 13 to 14 Aug before volume collapsed, and only 2 of the 4 quiet-phone tickets were collapsed responders.
- That a handler's outreach changes a responder's behaviour. Kip texting Meteor Mite is the only example, and it did not help.
- That Quiet catches a future failure mode and not just the four we know.

| Question | Answer |
|---|---|
| If the routing fix works, what is left? | Mostly insurance. The badge answers "can anyone see a responder drifting?", but the only drift in this data was the four. It is the first thing to cut if capacity is short. |
| Would we build Quiet if the lockouts had never happened? | Not as a priority. It follows the routing fix. |
| Did handlers ask for it? | No. Kip wanted the gap between his two cards to stop looking like a coincidence, Aunt Dot wanted to be told when a ping arrives, and Ambrose wanted live callouts harder to miss. The badge is inferred (A11). |
| What would make us switch from 3 of 5? | More than one self-cleared alert a fortnight after two weeks on the 90s wait: move towards 4 of 7. If Helen would rather catch dips like Nightwell's: 3 of 7. Review at two weeks and again after one full release. |
| What would make us remove it? | A full release cycle with no true alert (none that Kip acted on or that preceded a lockout): simplify to the roster alarm and the weekly report line. |

## Open items by owner

| Who | What |
|---|---|
| Wen Li | A1 to A3. Replay of callouts 41006, 41017, 41039, 41042. Travel minutes and the location used for callouts 40981, 40983, 40987, 40990, 40992, 40998, 41006, 41023, 41043, 41050, 41054. Why chains never exceed 4 pings. Whether "not available" can write to the Responder Availability Record without moving Supply's maintenance windows. |
| Marcus Oyelaran | A4 to A6, A14. Push receipts. A release slot. |
| Ravi Menon | A7, A8. Data after 6 Sep. Why night callouts roughly halved after 4.2. Weekly "pings down 50%" line. |
| Sofia Marino | A10 to A12. Card placement, responder screens, what triggers the console chime, a check with handlers and two or three responders. |
| Nadia Hoffmann | A9. The 45 unanswered routing tickets since 12 Aug, including #3043 from Mr. Ambrose (13 Aug). |

## Decisions for Helen

1. **The goal.** Prevent responders silently falling out of rotation first, with the responder screens held back. Agree?
2. **The action.** If Quiet appears on Kip's card tomorrow, is "get in touch within 24 hours" what we expect from him (A13)?
3. **Sequencing.** Does the 90s wait plus the score rebuild go out alongside the handler badge, or ahead of it? I recommend ahead, with the roster alarm.
4. **The threshold.** 3 of 5, or 3 of 7 if you want to catch dips like Nightwell's?
5. **Responders seeing their own ping outcomes.** Comfortable with that, once we get to phase 3?
