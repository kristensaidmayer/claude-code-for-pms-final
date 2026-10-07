import random, math, statistics as st, datetime as dt
from load import *
random.seed(5); C=load()
def make(credit=0.08, td=0.12, miss=0.12, rec=None, floor=0.0, miss_streak=None, area_only=False):
    def rule(): return dict(credit=credit,td=td,miss=miss,rec=rec,floor=floor,streak=miss_streak,area=area_only)
    return rule()
RULES={
 'Current (+0.08 / -0.12 / -0.12)':make(),
 'Smaller penalty (-0.08 each)':make(td=0.08,miss=0.08),
 'Bigger credit (+0.12)':make(credit=0.12),
 'Misses free':make(miss=0),
 'Misses cost -0.04':make(miss=0.04),
 'Misses free unless 3 in a row':make(miss=0,miss_streak=3),
 'Auto-recovery to 0.5 (up only, 14d)':make(rec=14),
 'Floor at 0.3':make(floor=0.3),
 'Area-only history (home pings only)':make(area_only=True),
 '3-in-a-row misses + auto-recovery':make(miss=0,miss_streak=3,rec=14),
}
def apply(s,o,R,streak):
    if o=='y': return min(1,s+R['credit']),0
    if o=='n': return max(R['floor'],s-R['td']),0
    streak+=1
    cost=R['miss']
    if R['streak'] and streak>=R['streak']: cost=R['td']; streak=0
    return max(R['floor'],s-cost),streak
def recov(s,days,R):
    if R['rec'] and s<0.5: s=0.5-(0.5-s)*0.5**(days/R['rec'])
    return s
def replay(R):
    s={r:0.5 for r in NAMES}; k={r:0 for r in NAMES}; last={r:C[0]['t'] for r in NAMES}; low={r:1 for r in NAMES}
    for c in C:
        for r,o in c['chain']:
            if R['area'] and HOME[r]!=c['area']: continue
            s[r]=recov(s[r],(c['t']-last[r]).total_seconds()/86400,R); last[r]=c['t']
            s[r],k[r]=apply(s[r],o,R,k[r])
            if c['t']>=REL: low[r]=min(low[r],s[r])
    end=dt.datetime(2026,9,7)
    for r in NAMES: s[r]=recov(s[r],(end-last[r]).total_seconds()/86400,R)
    return low,s
def rate(s): return 2 if s<0.4 else 12 if s>=0.7 else 2+10*(s-0.4)/0.3
def pois(l):
    L=math.exp(-l);k=0;p=1
    while True:
        p*=random.random()
        if p<L: return k
        k+=1
PROF={'good, bad fortnight':[(14,(0.23,0.18,0.59)),(70,(0.755,0.216,0.029))],
      'always turns down':[(84,(0.40,0.57,0.03))],
      'never answers':[(84,(0.40,0.03,0.57))],
      'steady reliable':[(84,(0.755,0.216,0.029))]}
def sim(R,prof,N=1500):
    ends=[]
    for _ in range(N):
        s=0.9;k=0
        for days,(py,pn,pm) in PROF[prof]:
            for d in range(days):
                s=recov(s,1,R)
                for _ in range(pois(rate(s)/7)):
                    u=random.random(); o='y' if u<py else 'n' if u<py+pn else 'm'
                    s,k=apply(s,o,R,k)
        ends.append(s)
    return st.median(ends), sum(e<0.4 for e in ends)/N
print(f"{'rule':38s} {'four: lowest / 6 Sep':28s} {'others <0.4':>11s} | 12-week score (share stuck <0.4): good+bad fortnight | always turns down | never answers | steady reliable")
for name,R in RULES.items():
    low,end=replay(R)
    four=' '.join(f'{low[r]:.2f}/{end[r]:.2f}' for r in FOUR)
    oth=sum(1 for r in NAMES if r not in FOUR and low[r]<0.4)
    res=[sim(R,p) for p in PROF] if not R['area'] else None
    tail=' | '.join(f'{m:.2f} ({100*q:3.0f}%)' for m,q in res) if res else '(needs area data; replay only)'
    print(f'{name:38s} {four:28s} {oth:>11d} | {tail}')
