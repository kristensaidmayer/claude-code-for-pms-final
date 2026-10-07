import datetime as dt
from collections import deque, defaultdict
from load import *
C=load(); D=lambda m,d:dt.datetime(2026,m,d)
SEL=FOUR+['H','K','I','M','J']   # Nightwell, Stormwrack, Bulwark, The Gale, Falkirk
def vol(s): return 2 if s<0.4 else 12 if s>=0.7 else 2+10*(s-0.4)/0.3
# replay both rules on the real pings; snapshot at dates
snaps=[D(8,12),D(8,18),D(9,7)]
cur={r:0.5 for r in NAMES}; hw={r:deque([0.5]*30,maxlen=30) for r in NAMES}; aw={r:deque([0.0]*30,maxlen=30) for r in NAMES}
S=defaultdict(dict); low=defaultdict(lambda:[1,1]); si=0
for c in C:
    while si<len(snaps) and c['t']>=snaps[si]:
        for r in NAMES: S[r][si]=(cur[r],sum(hw[r])/30,sum(aw[r])/30)
        si+=1
    for r,o in c['chain']:
        x=1.0 if o=='y' else 0.0
        cur[r]=max(0,min(1,cur[r]+(0.08 if o=='y' else -0.12)))
        (hw if HOME[r]==c['area'] else aw)[r].append(x)
        if c['t']>=REL: low[r][0]=min(low[r][0],cur[r]); low[r][1]=min(low[r][1],sum(hw[r])/30)
while si<len(snaps):
    for r in NAMES: S[r][si]=(cur[r],sum(hw[r])/30,sum(aw[r])/30)
    si+=1
def obs(r,a,b,home=True):
    return 7*sum(1 for c in C if a<=c['t']<b for rr,_ in c['chain'] if rr==r and (HOME[r]==c['area'])==home)/((b-a).days)
def first_home(r,a,b):
    A=[c for c in C if a<=c['t']<b and c['area']==HOME[r]]
    return sum(1 for c in A if c['chain'][0][0]==r)/len(A)
# strongest visitor seen in each area after 4.2
vis=defaultdict(set)
for c in C:
    if c['t']>=REL:
        for r,_ in c['chain']:
            if HOME[r]!=c['area']: vis[c['area']].add(r)
print(f"{'responder':16s}| CURRENT: score 12Aug/low/6Sep  home pings/wk pre->after18Aug  first at home pre->post | PROPOSED home score 12Aug/low/6Sep  modeled volume 6Sep | visitor must be closer by (min) current vs proposed")
for r in SEL:
    s0,s1,s2=S[r][0],S[r][1],S[r][2]
    vs=[v for v in vis[HOME[r]] if v!=r]
    cur_need=max(0,18.75*(s2[0]-max(S[v][2][0] for v in vs)))
    pro_need=max(0,18.75*(s2[1]-max(S[v][2][2] for v in vs)))
    print(f"{NAMES[r]:16s}| {s0[0]:.2f}/{low[r][0]:.2f}/{s2[0]:.2f}   {obs(r,C[0]['t'],REL):4.1f} -> {obs(r,D(8,18),D(9,7)):4.1f}    {first_home(r,C[0]['t'],REL):.0%} -> {first_home(r,REL,D(9,7)):.0%} | {s0[1]:.2f}/{low[r][1]:.2f}/{s2[1]:.2f}   ~{vol(s2[1]):.0f}/wk (current-rule model ~{vol(s2[0]):.0f}/wk) | {cur_need:4.1f} vs {pro_need:4.1f}")
print('\nOut-of-area scores on 6 Sep (proposed, seeded at 0):', ', '.join(f'{NAMES[r]} {S[r][2][2]:.2f}' for r in sorted(NAMES,key=lambda r:-S[r][2][2])[:6]))
