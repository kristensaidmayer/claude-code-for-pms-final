# 01 · Origin Story — prompts

**Context:** Rook Industries makes software for superheroes and the
people who handle them.

There are two products. Rook Dispatch is the one that gets a
superhero to where they're needed when there's an emergency — it
works out who is close enough and free enough to help, and gets hold
of them. Rook Supply keeps a responder's equipment serviceable and
accounted for, so a handler is never guessing whether the gear will
hold.

You joined two weeks ago as PM on Rook Dispatch. Release 4.2 shipped
on 12 August, shortly before you arrived. Responders have stopped
answering their phones the way they used to, and complaints have
gone up sharply. You were not in the room for any of it.

At the end of the session, type wrap up, and Claude Code saves the
prompts you wrote yourself below — not the starter prompt — updates
CLAUDE.md, and saves your work to GitHub. By Module 6 this file is a
prompt library built from your own questions.

---

### 1.

I just joined Rook Industries as PM for Rook Dispatch. Read everything in 00-rook/company/ and the company notes from the company wiki through the rook-wiki connector and add to the CLAUDE.md at the root of this folder, what you'd need to know to help me do my job here: the products, the people, the vocabulary, where things stand. Leave the session scope block at the top. Keep it under two pages.

### 2.

Based on what you added to CLAUDE.md, what are the 5 most important questions I should get answered in my first two weeks as PM for Rook Dispatch? For each, tell me why it matters and who at Rook is most likely to have the answer.

### 3.

Put yourself in my shoes as the new PM for Rook Dispatch. Based on everything you’ve read and the five questions you just identified, write me a concise “first week brief”: what you believe is happening with Dispatch right now, what you think is most likely causing the 4.2 issues, what you would investigate before making any product decision, and the first 3 actions you would take if you were me. Clearly separate facts from hypotheses, and call out anything you would not trust yet because the evidence is incomplete or conflicting.

### 4.

What's contradictory or missing, not just in the company documents, but across everything in 00-rook?

### 5.

Act as a skeptical senior PM reviewing your analysis. Try to disprove your current theory that the 4.2 ranking changes are driving the Dispatch problems. What alternative explanations could produce the same symptoms? For each one, tell me what evidence would distinguish it from the ranking hypothesis. Then tell me the minimum data I need before I can confidently recommend a fix, revert, or no change.

### 6.

Yes. Run items 1–5 against the rook-database now. Compare the periods before and after the 12 Aug 4.2 release and show me what the data actually says about each hypothesis. Use counts and aggregate metrics only, with no individual responder identities. For each analysis, explain what you measured, the result, and whether it strengthens or weakens the ranking-change, ping-timeout, push-delivery, seasonality, or demand/supply explanations. Then give me your updated assessment of the most likely cause, including how confident you are and what still cannot be determined from the available data. Do not recommend a solution yet.

### 7.

You are now the PM responsible for deciding what happens next with Rook Dispatch. Based on all the evidence you've gathered, give me your recommendation for what we should do about 4.2. Consider at least these options: full revert, restore only the 90-second ping timeout, change how missed pings affect ranking, or leave 4.2 in place while gathering more evidence. For each option, explain the expected benefit, risk, what problem it does and does not solve, and how reversible it is. Then make one clear recommendation and defend it. Give me a rollout and validation plan with specific success metrics and guardrails, plus what evidence would cause you to reverse your decision. Finally, draft the 60-second version I should say in a meeting with Helen, Wen, Marcus, and Ravi. Do not assume missing evidence is fact, and explicitly distinguish what the data proves from what we are still inferring.
