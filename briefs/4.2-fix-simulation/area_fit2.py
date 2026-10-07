import datetime as dt
from collections import Counter, defaultdict
from load import *
C=load(); pre=[c for c in C if c['t']<REL]; post=[c for c in C if c['t']>=REL]
home=lambda r,a: HOME[r]==a
E=dt.datetime(2026,8,18)
# away takes by period and by whether the area's home responder was one of the four
for lab,a,b in [('12-17 Aug',REL,E),('18 Aug-6 Sep',E,dt.datetime(2026,9,7))]:
    for grp in ('four\'s areas','other areas'):
        L=[(r,o) for c in C if a<=c['t']<b for r,o in c['chain'] if not home(r,c['area']) and ((c['area'] in {HOME[x] for x in FOUR})==(grp=="four's areas"))]
        print(f'away pings {lab:13s} {grp:13s}: {len(L):3d} taken {sum(o=="y" for _,o in L):3d} ({sum(o=="y" for _,o in L)/max(1,len(L)):.0%})')
# home-first unanswered: what happened after the home responder
print('\nUnanswered callouts where the home responder was asked first (post-4.2):')
U=[c for c in post if home(c['chain'][0][0],c['area']) and not any(o=='y' for _,o in c['chain'])]
print(' home outcome:',Counter(c['chain'][0][1] for c in U),' | nobody else asked:',sum(1 for c in U if len(c['chain'])==1),' | visitors asked next and failed:',sum(1 for c in U if len(c['chain'])>1))
Upre=[c for c in pre if home(c['chain'][0][0],c['area']) and not any(o=='y' for _,o in c['chain'])]
print(' pre-4.2 same:',Counter(c['chain'][0][1] for c in Upre),' nobody else asked:',sum(1 for c in Upre if len(c['chain'])==1))
# counterfactual: area-specific ranking puts the home responder first when they were available (= appears in the chain)
V=[c for c in post if not home(c['chain'][0][0],c['area'])]
withhome=[c for c in V if any(home(r,c['area']) for r,_ in c['chain'])]
nohome=[c for c in V if not any(home(r,c['area']) for r,_ in c['chain'])]
hout=Counter(next(o for r,o in c['chain'] if home(r,c['area'])) for c in withhome)
wasted=sum(next(i for i,(r,_) in enumerate(c['chain']) if home(r,c['area'])) for c in withhome)
print(f'\nVisitor-first callouts post-4.2: {len(V)}. Home responder later in the chain (so available): {len(withhome)}; home outcome there {dict(hout)}; pings before reaching home: {wasted}')
print(f'  missed pings before reaching home: {sum(1 for c in withhome for r,o in c["chain"][:next(i for i,(r,_) in enumerate(c["chain"]) if home(r,c["area"]))] if o=="m")}')
print(f'  home never asked: {len(nohome)}; visitor took it in {sum(1 for c in nohome if any(o=="y" for _,o in c["chain"]))}; unanswered {sum(1 for c in nohome if not any(o=="y" for _,o in c["chain"]))}')
print(f'  ...of which home was one of the four: {sum(1 for c in nohome if c["area"] in {HOME[x] for x in FOUR})}')
# area-specific score replay for the four: score moves only on home-area pings
def replay(area_only):
    s=defaultdict(lambda:0.5); low={}; out={}
    for c in C:
        for r,o in c['chain']:
            if area_only and not home(r,c['area']): continue
            s[r]=max(0,min(1,s[r]+(0.08 if o=='y' else -0.12)))
            if c['t']>=REL: low[r]=min(low.get(r,1),s[r])
    return {r:(low.get(r),s[r]) for r in FOUR}
g=replay(False); a=replay(True)
print('\nScore replay for the four (observed pings), lowest after 4.2 / end:')
for r in FOUR: print(f'  {NAMES[r]:13s} global history {g[r][0]:.2f}/{g[r][1]:.2f}   home-area-only history {a[r][0]:.2f}/{a[r][1]:.2f}')
# share of score damage from away pings for the four, 12-17 Aug
for r in FOUR:
    aw=[o for c in C if REL<=c['t']<E for rr,o in c['chain'] if rr==r and not home(r,c['area'])]
    hm=[o for c in C if REL<=c['t']<E for rr,o in c['chain'] if rr==r and home(r,c['area'])]
    print(f'  {NAMES[r]:13s} 12-17 Aug away pings {len(aw)} (taken {aw.count("y")}) score effect {sum(0.08 if o=="y" else -0.12 for o in aw):+.2f} | home pings {len(hm)} (taken {hm.count("y")}) effect {sum(0.08 if o=="y" else -0.12 for o in hm):+.2f}')
