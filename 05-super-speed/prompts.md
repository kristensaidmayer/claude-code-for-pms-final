# 05 · Super Speed — prompts

**Context:** You joined Rook two weeks ago as PM on Dispatch.
Release 4.2 shipped on 12 August, just before you arrived, and
landed badly. You've spent three sessions finding out what went
wrong: the two piles of feedback that didn't agree, the numbers that
hid four people inside an average, and the code that settled it —
the shorter timeout is what did it.

At the end of the session, type wrap up, and Claude Code saves the
prompts you wrote yourself below — not the starter prompt — updates
CLAUDE.md, and saves your work to GitHub. By Module 6 this file is a
prompt library built from your own questions.

---

### 1.

tell me what we'd build with 3 builllet points

### 2.

update the brief and click through with everything we've learned and make assumptions for those we didnt

### 3.

this is adorable add some superhero kitties and puppies
also name one Vello on the cape

### 4.

make the cape teal

### 5.

remove the name vello

### 6.

make my prototype really good and functional

### 7.

dont show these sections only show what the app is supposed to look like:

### 8.

looks great! now give me a paragraph explanation of what i Did for my notes

### 9.

dumb it down

### 10.

and what does this solve for

### 11.

ok so combine what i solved for with a 3 sentence explanation of what thise does

### 12.

show me the prototype

### 13.

should mission impact. go at the bottom also should editor's note be a diffrent title

### 14.

yes more of a hero name and what is that section supposed to be for? actually demoing?

### 15.

ok now rewrite my notes explaining what problems i solved and what it does

### 16.

will this actually update their score so they dont stop getting calls

### 17.

should it update the score?

### 18.

ok give me my notes

### 19.

no just explain the app not the brief i have to present it to a coworker


---

## Questions Copilot asked in its reviews

Only the questions, in the words Copilot used. Each review is in the order it arrived.

### Review 1: the engineer's critique

- What exactly causes someone to become "Quiet" and exactly what clears it?
- Which score? The rebuilt home-area score?
- Compared to what baseline?
- Does the flag recalculate hourly, daily, or on every ping?
- What clears Quiet?
- Can someone oscillate in and out of Quiet every day?
- What actions are we actually changing in the routing workflow?
- When Kip sees Quiet, what operational action follows?
- What new workflow is created when Quiet appears, and which system owns it?
- Where does the responder-facing data come from and how trustworthy must it be?
- Are those values computed from ping logs in real time?
- What happens if a push receipt is missing (Marcus's open item)?
- What happens if Wen's replay disagrees with historical counts?
- Using Kip and Meteor Mite: what's still missing before this can actually be built?

### Review 2: "Questions I'd still ask before building"

- Why is "3 of the last 5 missed" the right threshold?
- Are we optimizing for catching every issue, or minimizing false alarms?
- What outcome are we actually trying to improve?
- What should Kip do when someone stays Quiet for 14+ days?
- What if the responder simply doesn't want work right now?
- Does Quiet mean "broken," "disengaged," or "temporarily unavailable"?
- Are we exposing enough information to responders?
- If Meteor Mite sees lots of missed pings, what action can they take besides sending a test ping?

### Review 3: "I'd push the brief a little harder"

- What happens if Quiet works perfectly?
- If the badge catches all four lockouts, what is Kip expected to do differently?
- If Quiet appears on Kip's card tomorrow, what specific action should we expect him to take within the next 24 hours?
- Why does Quiet need a responder-facing experience at all?
- Does the responder experience solve a problem responders reported, or is it primarily giving Kip a better way to investigate a Quiet alert?
- What outcome should the check-in replies change?
- Are the reply options purely informational for Kip, or do they trigger a different workflow, investigation path, or routing behavior?
- Are we solving lockouts or diagnosing causes?
- If the routing fix eliminates all four lockouts, would we still build Quiet and the responder tools?
- What makes an alert a false positive?
- Was Stormwrack actually a false positive, or did Quiet correctly identify a responder who briefly needed attention?
- Why didn't Nightwell flag?
- Nightwell was described as a real near-miss. What specifically distinguishes Nightwell from the four lockouts, and are we comfortable with a rule that misses that pattern?
- What is the "success" path for Meteor Mite?
- After Meteor Mite receives a Quiet check-in and confirms "I'm fine, keep pinging me," how do they know the system actually worked and they're no longer at risk of falling out of rotation?
- Is the goal to prevent responders from silently falling out of rotation, or to help us understand why they fell out of rotation after we've detected it?

### Review 4: "This is getting much stronger"

- Why is a responder required to take 4 of 5 pings to recover?
- Why is recovery harder than entering Quiet?
- What user behavior are we trying to encourage by requiring 4 of 5 taken instead of returning below the trigger threshold?
- Did we test alternative clear rules, or only trigger rules?
- Is "still quiet after 14 days" actually a product state or an organizational problem?
- What evidence do we have that another list after 14 days results in a different outcome than Kip's original outreach?
- If Nadia's team declined ownership tomorrow, would we still build the 14-day state?
- What happens if everyone starts using "I'm not available right now"?
- If responders discover they can suppress Quiet by marking themselves unavailable, what prevents availability data from becoming a proxy for "don't bother me" rather than actual availability?
- What is the cost of a missed Quiet episode?
- What happened operationally for the four lockouts that makes catching them worth two Stormwrack-style alerts every ten weeks?
- Is "phone not getting pings" the right diagnosis?
- What percentage of missed pings are believed to be delivery failures versus responder behavior versus routing issues?
- Are we measuring the right thing?
- If unanswered callouts fall but Quiet alerts increase, is that considered success or failure?
- Why is Quiet based on misses rather than lack of opportunities?
- Could a responder gradually receive fewer and fewer pings without ever triggering Quiet?
- What should Kip see after taking action?
- What feedback tells Kip the intervention worked?
- Should Quiet be responder-level or roster-level?
- If a deployment bug causes 30 responders to start missing pings simultaneously, is Quiet the right tool, or should the roster-level alarm fire first?
- If we could only ship one thing this quarter, would we choose the routing fix or Quiet?

### Review 5: "Have We Actually Solved the Problem?"

- If the routing fix works, what problem remains?
- Is the Quiet badge solving a separate visibility problem, or is it mainly insurance against future regressions?
- Would we still build Quiet if the lockouts had never happened?
- What evidence says handlers need a Quiet badge?
- Did handlers explicitly ask for earlier warning signs, or did they ask for help understanding what happened after a responder stopped receiving work?
- Who owns resolution once a responder replies?
- If someone says "my phone isn't getting pings," who is accountable for investigation and follow-up?
- What would make us revisit the 3-of-5 rule?
- Under what conditions would we switch to 3-of-7 to catch more near-misses like Nightwell?
- What would convince us the feature is no longer needed?
- If six months pass with no lockouts after the routing fix, do we keep Quiet, simplify it, or remove it?
- Are we primarily trying to prevent responders from silently falling out of rotation, or are we trying to understand why they fell out of rotation after we've detected it?

### Review 6: the pre-review questions

- What's the actual MVP?
- If we only have one sprint, what ships?
- Why isn't Quiet part of the MVP?
- What evidence supports Quiet?
- What's the biggest assumption?
- What would make you kill the feature?
- What did you intentionally not solve?
- How do you know you're not just overfitting to these four responders?
