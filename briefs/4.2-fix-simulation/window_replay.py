import datetime as dt
from collections import deque, defaultdict
from load import *
C=load(); E=dt.datetime(2026,9,7)
def replay(N,mode):
    h={r:deque([0.5]*N,maxlen=N) for r in NAMES}; a={r:deque([0.5]*N,maxlen=N) for r in NAMES}
    low={r:1 for r in NAMES}; need=[]
    for c in C:
        f=c['chain'][0][0]; homes=[r for r in NAMES if HOME[r]==c['area']]
        if c['t']>=REL and f not in homes and mode=='split' and homes:
            hs=max(sum(h[x])/N for x in homes); va=sum(a[f])/N
            need.append(max(0,0.25*(hs-va)/0.60*45))
        for r,o in c['chain']:
            x=1.0 if o=='y' else 0.0; home=HOME[r]==c['area']
            if mode=='combined' or home: h[r].append(x)
            else: a[r].append(x)
            if c['t']>=REL: low[r]=min(low[r],sum(h[r])/N)
    return low,{r:sum(h[r])/N for r in NAMES},{r:sum(a[r])/N for r in NAMES},need
def tally():
    s={r:0.5 for r in NAMES}; low={r:1 for r in NAMES}
    for c in C:
        for r,o in c['chain']:
            s[r]=max(0,min(1,s[r]+(0.08 if o=='y' else -0.12)))
            if c['t']>=REL: low[r]=min(low[r],s[r])
    return low,s
l,e=tally()
print('REAL HISTORY (pings as they happened). Four = Farlight, Meteor Mite, The Undertow, Vesper')
print(f"  Current tally        four lowest/6 Sep: {' '.join(f'{l[r]:.2f}/{e[r]:.2f}' for r in FOUR)} | others ever <0.4: {sum(1 for r in NAMES if r not in FOUR and l[r]<0.4)}")
for N in (20,30,40):
    for mode in ('combined','split'):
        l,e,a,need=replay(N,mode)
        extra=''
        if mode=='split':
            extra=f" | visitor-first callouts after 4.2: visitor would need to be rated >=10 min closer in {sum(x>=10 for x in need)}/{len(need)} (median {sorted(need)[len(need)//2]:.0f} min)"
        print(f"  Last {N}, {mode:8s}   four lowest/6 Sep: {' '.join(f'{l[r]:.2f}/{e[r]:.2f}' for r in FOUR)} | others ever <0.4: {sum(1 for r in NAMES if r not in FOUR and l[r]<0.4)}{extra}")
l,e,a,need=replay(30,'split')
print('\nLast 30 split, out-of-area score on 6 Sep (share of last 30 away pings taken, padded with 0.5 at start):')
print('  '+', '.join(f'{NAMES[r]} {a[r]:.2f}' for r in sorted(NAMES,key=lambda r:-a[r])))
