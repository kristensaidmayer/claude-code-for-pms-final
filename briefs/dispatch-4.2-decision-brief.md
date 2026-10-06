# Rook Dispatch 4.2: decision brief

**Status:** proposed and not yet approved. The decision is Helen's, because
"Ping timeout tuning" is a committed Q3 item.
**Evidence:** rook-database pings, callouts and support tickets from
29 Jun to 6 Sep 2026 (44 days before the 12 Aug release, 26 after), the
`dispatch-routing` code, and the wiki. All figures are counts or groups,
with no individual responders identified.
**Limits:**
- The data ends on 6 Sep.
- There are only 16 responders, so the affected group is just four people.
- Routing settings change only with a release.

---

## 1. What the data shows

| Measure | Before 12 Aug | After 12 Aug |
|---|---|---|
| Pings taken | 76.6% | 64.0% |
| Pings turned down | 21.1% | 18.0% |
| **Pings missed** | **2.3%** | **18.0%** |
| Callouts needing 3+ pings | 1.4% | 5.9% |
| **Callouts nobody took** | **5.5%** | **11.1%** |
| Callouts per week | ~140 | ~120 |
| Seconds until a ping counts as missed | 91–93 | 61–63 |

- **There was no dip before the release.** The share of pings taken was flat
  at 75–78% for all six weeks before 12 Aug. The week of 3–9 Aug was the
  highest. Then it stepped down to 54% and climbed back to 73% by the week
  of 31 Aug.
- **Turned-down answers are quick.** Every one came within 40 seconds, both
  before and after the release.
- **Four responders lost most of their pings (66–75% fewer).**
  - Before the release they took about 75% of their pings and missed about 3%.
  - On 13–14 Aug their volume was still normal, but they missed 12 of 16
    pings. After that their pings fell to one or two a week, and they missed
    59% of those.
  - Callouts in their home areas used to go first to the local responder 80%
    of the time. After the release it was 17%.
- **The other 12 responders absorbed the work.** Most got 16–42% more pings.
  Their miss rate rose to about 14%.
- **Tickets:** 32 "quiet phone" tickets after the release, 22 of them about
  the four, and 0 before. 13 "gone before I could answer" tickets, all about
  the other 12. The 4 push or duplicate tickets were all before the release,
  and there were none after.
- **The tickets say phones ring.** Handlers wrote "buzzed, unlocked it,
  gone", and "first one in 5 (or 9) days and gone before she could answer".
- **Demand fell by about 15%,** evenly across areas.

## 2. What the data shows vs. what we're inferring

| The data shows | We're inferring |
|---|---|
| Misses jumped on 12 Aug and now happen at 60s. | That the 60s wait caused them. Both 4.2 changes shipped the same day. |
| Turned-down answers all come within 40s. | That about 15% of pings used to be taken at 60–90s. There are no answer times for takes. |
| The four missed many pings first, and their volume collapsed afterwards. | That the miss penalty sank them. We have no scores or ranked lists. |
| Unfilled callouts doubled. | That the proximity reweighting played only a small part. It's unmeasured, not ruled out. |
| Quiet-phone tickets match the responders who lost pings, and tickets say phones ring. | That push delivery is fine. There are no delivery receipts. |
| Acceptance improved through late August. | That the improvement is mostly an artifact, because the four are barely pinged now. |

**Most likely cause (about 75% confidence):** the 60s wait set it off, and
the existing miss penalty made it much worse.
- In the code, a miss costs the same as a decline
  ([offer.py:30](../00-rook/code/dispatch-routing/offer.py),
  [history.py:35](../00-rook/code/dispatch-routing/history.py)).
- Scores never ease back on their own. A 2019 TODO left that open.
- So responders who answer slowly sank and stayed down.

**How likely the other explanations are:**
- **Proximity reweighting as main cause:** low.
- **Seasonality:** low.
- **Demand:** a real but minor contributor.
- **Push delivery:** low, but not excluded.

**What this data can't settle:**
- How long takes actually take.
- Whether pushes are delivered.
- Scores and ranked lists.
- Proximity's separate effect.
- Data from earlier years.
- Why the four answer slowly.
- Why demand fell in release week.

## 3. The options

| Option | What it fixes | What it doesn't fix | Main risk | How reversible |
|---|---|---|---|---|
| **Full revert** | Extra misses, if the 60s wait is the cause. | The four responders' scores. A revert doesn't repair them. | Undoes the proximity change that responders asked for, with no evidence it did harm. | Possible each release, but it costs trust. |
| **Restore 90s only** | "Gone before I could answer" and new misses. | "Phone never goes off." The four are already buried. | Slower hand-offs. Does nothing if the 60s wait wasn't the cause. | Very, if a release can carry it. |
| **Change how misses count** | Sinking scores, now and in the future. | 60s misses and unfilled callouts. | Changes ranking for everyone. Needs design and a replay, so it won't be ready for the next release. | Technically yes, but the effects are hard to predict. |
| **Leave 4.2 in place and gather evidence** | Nothing. | Everything. | Unfilled callouts stay at double. The four sink further. The headline number misleads. | Waiting can stop any time, but the cost of each week can't be undone. |

## 4. Recommendation

**In the next release, restore the 90s wait and do a one-time repair of the
scores affected since 12 Aug. Keep the proximity weights. Design the change
to how misses count as a separate piece of work for a later release.**

**Why:**
- It targets the best-supported cause and keeps the part of 4.2 that people
  asked for and that shows no evidence of harm.
- **The score repair is essential.** Without it, we fix the "gone before"
  tickets but not "phone never goes off". The repair is a correction to the
  data, not a change in how ranking works.
- It's the smallest change that can be reversed, and each part can be undone
  separately. Shipping it apart from the miss-handling change means we can
  tell which one worked.

**What would change this before we ship:**
- **Data since 6 Sep shows the four already recovered:** ship only the 90s wait.
- **A release resets scores anyway:** the release itself does the repair.
- **Push logs show pings not delivered:** a delivery fix comes first.

## 5. Rollout and validation

**Step 0, this week:**
- **Ravi:** refresh the data through today, plus 2025 data if any exists.
- **Wen:**
  - Where do scores live in production, and does a release reset them?
  - Replay the post-4.2 callouts with scores restored.
  - Confirm the availability record Supply reads is unaffected.
- **Marcus:**
  - What's the earliest release slot, and is an out-of-cycle release possible?
  - Pull the push delivery logs.
  - Can the setting be changed for one area at a time?
- **Nadia:** tell the affected handlers we've found the likely cause. Make no
  date promises until the release slot is confirmed.

**Step 1:** ship the 90s wait and the score repair. Check daily for the first
week, then weekly. The baseline is 29 Jun to 11 Aug.

**Step 2:** design the change to how misses count (separate misses from
declines, let scores ease back, or both). Test it with Wen's replay. Write it
up as the routing doc Priya asked for.

**Success measures, by week 2 unless stated:**

| Measure | Before 4.2 | After 4.2 | Target |
|---|---|---|---|
| Pings missed | 2.3% | 18.0% | ≤ 4% |
| Callouts nobody took | 5.5% | 11.1% | ≤ 6.5% |
| The four responders' pings per week | ~12 | ~4 | ≥ 50% of baseline by week 2, ≥ 80% by week 4 |
| The four responders' take rate | ~75% | ~22% | ≥ 65% |
| Quiet-phone and gone-before tickets | ~0 a week | ~12 a week | ~1 a week by week 3 |
| Acceptance rate | 76.6% | 64.0% | ≥ 74%, read alongside the measures above |

**Guardrails:**
- **Median time from first ping to a take:** up by no more than 15 seconds.
- **Turned-down pings:** at or below 21%.
- **Pings to the other 12 responders:** not below their pre-4.2 level.
- **The availability record Supply reads:** unchanged.
- **Reporting:** stays at the level of counts and groups.

**What would make us reverse or widen the decision:**
- **Misses still above 8% after two weeks at 90s:** the wait wasn't the
  cause. Check push delivery, and consider reverting the weights.
- **Misses back to normal but the four still rarely pinged:** the repair
  failed, or proximity is involved. Consider reverting the weights.
- **Misses back to normal but unfilled callouts still high:** this is a
  coverage or demand problem, a separate investigation.
- **Wen's replay shows the new weights alone push the four down:** add a
  revert of the weights.
- **Median time-to-take worse by more than 30 seconds:** try a value between
  60 and 90 seconds, such as 75.

## 6. The 60-second version

> "Here's what the pings data says about 4.2. The drop isn't seasonal —
> acceptance was flat all summer and stepped down on 12 August. Turned-down
> pings didn't rise; *missed* pings went from 2% to 18%, all timing out at
> exactly 60 seconds. Four responders who almost never missed started
> missing on 13 and 14 August, and because a miss costs the same as a
> decline and scores never recover, they sank to the bottom — they're
> getting about a third of their old pings. That's the 'my phone never goes
> off' tickets. Meanwhile callouts nobody takes have doubled, to 11 percent.
> And the acceptance rate looks like it's recovering partly because those
> four barely get pinged.
>
> What we don't know yet: actual answer times, whether push is delivering,
> and the proximity weighting's separate effect.
>
> My proposal: in the next release, restore the 90-second wait and repair
> the affected scores, keep the proximity change, and design a proper fix
> for how misses count separately. Helen, it's a committed Q3 item, so I
> need your call. Wen, I need to know how scores are stored and a replay.
> Marcus, the earliest release slot and the push logs. Ravi, data through
> today. We'll judge it on missed pings under 4 percent and unfilled
> callouts back near 5 within two weeks."
