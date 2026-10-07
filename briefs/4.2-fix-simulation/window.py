import random, math, statistics as st
from collections import deque
from load import *
from rules import rate, pois, PROF, C
random.seed(9)
def wscore(q): return sum(q)/len(q)
def replay(N, miss_w=1.0):
    q={r:deque([0.5]*N,maxlen=N) for r in NAMES}; low={r:1 for r in NAMES}; sc={}
    for c in C:
        for r,o in c['chain']:
            q[r].append(1.0 if o=='y' else (0.0 if o=='n' else 1-miss_w))
            if c['t']>=REL: low[r]=min(low[r],wscore(q[r]))
    return low,{r:wscore(q[r]) for r in NAMES}
def sim(N,prof,miss_w=1.0,runs=1500):
    ends=[]
    for _ in range(runs):
        q=deque([0.75]*N,maxlen=N)  # a responder with a normal track record
        for days,(py,pn,pm) in PROF[prof]:
            for d in range(days):
                for _ in range(pois(rate(wscore(q))/7)):
                    u=random.random(); o='y' if u<py else 'n' if u<py+pn else 'm'
                    q.append(1.0 if o=='y' else 0.0 if o=='n' else 1-miss_w)
        ends.append(wscore(q))
    return st.median(ends), sum(e<0.4 for e in ends)/runs
for N in (20,30,40):
    low,end=replay(N)
    oth=sum(1 for r in NAMES if r not in FOUR and low[r]<0.4)
    res=[sim(N,p) for p in PROF]
    print(f'share of last {N} pings taken: four lowest/6 Sep '+' '.join(f'{low[r]:.2f}/{end[r]:.2f}' for r in FOUR)+f' | others<0.4 {oth} | '+' | '.join(f'{k}: {m:.2f} ({100*s:.0f}% stuck)' for k,(m,s) in zip(PROF,res)))
