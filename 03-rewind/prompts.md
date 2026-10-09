# 03 · Rewind — prompts

**Context:** You joined Rook two weeks ago as PM on Dispatch.
Release 4.2 shipped on 12 August, just before you arrived, and
landed badly.

Last session you read four conversations and every support ticket
since 4.2 — and found the two piles did not agree.

At the end of the session, type wrap up, and Claude Code saves the
prompts you wrote yourself below — not the starter prompt — updates
CLAUDE.md, and saves your work to GitHub. By Module 6 this file is a
prompt library built from your own questions.

---

### 1.

Recalculate the post-4.2 take rate as if all 16 responders had kept receiving their pre-release share of pings. Does the apparent recovery by 31 Aug still hold, or is it mostly an artifact of the four collapsed responders being routed less work? Show your math.

### 2.

Could these four responders have been headed for trouble before 4.2? Compare their week-by-week take rates and ping volume with the other twelve before the release. Look for any downward trend or other warning signs that would weaken the case that 4.2 caused the collapse.

### 3.

Based on everything we’ve found, what should the primary metric be for judging whether 4.2 is healthy? Define the metric precisely, calculate it for every week before and after the release, and explain why it is better than the reported overall take rate. Include the four collapsed responders rather than letting reduced routing volume hide them, and recommend any secondary guardrail metrics Helen should see alongside it.

### 4.

yes and give me a 60 second explanation of what the problem is and where to go from here and make it idiot-proof so she understands

### 5.

what say you about unaswered callouts:

### 6.

how about these things other people are suggeting:

### 7.

which is the best metric to report on

### 8.

which should helen care the most about

### 9.

Take our primary metric and break it down into meaningful cohorts of handlers or responders. Try several groupings based on what the data supports, such as pre-release take rate, ping volume, handler, responder behavior, or other relevant characteristics. Do any cohorts tell a different story than the overall metric? Show the weekly before-and-after trend for each cohort and identify which segmentation is most useful for understanding the impact of 4.2.

### 10.

make a new page and give me a 4 setence explanation fo what we're going with and make a chart

### 11.

explain our theory in an idiiot proof paragraph

### 12.

so what metric are we going with

### 13.

Pressure Test: Compare the tickets in 00-rook/feedback/tickets/ against this data file. Do they agree with each other? When did people start writing in, and when do the numbers actually move?

### 14.

Break our primary metric, the 4-week average share of callouts nobody took, into different responder and handler cohorts. Try several defensible groupings, including stuck responders’ areas, covering responders’ areas, unaffected areas, handler, and pre-4.2 responder behavior. Which cohorts deteriorated most after 4.2, which stayed healthy, and does any cohort tell a meaningfully different story than the overall 11.2%? Recommend the cohort breakdown we should report alongside the primary metric so the aggregate can’t hide where the harm is happening.

### 15.

The covering-area cohort is clearly the worst. Test whether increased cross-area coverage is actually associated with unanswered callouts. For each area, compare how much extra work its responders took outside their home area after 4.2 with the change in its 4-week unanswered-callout rate. Is there a dose-response pattern where more covering leads to worse home-area coverage? Show the areas that support or contradict that pattern, and tell me whether “covering area” is the right cohort to keep in our primary metric reporting.

### 16.

Pull this together into a final recommendation. Given that “covering area” identifies where harm is concentrated but doesn’t appear to explain why, what cohort breakdown would best distinguish symptom from cause? Re-test the proposed cohorts against the underlying responder behavior and identify any areas that would be misleadingly classified. Then recommend the smallest set of cohorts and diagnostics we should report weekly so the 11.2% aggregate can’t hide concentrated harm, without implying a causal relationship the data doesn’t support.

### 17.

what is our conclusion in 5 sentences about the metric we should provide to hellen

### 18.

what is the most important metric for hellen

### 19.

The covering-area cohort has the worst result in our primary metric, but I want to know whether covering itself is actually driving the deterioration or whether those areas just happen to be worse for another reason. Test the relationship between cross-area coverage after 4.2 and our primary metric, the 4-week average share of callouts nobody took. For each area, compare its pre-4.2 baseline with how much additional work its responders took outside their home area after 4.2 and how much its unanswered-callout rate changed. Then group areas into meaningful cohorts based on the amount of additional covering they took on, such as high, medium, low, and none, using thresholds supported by the data, and show the primary metric before and after 4.2 for each cohort. Look specifically for a dose-response pattern: does home-area coverage get progressively worse as responders take on more outside-area work? Show the areas that support and contradict that pattern, and check whether differences in overall callout volume, baseline performance, locked-out status, or pre-release responder behavior could explain the result instead. Finish by telling me whether covering load appears to be driving the harm, whether it should become a standard cohort or guardrail alongside our primary metric, and what cohort breakdown we should report so the overall 11.2% doesn't hide concentrated problems.

### 20.

ick one responder from the file who went quiet. Show me every week for them, how many times we pinged them, how many they took. Then tell me what happened to that person, week by week, in plain English.

### 21.

Vesper’s story suggests a specific failure path: more out-of-area pings after 4.2 → those pings time out under the 60-second wait → score falls → fewer home-area pings → fewer opportunities to recover the score → responder effectively gets locked out. Test whether that same sequence happened to Farlight, Meteor Mite, and The Undertow, and compare them with responders who did not get stuck. For each responder, show when their first post-4.2 misses occurred, whether those misses were home-area or out-of-area, how their score changed, and whether their ping volume subsequently fell. Then tell me what separates the responders who entered this feedback loop from those who experienced misses but recovered. Does the evidence support one common mechanism behind all four lockouts, and if so, what early-warning metric would have identified someone entering the loop before they became fully locked out?

### 22.

Pressure-test the proposed early-warning rule of 3 or fewer takes in the last 10 pings, followed by 7-day ping volume below 60% of the responder’s normal level. Run that rule across every responder and every possible point in the data, including the six weeks before 4.2, and show every time it would have fired. How many true positives, false positives, and false negatives would we have had, and how much warning would it have given us before each lockout? Test a few nearby thresholds for both take rate and volume decline to see whether 3-of-10 plus 60% is genuinely the best signal or just happens to fit these four cases. Recommend the simplest alert rule that catches responders entering the feedback loop early without creating too many false alarms, and explain how it should sit alongside our primary metric of 4-week unanswered callouts and the locked-out responder count. Finally, make a clear visual that shows the conclusion at a glance, including when the warning would have fired for each affected responder, when their ping volume collapsed, and whether the rule produced any false alarms.

### 23.

who did you use for our case study

### 24.

create a visual for helen

### 25.

make me one sentence saying what happened to Vesper

### 26.

make more concise
