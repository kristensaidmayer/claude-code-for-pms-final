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
