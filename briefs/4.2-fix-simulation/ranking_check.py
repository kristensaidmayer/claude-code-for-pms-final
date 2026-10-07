import datetime as dt
from load import *
C=load()
D=lambda m,d,h=0: dt.datetime(2026,m,d,h)
def hist_at(cut):
    s={r:0.5 for r in NAMES}
    for c in C:
        if c['t']>=cut: break
        for r,o in c['chain']: s[r]=max(0,min(1,s[r]+(0.08 if o=='y' else -0.12)))
    return s
H=hist_at(REL)
pre=[c for c in C if c['t']<REL]; days_pre=(REL-C[0]['t']).days+1
def stats(S, days):
    out={}
    for r in NAMES:
        p=[(c,i,o) for c in S for i,(rr,o) in enumerate(c['chain']) if rr==r]
        home=[c for c in S if c['area']==HOME[r]]
        first_home=sum(1 for c in home if c['chain'][0][0]==r)
        out[r]=dict(perwk=7*len(p)/days, away=sum(1 for c,i,o in p if c['area']!=HOME[r])/max(1,len(p)),
            first_home=first_home/max(1,len(home)), nhome=len(home),
            tk=sum(1 for *_,o in p if o=='y'), td=sum(1 for *_,o in p if o=='n'), ms=sum(1 for *_,o in p if o=='m'), n=len(p))
    return out
P=stats(pre,days_pre)
print('PRE-4.2 (29 Jun-11 Aug): replayed history score on 11 Aug, take rate, pings/wk, first-in-line share of own-area callouts')
for r in sorted(NAMES,key=lambda r:H[r]):
    x=P[r]; print(f"{NAMES[r]:18s} hist {H[r]:.2f}  take {x['tk']}/{x['n']}={x['tk']/x['n']:.0%} td {x['td']} miss {x['ms']}  {x['perwk']:4.1f}/wk  first-at-home {x['first_home']:.0%}  away-share {x['away']:.0%}")
# turn-down/miss history in last 3 weeks pre
print()
win=[('pre (6.3 wk)',C[0]['t'],REL),('12-13 Aug',D(8,12),D(8,14)),('14-17 Aug',D(8,14),D(8,18)),('18 Aug-6 Sep',D(8,18),D(9,7))]
print('FIRST-IN-LINE share of own-area callouts, and pings/wk, by period')
print(' '*18+''.join(f'{w[0]:>22s}' for w in win))
for r in sorted(NAMES,key=lambda r:H[r]):
    row=f'{NAMES[r]:18s}'
    for lab,a,b in win:
        S=[c for c in C if a<=c['t']<b]; x=stats(S,(b-a).total_seconds()/86400)[r]
        row+=f"{x['first_home']:>8.0%} ({x['nhome']:2d}) {x['perwk']:5.1f}/wk"
    print(row)
# out-of-area first pings overall
print()
for lab,a,b in win:
    S=[c for c in C if a<=c['t']<b]
    fa=sum(1 for c in S if HOME[c['chain'][0][0]]!=c['area'] and not (c['area']=='a' and c['chain'][0][0] in 'GM'))
    print(f'{lab:14s} callouts {len(S):4d}  first ping went to an out-of-area responder: {fa} ({fa/len(S):.0%})')
