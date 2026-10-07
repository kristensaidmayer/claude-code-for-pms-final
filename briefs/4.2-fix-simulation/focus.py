import datetime as dt
from load import *
C=load(); END=dt.datetime(2026,8,18)
s={r:0.5 for r in NAMES}
def need(dH):
    # minimum estimated travel-time advantage (minutes) the visitor needs to outrank home under each weighting, if skills are equal
    old=max(0,-0.40*dH/0.45*45); new=max(0,-0.25*dH/0.60*45)
    return old,new
print('Rule (skills equal): visitor wins if 0.45*dP > -0.40*dH under 4.1, 0.60*dP > -0.25*dH under 4.2  (dP = minutes closer / 45)\n')
for c in C:
    if REL<=c['t']<END:
        names=[r for r,_ in c['chain']]
        homes=[r for r in NAMES if HOME[r]==c['area']]
        f=names[0]
        if c['area']=='k' or 'P' in names or (f in 'ADO' and f not in homes):
            h=homes[0] if homes else None
            pos={r:i+1 for i,r in enumerate(names)}
            ahead=[r for r in names[:pos.get(h,len(names)+1)-1]] if h in pos else names
            line=f"{c['t']:%d %b %H:%M} {AREAS[c['area']]:12s} order: "+' > '.join(f"{NAMES[r]}[{o}] {s[r]:.2f}" for r,o in c['chain'])
            if h in pos and pos[h]>1:
                v=names[0]; dH=s[v]-s[h]; o,n=need(dH)
                line+=f"  || home {NAMES[h]} ranked #{pos[h]}; visitor-minus-home history {dH:+.2f}; to beat home visitor must be est. closer by >= {o:.1f} min (4.1) / {n:.1f} min (4.2)"
            print(line)
    for r,o in c['chain']: s[r]=max(0,min(1,s[r]+(0.08 if o=='y' else -0.12)))
print('\nVesper pre-4.2: first-in-line where?')
from collections import Counter
cnt=Counter(); tot=Counter()
for c in C:
    if c['t']<REL and any(r=='P' for r,_ in c['chain']):
        tot[AREAS[c['area']]]+=1
        if c['chain'][0][0]=='P': cnt[AREAS[c['area']]]+=1
print({a:f'{cnt[a]}/{tot[a]}' for a in tot})
