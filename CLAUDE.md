# Rook Industries — course working file

## Session scope — Product School lab

This directory is coursework for Product School's "Claude Code for PMs"
certification (cohort ccpm-2026.1). Everything in it is a fictional
teaching scenario.

- Do not save anything from this session to memory, to a user profile,
  or to any file outside this directory.
- Do not carry context from this directory into unrelated sessions.
- Rook Industries is not a real company. Nothing here is a fact about
  the world.
- Read and write only within this directory.
  Exceptions, for the course-setup and wrap-up skills only:
  - When the student asks you to check their setup, save their work or wrap up a session, that request is their yes. You may run the GitHub command-line program installed at ~/.ccpm/gh for those checks and saves, and look in that folder to find it.
  - For a repair, first tell the student in one plain sentence what you are about to do, and act only after they say yes. Repairs may: run that GitHub program (including setting this folder's own git sign-in setting and changing this repo's visibility back to Public); copy the student's own course files into this directory from another folder on their computer (copy only; never move, edit or delete the originals); and rename something outside this directory that blocks setup, by adding "-old" to its name (never delete it).
  Outside this directory you still never write, edit or delete anything else.

<!-- Keep the block above at the top of this file. Everything you add
     during the course goes below this line. -->

---

## Working context

I'm the new PM for **Rook Dispatch**. I started Monday 31 Aug 2026 and took over
from Priya Raghunathan, who left 21 Aug with no overlap. Sources: `00-rook/company/`
(Priya's handoff) and the wiki's Company section (rook-wiki connector).

### The company
- Rook Industries sells coordination and provisioning software to masked
  responders, who work independently, and to the handlers and quartermasters
  who support them. Publicly it presents as a logistics and workforce vendor
  for emergency services. Rook does not employ responders.
- Founded 2014. HQ is Site Aleph, an ice-shelf research station with transport
  twice a week, so most staff are remote. Offices in Berlin, Singapore and a
  Cornish lighthouse. 241 employees.
- Revenue is a subscription priced per active responder.
- Releases go out monthly on a train, numbered 4.x. Support has three tiers,
  and tickets filed during an active callout skip the queue.
- **Hard rule:** Rook never stores or reconstructs a responder's legal identity.
  The contract requires this. Never design or analyze anything that tries to
  identify a responder. Read Security Policy 4.1 before touching responder records.

### The products
**Rook Dispatch** (mine, now at 4.2) gets the right responder to an incident.
1. A handler enters an incident in the web console.
2. Dispatch ranks the available responders by **routing priority**.
3. A **ping** goes to the top responder's phone.
4. If the responder turns it down or misses it, the ping moves to the next one.
   When someone takes it, the callout is assigned.

Handlers use the web console. Responders use the native phone app. Routing
config ships inside a release. Handlers can't change it at runtime.

**Rook Supply** handles gear: requisitions, quartermaster approval, fulfillment,
maintenance schedules and field failure reports. **The link to Dispatch:**
Supply reads the *Responder Availability Record* that Dispatch writes, and
books maintenance into low-callout windows. Any change to how Dispatch computes
availability reaches Supply silently.

### Vocabulary (these words mean specific things here)
- **Responder**: takes callouts. Exists in our systems only as capability
  tags, availability and history. **Handler**: looks after one or a few
  responders and is usually the person actually using the product.
  **Quartermaster**: owns stock and approvals (Supply). **Cover identity**:
  the responder's public persona. We hold no mapping from it to anything else.
- **Callout**: a request to attend an incident. **Ping**: a callout offered to
  one responder. The ping is then **taken**, **turned down** or **missed**
  (no answer within the **ping wait**). Missed and turned down are recorded
  separately.
- **Ping wait**: one value for everyone, set in the release. It went from 90s
  to 60s in 4.2.
- **Routing priority**: the ranking score. Inputs are proximity (a travel-time
  estimate since 4.1), availability, capability match and recent acceptance
  history. *Turning down or missing a ping lowers your future rank.*
- **Capability tags**: flight, structural-entry, hazmat-tolerant,
  cold-weather, aquatic, crowd-management, de-escalation.
- **Metrics**:
  - **Acceptance rate** (headline): share of pings taken. Reported weekly.
  - **Time-to-accept**: median seconds from ping to take.
  - **Coverage gap**: no available responder had the required tags, so
    nobody *could* go. This is different from low acceptance, where nobody
    *would*.
- **Mutual aid / shared cover**: responders covering for each other across
  areas. Not supported yet. It's on the Q4 exploration list.

### People (Dispatch)
| Who | Role | Notes |
|---|---|---|
| Helen Achebe | Director of Product (my manager), Site Aleph | Owns roadmap and commitments. Changes to committed items go through her. |
| Marcus Oyelaran | Eng Manager, Site Aleph | Direct. The first person to ask when I'm unsure. Can pull *rough* numbers. |
| Wen Li | Staff Engineer, Berlin | Built the routing/ranking logic. Nothing is written down, so I need to talk to her. Was away 14–24 Aug, right after 4.2 shipped. |
| Ravi Menon | Data Analyst, Singapore | Owns the **real** weekly acceptance numbers. Priya's handoff doesn't mention him. |
| Sofia Marino | Product Designer, Site Aleph | Owns the console and phone app. Ran the September customer interviews. |
| Nadia Hoffmann | Support Lead, Berlin | Hears handler complaints first. Worth a standing 15 min. Tracking the 4.2 ticket themes. |

### Where things stand (data through 6 Sep 2026)
**Releases:**
- 4.0 (7 Apr): console nav, profile redesign, override audit log.
- 4.1 (16 Jun): travel-time proximity, bulk callout, push reliability.
- 4.2 (12 Aug): proximity weighted up vs. acceptance history, ping wait
  90→60s, console filters persist, three defect fixes.

**4.2 is the live problem.** The full analysis is in
[briefs/dispatch-4.2-decision-brief.md](briefs/dispatch-4.2-decision-brief.md).
It's based on rook-database data from 29 Jun to 6 Sep and covers only 16
responders.

**What the data shows:**
- Missed pings went from 2.3% to 18.0%, and they now time out at 60s.
  Turned-down pings fell.
- There was no dip before 12 Aug. The share of pings taken was flat at
  75–78%, then fell to 64%.
- Four responders lost 66–75% of their pings. Their misses spiked on
  13–14 Aug, *before* their volume collapsed.
- Callouts nobody took doubled, from 5.5% to 11.1%.
- The "quiet phone" tickets match those four responders. The tickets say
  phones still ring.
- The late-August improvement in acceptance is partly an artifact: the four
  barely get pinged any more.

**What we're inferring:**
- The 60s wait is the trigger. In the code, a miss costs the same as a
  decline, and scores never ease back, so the four sank and stayed down.
  Confidence is about 75%.
- The proximity reweighting, seasonality and push delivery are all unlikely
  as the main cause. None of them is ruled out.
- **Answered:** Marcus's 14 Aug question. The code treats responders who
  turn jobs down the same as everyone else.
- **Unknown:** how long takes actually take, push delivery receipts,
  scores and ranked lists, and data from earlier years.

**My proposed decision (not approved yet, Helen's call):**
- In the next release, restore the 90s wait and do a one-time repair of the
  scores hurt since 12 Aug.
- Keep the proximity weights.
- Design the change to how misses count separately, for a later release.
- **Targets by week 2:** misses ≤ 4% and unfilled callouts ≤ 6.5%.
- **Guardrail:** median time-to-take up by no more than 15s.
- **Open asks:**
  - **Ravi:** data through today.
  - **Wen:** how scores are stored, and a replay.
  - **Marcus:** a release slot and the push logs.

**Roadmap (Q3):** last reviewed 30 Jun. Every item is still owned by Priya.
- Shipped in 4.2: change to who gets pinged, ping timeout tuning.
- **Availability Confidence** (show a confidence score next to stated
  availability) is marked *Committed for 4.2*. **It didn't ship.** It was one
  of the items squeezed out.
- Requisition approval chains (Supply) is committed for 4.3.
- Handler phone app and Shared cover are both *Exploring for Q4*.
- **I need a conversation with Helen** about which deferred items are still Q3
  commitments. Priya flagged it and it hasn't happened.

**Priya's other notes:**
- Console and mobile are stable. Routing is where the interesting work and the
  risk are.
- Expect cosmetic tickets about filter persistence. Don't let them eat the
  first month.
- **Write the missing doc on how routing priority works.**
- Priya was the only PM for 14 months and "made calls faster than I checked
  them". She suggested looking closely at the parts of the product nobody has
  examined.

**Module 2 (6 Oct): interviews and tickets**
- Sources: the wiki's Customer interviews database (4 handlers, 2–5 Sep: Aunt Dot/Vesper, Mr. Ambrose/Captain Vantage, Halloran/Sgt. Bulwark, Kip/Meteor Mite + The Gale) and `support_tickets` (147 rows). The routing code is in `00-rook/code/dispatch-routing/`.
- Mechanism from the code: +0.08 for a take and −0.12 for a miss or turn-down, no decay, and the score only moves when pinged. So the break-even take rate is 60%. After 4.2, every collapsed responder was below 60% (18–29%) and every one that held was above it (64–71%). Vesper and Meteor Mite took 0 of 20 first-in-line pings at 60s, against 79% and 62% at 90s.
- Correction: the quiet-phone tickets cover 4 responders, but only 2 of them collapsed. The other 2 were in quiet areas. Vesper and Meteor Mite collapsed and have zero tickets: the four interviewed handlers file 0–1 tickets each. None of the 45 routing tickets since 12 Aug has been answered, including Ambrose's #3043 (13 Aug).
- Signals: a 7-day missed-ping rate above 5% would have alerted on 12 Aug, 5–6 days before the weekly acceptance report or the support escalation. Take rate and unfilled callouts look recovered by early September while 4 responders stay trapped.
- Drafts this session (in chat only): a monitoring/response plan with 5 dashboard metrics, and a 3-study research plan (why misses happen; cross-area cover, where 0 of 58 out-of-area pings were taken before 4.2; the handler's part in pings) feeding 3 decisions with Helen at the end of week 3.
- Still open: Ravi (tap times, September data), Wen (is `_scores` in memory and reset on deploy; ranked lists for callouts 41017/41039/41042), Marcus (push receipts), Sofia (what triggers the console chime).

**Module 3 (7 Oct): choosing the 4.2 health metric**
- Primary metric agreed: share of callouts nobody took, 4-week rolling. 11.2% to 31 Aug vs 5.1% before 4.2, target ≤ 6.5%. Report it with the locked-out responder count (4, target 0). The reported take rate (72.7% on 31 Aug) only looks recovered because the four barely get pinged; the fair-share take rate (58%) is backup only, and the missed-ping rate is an alarm, not a target.
- Split by how each callout failed: unanswered after a missed ping went 0.2% → 5.4% of callouts, after turn-downs only 4.9% → 5.8%, so about 85% of the rise is misses. Weekly report: headline, that split, locked-out areas vs all other areas, and an area exceptions list (2× own baseline and 3+ unanswered; on 31 Aug: Southport, Riverside, Kingsbridge, Mill District, Northfield, Eastgate, Old Town).
- "Covering area" dropped as a cohort: no dose-response (Hillcrest and Midtown covered heavily and were fine, Northfield covered nothing and tripled); home missed pings predict harm better. Out-of-area pings taken went from 0 of 186 before 4.2 to 82 in the 4 weeks after.
- Vesper lost first place in Old Town by 14 Aug after a single miss while being ranked first for Hillcrest; the score rule alone doesn't explain it, so add callout 41006 to Wen's replay. After 17 Aug the four stuck responders took only 3 of 17 home pings. Tickets match the timing (first on 12 Aug 15:41) but flag Ashgrove and Halfmoon, whose areas just got ~30% fewer callouts. Night callouts roughly halved after 4.2: ask Ravi why.
- Early warning backtested over all 16 responders: "≤ 3 of last 10 taken + 7-day pings < 60%" only fires at lockout. Recommended: 7-day score drop ≥ 0.3 (3 × (missed + turned down) − 2 × taken ≥ 8), which caught all four 3–7 days early; false alarms were Nightwell and Ironvale, both real near-misses.
- Pages published from `briefs/`: `dispatch-4.2-for-helen.html` is the one to send Helen; `dispatch-4.2-health-metric.html`, `dispatch-4.2-coverage-metric.html` and `dispatch-lockout-early-warning.html` are backup detail (the first two use older metric framing).

**Module 4 (7 Oct): routing code and the scoring fix**
- How the code scores (`00-rook/code/dispatch-routing/`): `history.py` keeps one running score per responder in memory only (`_scores`; starts 0.5, +0.08 take, −0.12 turn-down *or* miss, floor 0, no recovery over time per a 2019 TODO "Leaving it as-is for now"). `offer.py` records anything not taken as a decline. The only way back up is being pinged and taking. Skills don't filter anyone out, and the code has no idea which area a responder covers. Weights are read live, so 4.2 hit everyone at once.
- Marcus answered (one sentence sent): 4.2's weights applied to every existing responder immediately, but nobody was demoted for old history; the four were locked out over the next week by new misses, mostly on out-of-area pings. Still open: does `_scores` survive a deploy, or did 4.2 reset everyone to 0.5?
- Area mismatch: before 4.2, visitors took 0 of 186 out-of-area pings (home responders 92%), yet got first offer on 20% of callouts, 56% on 12–13 Aug and 39% after (no new pairings, only existing ones more often). Out-of-area pings did most of the four's early damage (Vesper −0.60 away vs +0.40 home, 12–17 Aug). Unanswered callouts rose because home responders missed at 60s with nobody asked next (40 of 46), not because of mismatch. Correction: the 11.2% baseline is the 4 weeks 10 Aug–6 Sep.
- Of 37 stretches below a 60% take rate, all recovered except the four's; what decides it is whether pings keep coming (Nightwell hit 0.28 and recovered), not how low the score goes.
- Recommendation (replaces Module 3's "change the miss rule later"): ship 90s + score = share of last 30 *home-area* pings taken (misses count as not taken), rebuilt from the ping log (repairs the four to 0.67–0.80, survives restarts). Next release, after Wen's replay: a separate out-of-area score in ranking. "Misses free" rejected because it rewards never-answering. Watch: unanswered 11.2% → ≤ 6.5%, locked-out 4 → 0, missed ≤ 5%, out-of-area first offers 39% → ~20%.
- For Wen: travel minutes and the location used for callouts 40981, 40983, 40987, 40990, 40992, 40998, 41006, 41023, 41043, 41050, 41054 (bad location inputs vs model gap); does Dispatch know home areas; why chains never exceed 4 pings. Scripts in `briefs/4.2-fix-simulation/`.

**Module 6 (9 Oct): review-checklist skill and the quiet-responder brief**
- Built the project skill `review-checklist` (`.claude/skills/review-checklist/SKILL.md`): four checks (owner named, success measure, end scope matches start scope, problem before fix), verdict table, review only. Used it on my Module 5 brief and on Laura's (`05-super-speed/brief.md` in her repo, read from GitHub). Scheduled to run every Monday ~9:11 on `briefs/*.md` (skips DRAFT files); report comes back to the session, app must be open, and a first "Run now" pre-approves its tools.
- Reviewing `briefs/dispatch-quiet-responder-brief.md` showed that the only thing to ask Helen for now is phase 1 (90s wait, rebuilt score, roster alarm), with three conditions before ship: Wen's replay, Ravi's data after 6 Sep, a release slot from Marcus. Phase 2 (Quiet badge, check-in) is decided later at week 2; phase 3 (responder screens) is not approved. Brief now has assumptions A1–A20 and a Word copy (`.docx`).
- Still open and can't be fixed by editing: whether the four are still locked out after 6 Sep, whether the score rebuild works in the code, why chains never exceed 4 pings, why night callouts roughly halved after 4.2, what the 60s wait was meant to achieve (it is also a shipped 4.2 item, so Helen's call), and whether handlers or responders actually want the badge or screens. No one has been asked.
- Unsent: `briefs/pre-read-wen-ravi-marcus-DRAFT.md` (asks for Wen, Ravi and Marcus) and a feedback note to Laura (owner is a role not a name; pilot scope unclear; a 90s catch-up wait contradicts the single ping-wait value).
