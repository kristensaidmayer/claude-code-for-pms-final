# 02 · Super Hearing — prompts

**Context:** You joined Rook two weeks ago as PM on Dispatch.
Release 4.2 shipped on 12 August, just before you arrived, and
landed badly. Last session you built a context file and met the
company.

You still do not know what actually went wrong.

At the end of the session, type wrap up, and Claude Code saves the
prompts you wrote yourself below — not the starter prompt — updates
CLAUDE.md, and saves your work to GitHub. By Module 6 this file is a
prompt library built from your own questions.

---

### 1.

Yes. Cross-check the four responders mentioned in these interviews against the rook-database. For each interview theme, tell me whether the behavioral data supports, contradicts, or can't verify what the handler described. Pay particular attention to ping volume before vs. after 4.2, missed vs. taken pings, whether any responder's volume declined after accumulating misses, and whether the 60-second timeout could plausibly explain what they reported. Do not expose responder-level data beyond the four people explicitly named in the interviews. Then tell me which customer complaints we should treat as validated product problems versus anecdotal or still unproven. Finally, identify anything surprising where what customers said and what the data shows don't line up.

### 2.

Based on everything we've learned from the customer interviews, database, and routing code, what should I do first as PM for Rook Dispatch? Compare restoring the 90-second timeout, changing the miss penalty, adding score recovery, fixing other routing issues, or waiting for more evidence.

Make one clear recommendation, explain what evidence supports it and what remains unproven, and give me the key metrics and guardrails I'd use to validate the change. Then give me a 60-second version I can use to explain the decision to the team.

### 3.

Based on the interviews, the trouble with 4.2 is ___?

### 4.

Use the rook-database connector to read the support_tickets table. Same treatment as before: group them, tell me how many are in each group, and quote one line from each.

### 5.

Dig into the mismatch between support tickets and actual responder impact. Compare the responders with quiet-phone tickets to the responders whose ping volume actually declined after 4.2. What distinguishes the people who complained from the people who were most affected but never filed tickets? Then tell me whether support-ticket volume is a reliable signal for Dispatch health, what it would have missed in this incident, and what metrics I should monitor instead.

### 6.

Using the database, test the health metrics you just proposed against the 4.2 incident. Build a simple Dispatch early-warning framework and tell me which metrics would have first detected the problem, on what date, and how much earlier they would have alerted us than support tickets or the existing acceptance metric. Recommend 3–5 metrics I should put on a PM dashboard, with thresholds for when the team should investigate. Keep everything aggregated and explain any threshold you can't justify from the available data.

### 7.

Turn this into a lightweight monitoring and response plan for Dispatch. For the five dashboard metrics, define what happens when one crosses its threshold: who should investigate, what they should check first, and when it should become a release-blocking issue. Then use the 4.2 incident as a test case and show me how this process would have changed what the team did between 12–19 Aug. Keep it concise and practical enough that I could propose it to the team.

### 8.

Only look at what came in after 12 August. What's different about these compared to everything before?

### 9.

You've now read both folders (interviews and tickets). Where do they disagree? What's loud in the interviews but rare in the tickets, and what's all over the tickets that nobody brought up in the interviews?

### 10.

Given these gaps between interviews and support tickets, what are we at risk of getting wrong if we rely too heavily on either source? Identify the 5 biggest blind spots in our current customer understanding, explain why each matters for Dispatch, and tell me the specific question or research method you'd use to validate each one. Prioritize them by which could most change our product roadmap.

### 11.

Turn these five blind spots into a prioritized research plan. Assume I only have time to investigate 3 before making roadmap decisions. Pick the 3 that could most change what we build, explain why, and for each give me the exact question to answer, who we need to hear from, what data to check, and what finding would actually change the roadmap. Keep it practical and don’t recommend features yet.

### 12.

Now turn this into a roadmap decision framework. For each of the three studies, tell me what we should do if the evidence supports the hypothesis, what we should do if it disproves it, and what we should do if the result is inconclusive. Then give me the order you’d make the Dispatch decisions in, including what we can safely decide now versus what should wait for research. End with the 3 decisions I should be prepared to make with Helen at the end of week 3.

### 13.

based on everything, the trouble with 4.2 is what?

### 14.

Assume both the interviews and support tickets are telling the truth. How can they both be right? Build me one coherent explanation of the customer experience that accounts for the apparent contradictions between them. Tell me what each source sees that the other misses, what looks contradictory but actually isn't, and what this changes about how I should understand and prioritize the problems in Dispatch.
