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
