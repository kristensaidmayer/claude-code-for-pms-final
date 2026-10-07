import random, math, statistics as st, datetime as dt
from collections import deque
from load import *
random.seed(21); C=load()
def rate(s): return 2 if s<0.4 else 12 if s>=0.7 else 2+10*(s-0.4)/0.3
def pois(l):
    L=math.exp(-l);k=0;p=1
    while True:
        p*=random.random()
        if p<L: return k
        k+=1
# ---------- scorers ----------
class Tally:
    def __init__(s,init): s.v=0.9
    def add(s,o,home): s.v=max(0,min(1,s.v+(0.08 if o=='y' else -0.12)))
    def score(s): return s.v
class Window:
    def __init__(s,N,mode,init):
        s.mode=mode
        s.h=deque(init(N,True),maxlen=N); s.a=deque(init(N,False),maxlen=N) if mode=='split' else None
    def add(s,o,home):
        x=1.0 if o=='y' else 0.0
        if s.mode=='combined': s.h.append(x)
        elif s.mode=='home-only':
            if home: s.h.append(x)
        else: (s.h if home else s.a).append(x)
    def score(s): return sum(s.h)/len(s.h)
NORMAL_HOME=(0.92,0.07,0.01); AWAY=(0.0,0.9,0.1); AWAY_SHARE=0.17
def draw(p):
    u=random.random(); return 'y' if u<p[0] else 'n' if u<p[0]+p[1] else 'm'
def init_hist(N,home,combined_mode=None):
    # a reliable responder's recent record
    out=[]
    for _ in range(N):
        if combined_mode=='combined' and random.random()<AWAY_SHARE: out.append(1.0 if draw(AWAY)=='y' else 0.0)
        else: out.append(1.0 if draw(NORMAL_HOME if home else AWAY)=='y' else 0.0)
    return out
def run(make, phases):
    sc=make(); trace=[]
    for days,home_p,away_share in phases:
        for d in range(days):
            for _ in range(pois(rate(sc.score())/7)):
                home=random.random()>away_share
                sc.add(draw(home_p if home else AWAY),home)
            trace.append(sc.score())
    return trace
SCORERS={'Current tally':lambda:Tally(None)}
for N in (20,30,40):
    for mode in ('combined','split'):
        SCORERS[f'Last {N}, {mode}']=(lambda N=N,mode=mode:Window(N,mode,lambda n,h,mode=mode:init_hist(n,h,mode)))
SHOCK=[(14,(0.38,0.09,0.53),0.40),(70,NORMAL_HOME,AWAY_SHARE)]          # the four's 4.2 fortnight, then normal
PHONE=[(7,(0.0,0.0,1.0),AWAY_SHARE),(77,NORMAL_HOME,AWAY_SHARE)]         # a week of answering nothing
STOP=[(14,NORMAL_HOME,AWAY_SHARE),(70,(0.10,0.80,0.10),AWAY_SHARE)]      # genuinely stops taking work on day 14
STEADY=[(84,NORMAL_HOME,AWAY_SHARE)]
R=1500
print(f"{'scorer':24s}| bad fortnight: fell<0.4 / stuck day 84 | week of no answers: fell<0.4 / stuck | stopped working: days to <0.5 , <0.4 (median, 90th) | steady: ever<0.4 | steady score")
for name,mk in SCORERS.items():
    a=[run(mk,SHOCK) for _ in range(R)]; b=[run(mk,PHONE) for _ in range(R)]; c=[run(mk,STOP) for _ in range(R)]; d=[run(mk,STEADY) for _ in range(R)]
    f=lambda T:(sum(min(t)<0.4 for t in T)/R, sum(t[-1]<0.4 for t in T)/R)
    def det(th):
        ds=[next((i-14 for i,x in enumerate(t) if i>=14 and x<th),999) for t in c]; ds.sort(); return ds[R//2],ds[9*R//10]
    print(f"{name:24s}| {100*f(a)[0]:4.0f}% / {100*f(a)[1]:3.0f}%            | {100*f(b)[0]:4.0f}% / {100*f(b)[1]:3.0f}%               | {det(0.5)} , {det(0.4)}                 | {100*f(d)[0]:4.0f}%       | {st.median(t[-1] for t in d):.2f}")

print('\n== stopped working: days until score falls below 0.7 (where ping volume starts to drop) ==')
for name,mk in SCORERS.items():
    c=[run(mk,STOP) for _ in range(R)]
    ds=sorted(next((i-14 for i,x in enumerate(t) if i>=14 and x<0.7),999) for t in c)
    print(f'  {name:24s} median {ds[R//2]} days, 90th pct {ds[9*R//10]}')
