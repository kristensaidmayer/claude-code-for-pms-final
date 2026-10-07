import random, statistics as st, datetime as dt, math
from load import *
random.seed(11)
C=load()
pre=[c for c in C if c['t']<REL]; post=[c for c in C if c['t']>=REL]
def rates(S, who):
    o=[x for c in S for r,x in c['chain'] if r in who]; n=len(o); return {k:o.count(k)/n for k in 'ynm'}
F={'90':rates(pre,set(FOUR)),'60':rates(post,set(FOUR))}
# pings per week vs score (ASSUMPTION calibrated to the four: ~12/wk before, ~2/wk once locked out)
def rate(s): return 2 if s<0.4 else 12 if s>=0.7 else 2+10*(s-0.4)/0.3
def poisson(l):
    L=math.exp(-l);k=0;p=1
    while True:
        p*=random.random()
        if p<L: return k
        k+=1
def run(s0, days, wait, mc, rec, repair_day=None, repair_to=0.9):
    s=s0; low=s0; rec_day=None; relock=None; hist=[]
    for d in range(days):
        if repair_day is not None and d==repair_day: s=max(s,repair_to)
        if rec=='both': s=0.5+(s-0.5)*0.5**(1/14)
        elif rec=='up' and s<0.5: s=0.5-(0.5-s)*0.5**(1/14)
        for _ in range(poisson(rate(s)/7)):
            u=random.random(); p=F[wait]
            o='y' if u<p['y'] else 'n' if u<p['y']+p['n'] else 'm'
            s=max(0,min(1,s+{'y':0.08,'n':-0.12,'m':-mc}[o]))
        low=min(low,s)
        if rec_day is None and s>=0.7: rec_day=d
        if relock is None and s<0.4: relock=d
        hist.append(s)
    return low,s,rec_day,relock,hist
N=3000
print('== MODELED: would the four have been locked out in the 26 days after 4.2? (start = their 11 Aug score ~0.92) ==')
for lab,wait,mc,rec in [('Current (60s, miss=decline)','60',0.12,None),('90s only','90',0.12,None),('Misses cost 0 (60s)','60',0,None),
    ('Misses cost half (60s)','60',0.06,None),('Ease back both ways (60s)','60',0.12,'both'),('Ease back up-only (60s)','60',0.12,'up'),
    ('90s + misses 0','90',0,None),('90s + misses half','90',0.06,None),('90s + up-only ease','90',0.12,'up'),('90s + both-ways ease','90',0.12,'both')]:
    R=[run(0.92,26,wait,mc,rec) for _ in range(N)]
    end_locked=sum(1 for r in R if r[1]<0.4)/N; ever=sum(1 for r in R if r[0]<0.4)/N
    print(f'{lab:32s} ever below 0.4: {100*ever:5.1f}%   still below 0.4 at 6 Sep: {100*end_locked:5.1f}%   median end score {st.median(r[1] for r in R):.2f}')
print('\n== MODELED: recovery after a fix ships, starting from today\'s score of 0 (180-day horizon) ==')
def summ(R,days):
    rd=[r[2] for r in R if r[2] is not None]
    pct=lambda q: sorted(rd)[int(q*len(rd))] if rd else None
    return (100*len(rd)/len(R), st.median(rd) if rd else None, pct(0.9) if len(rd)>len(R)*0.5 else None)
for lab,wait,mc,rec,rep in [('Nothing changes','60',0.12,None,None),('90s only','90',0.12,None,None),('Misses 0 only (60s)','60',0,None,None),
    ('Up-only ease only (60s)','60',0.12,'up',None),('Repair only (60s)','60',0.12,None,0),('90s + misses 0 (no repair)','90',0,None,None),
    ('90s + up-only ease (no repair)','90',0.12,'up',None),('90s + repair','90',0.12,None,0),('90s + repair + misses half','90',0.06,None,0),
    ('90s + repair + misses 0','90',0,None,0),('90s + repair + up-only ease','90',0.12,'up',0),('All: 90s+repair+miss half+up-ease','90',0.06,'up',0)]:
    R=[run(0.0,180,wait,mc,rec,rep) for _ in range(N)]
    share,med,p90=summ(R,180)
    relock=sum(1 for r in R if rep is not None and r[3] is not None and r[3]<=28)/N
    end=st.median(r[1] for r in R)
    print(f'{lab:36s} reach 0.7: {share:5.1f}%  median day {med}  90th pct day {p90}  | relocked within 28d: {100*relock:4.1f}% | median score day 180 {end:.2f}')
# resilience test: a 2-week shock where misses jump back to post-4.2 levels (e.g. push outage) after recovery
print('\n== MODELED: future shock — 14 days of 60s-style missing for a healthy responder (score 0.92), then normal 90s ==')
def shock(mc,rec):
    s=0.92; 
    for d in range(14+60):
        wait='60' if d<14 else '90'
        if rec=='up' and s<0.5: s=0.5-(0.5-s)*0.5**(1/14)
        for _ in range(poisson(rate(s)/7)):
            u=random.random(); p=F[wait]; o='y' if u<p['y'] else 'n' if u<p['y']+p['n'] else 'm'
            s=max(0,min(1,s+{'y':0.08,'n':-0.12,'m':-mc}[o]))
        if d==13: after=s
    return after,s
for lab,mc,rec in [('Miss = decline, no recovery',0.12,None),('Miss half',0.06,None),('Miss 0',0,None),('Miss = decline + up-only ease',0.12,'up'),('Miss half + up-only ease',0.06,'up')]:
    R=[shock(mc,rec) for _ in range(N)]
    print(f'{lab:32s} below 0.4 after shock: {100*sum(1 for a,b in R if a<0.4)/N:5.1f}%   still below 0.4 60 days later: {100*sum(1 for a,b in R if b<0.4)/N:5.1f}%')
