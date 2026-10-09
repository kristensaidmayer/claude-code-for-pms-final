# 04 · X-Ray Vision — prompts

**Context:** You joined Rook two weeks ago as PM on Dispatch.
Release 4.2 shipped on 12 August, just before you arrived, and
landed badly. Last session the numbers showed you what happened: a
ping used to wait ninety seconds and now it waits sixty, people
missed pings they used to catch, and missing one counts the same as
turning one down — so four responders stopped hearing from us
altogether.

At the end of the session, type wrap up, and Claude Code saves the
prompts you wrote yourself below — not the starter prompt — updates
CLAUDE.md, and saves your work to GitHub. By Module 6 this file is a
prompt library built from your own questions.

---

### 1.
Open the folder 00-rook/code/dispatch-routing/. This is the part of our software that decides who gets asked to take a job. I have never read code before and I am not going to start now. Walk me through what happens from the moment something goes wrong somewhere to the moment a responder's phone buzzes, in plain English, no jargon. Then tell me which file each step lives in.

### 2.
now fill this out for me: Based on what I found, the reason some responders are getting no pings at all is ___, because ___.

### 3.
and also the answer to marcus' question, in one sentence, the way you'd say it to him.

### 4.
consider how to code was tracking these cores and give me a response for marcus

### 5.
needs to be a one sentence response to marcus

### 6.
Find me the part of this code that takes points off somebody when they miss a ping or turn one down. Show it to me and explain it in plain English. Then find me every single thing in this code that puts points back on.

### 7.
Pressure-test the last 30 pings scoring recommendation. Compare 20, 30, and 40-ping windows to see which best protects reliable responders from short bad stretches without being too slow to identify someone who has genuinely stopped taking work. Also test whether home-area and out-of-area pings should be scored separately. Recommend the rule we should actually ship and make a simple visual comparing it with the current scoring system.

### 8.
Now turn this into a concrete recommendation for the 4.2 fix. Compare the current scoring rule with the proposed last-30, home/away split using the four locked-out responders and a few responders who stayed healthy. Show what would have happened to their ranking and ping volume under each rule, and identify any new risks the proposed rule introduces. Then give me the smallest change we can safely ship now, what should wait for a later release, and the metrics we should watch to know whether the fix worked. Also answer this in one sentence: According to my findings in the code, for someone who's gone quiet, they would need to ___ to earn their score back under the current system.

### 9.
If I'd only asked what the code does, not what it doesn't do, what would I have missed?

### 10.
now answer this in 1 sentence: What did the code tell you that no one at this company could have?

### 11.
quote the note

### 12.
just quote it

### 13.
Now test the three things that stand out in the routing code against the actual dispatch data: misses counting the same as turn-downs, scores never recovering on their own, and skills not filtering responders out of the ranking. For each one, show me whether it actually affected real callouts after 4.2, who was affected, and how much it contributed to unanswered callouts or responders becoming locked out. Separate what the code proves from what the data supports and what we're still assuming. Then rank these three behaviors by risk and tell me which one we should fix first, which can wait, and what evidence would change your recommendation. Keep it in plain English and make a simple visual showing where each issue sits in the path from incident → ranking → phone buzz → response → future ranking.

### 14.
Now simulate the main fixes we’re considering against the actual post-4.2 data: restore the wait from 60 to 90 seconds, stop treating missed pings the same as turn-downs, repair the four damaged scores, and add some form of score recovery over time. Test each change on its own first, then the most realistic combinations. For each scenario, estimate whether the four responders would still have become locked out, how quickly they would have recovered, and what would likely happen to our primary metric, the 4-week share of callouts nobody took, versus the current 11.2%. Be very clear about what can be replayed directly from the data versus what requires assumptions. Then recommend the smallest set of changes that addresses both the immediate 4.2 problem and prevents the same feedback loop from happening again, separating what should ship immediately from what can wait for a later release.

### 15.
My hypothesis is that the 4.2 change to who gets asked first applied to all existing responders based on their current history and score, not just new responders. Before looking at the post-release results, use the pre-4.2 data to predict which responders should have moved up or down in the ranking when the weighting changed, especially responders who had already been turning down or missing jobs. Then check the actual ping order and volume after 12 August to see whether those predictions happened. Pay particular attention to responders with a meaningful history before 4.2 and compare them with responders who had stronger acceptance histories. Show examples that support and contradict the hypothesis, and tell me whether the evidence is strong enough to answer Marcus’s question: did 4.2 immediately change the ranking of existing responders using their existing history, or did the new behavior only take effect as new decisions accumulated after the release? Separate what the data proves from what we can only infer.

### 16.
The biggest unanswered question now is why out-of-area responders suddenly started getting first offer much more often on 12–13 Aug, even though the increased distance weight should seemingly favor local responders. Test that directly. Compare the actual first-offer order before and immediately after 4.2 using only callouts that happened early enough that new misses and score changes could not yet explain the ranking. For each case where an out-of-area responder jumped ahead of the home responder, compare their estimated travel time, pre-4.2 history score, skills contribution if available, and resulting ranking under both the 4.1 and 4.2 weights. Identify which part of the scoring change would have been large enough to flip the order. Pay special attention to Vesper’s Old Town callouts and the unusual out-of-area first offers involving Captain Vantage, Farlight, and The Undertow. Then tell me whether the day-one shift can actually be explained by the new distance weighting, whether it points to a problem with the travel-time estimates, or whether there is still something in the ranking logic we haven’t accounted for. Separate what we can prove from what still requires Wen’s ranked-list replay, and show me a simple visual of the clearest before-versus-after ranking flip.

### 17.
Treat the new hypothesis as: 4.2 exposed a mismatch between who Dispatch thinks is closest and who actually serves an area. Test that without relying on missing travel-time or location data. Use the pre-4.2 history as evidence of actual responder behavior: for every responder-to-area pairing, calculate how often they were offered jobs there, how often they accepted them, and whether they were the home responder or a visitor. Then compare those behavioral patterns with who started getting first offer after 4.2. Are we systematically ranking responders first in areas where their historical acceptance rate is near zero, while pushing down responders who reliably take jobs there? Identify the clearest examples and exceptions, quantify how much of the post-4.2 increase in missed or unanswered callouts came from these mismatched pairings, and estimate how the outcome might differ if Dispatch incorporated area-specific acceptance history instead of one global history score. Finish by telling me whether the evidence points more strongly to bad location inputs, an incomplete ranking model, or both, and what specific result from Wen’s replay would distinguish between those explanations.

### 18.
Now test the consequence of this scoring math across all 16 responders. Since someone has to take 60% of their pings just to keep their score from falling, show me what happens when a responder temporarily falls below that threshold. For each responder, identify every stretch where their rolling take rate dropped below 60%, how far their score would have fallen, whether their ping volume then decreased, and whether they eventually recovered. Compare the four responders who became locked out with people like Nightwell who dipped below the threshold but recovered. I want to know what determines whether a bad stretch is recoverable versus becoming a feedback loop where fewer pings mean fewer chances to earn points back. Then test whether changing the penalty, acceptance credit, or adding automatic score recovery would have prevented the four lockouts without rewarding responders who consistently turn jobs down. Finish by recommending the simplest scoring change and show a visual of the current feedback loop versus the proposed safer version.
