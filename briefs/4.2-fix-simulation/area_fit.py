import datetime as dt
from collections import defaultdict, Counter
from load import *
C=load()
pre=[c for c in C if c['t']<REL]; post=[c for c in C if c['t']>=REL]
# ---- 1. pre-4.2 behaviour per responder-area pair
P=defaultdict(lambda:dict(off=0,tk=0,td=0,ms=0,first=0))
for c in pre:
    for i,(r,o) in enumerate(c['chain']):
        d=P[(r,c['area'])]; d['off']+=1; d[{'y':'tk','n':'td','m':'ms'}[o]]+=1
        if i==0: d['first']+=1
home=lambda r,a: HOME[r]==a
H=[(k,v) for k,v in P.items() if home(*k)]; V=[(k,v) for k,v in P.items() if not home(*k)]
print('PRE-4.2 BEHAVIOUR')
print(f"home pairs: {len(H)}  offers {sum(v['off'] for _,v in H)}  taken {sum(v['tk'] for _,v in H)} ({sum(v['tk'] for _,v in H)/sum(v['off'] for _,v in H):.0%})  take-rate range {min(v['tk']/v['off'] for _,v in H):.0%}-{max(v['tk']/v['off'] for _,v in H):.0%}")
print(f"visitor pairs: {len(V)}  offers {sum(v['off'] for _,v in V)}  taken {sum(v['tk'] for _,v in V)}  turned down {sum(v['td'] for _,v in V)}  missed {sum(v['ms'] for _,v in V)}")
print(f"visitor pairs with 3+ offers: {sum(1 for _,v in V if v['off']>=3)}, all at 0% taken: {all(v['tk']==0 for _,v in V)}")
# ---- 2. post-4.2 first offers by pair type
def ftype(c):
    r=c['chain'][0][0]; a=c['area']
    if home(r,a): return 'home responder first'
    return 'visitor first (0% pre-4.2 take rate here)'
def summarize(S,lab):
    g=defaultdict(list)
    for c in S: g[ftype(c)].append(c)
    print(f'\n{lab}: {len(S)} callouts')
    for k,L in g.items():
        un=sum(1 for c in L if not any(o=='y' for _,o in c['chain']))
        fo=Counter(c['chain'][0][1] for c in L)
        ms=sum(1 for c in L for _,o in c['chain'] if o=='m')
        print(f'  {k:42s} {len(L):4d} ({len(L)/len(S):.0%})  first offer taken {fo["y"]/len(L):.0%} / turned down {fo["n"]/len(L):.0%} / missed {fo["m"]/len(L):.0%}  | unanswered {un} ({un/len(L):.1%})  missed pings {ms}')
    return g
g0=summarize(pre,'PRE-4.2'); g1=summarize(post,'POST-4.2 (12 Aug - 6 Sep)')
# ---- 3. decomposition of unanswered + missed increase
def rate(L): return sum(1 for c in L if not any(o=='y' for _,o in c['chain']))/len(L)
kH,kV='home responder first','visitor first (0% pre-4.2 take rate here)'
s0=len(g0[kV])/len(pre); s1=len(g1[kV])/len(post)
uH0,uV0,uH1,uV1=rate(g0[kH]),rate(g0[kV]),rate(g1[kH]),rate(g1[kV])
tot0=s0*uV0+(1-s0)*uH0; tot1=s1*uV1+(1-s1)*uH1
mix=(s1-s0)*(uV0-uH0)
print(f'\nUNANSWERED: {tot0:.1%} -> {tot1:.1%} (+{100*(tot1-tot0):.1f} pts)')
print(f'  more visitor-first callouts (mix, at pre-4.2 rates): {100*mix:+.1f} pts')
print(f'  worse outcomes when visitor first:   {100*s1*(uV1-uV0):+.1f} pts')
print(f'  worse outcomes when home first:      {100*(1-s1)*(uH1-uH0):+.1f} pts')
un_post=[c for c in post if not any(o=='y' for _,o in c['chain'])]
print(f'  of {len(un_post)} unanswered post-4.2 callouts: visitor first in {sum(1 for c in un_post if ftype(c)==kV)}; any away ping in chain {sum(1 for c in un_post if any(not home(r,c["area"]) for r,_ in c["chain"]))}')
mp=[(r,c['area']) for c in post for r,o in c['chain'] if o=='m']
mpre=[(r,c['area']) for c in pre for r,o in c['chain'] if o=='m']
print(f'MISSED PINGS: pre {len(mpre)} (away {sum(1 for r,a in mpre if not home(r,a))})  post {len(mp)} (away {sum(1 for r,a in mp if not home(r,a))}, home {sum(1 for r,a in mp if home(r,a))})')
awaypost=[(r,o) for c in post for r,o in c['chain'] if not home(r,c['area'])]
print(f'away pings post: {len(awaypost)} taken {sum(1 for _,o in awaypost if o=="y")} td {sum(1 for _,o in awaypost if o=="n")} ms {sum(1 for _,o in awaypost if o=="m")}')
# ---- 4. pushed down: reliable home responders not first at home
print('\nRELIABLE HOME RESPONDERS: pre-4.2 home take rate, and share of their own-area callouts where they were first (pre -> post)')
for r in NAMES:
    d=P[(r,HOME[r])]
    A0=[c for c in pre if c['area']==HOME[r]]; A1=[c for c in post if c['area']==HOME[r]]
    f0=sum(1 for c in A0 if c['chain'][0][0]==r)/len(A0); f1=sum(1 for c in A1 if c['chain'][0][0]==r)/len(A1)
    vis1=sum(1 for c in A1 if not home(c['chain'][0][0],c['area']))/len(A1)
    print(f'  {NAMES[r]:18s} {AREAS[HOME[r]]:13s} takes {d["tk"]}/{d["off"]} ({d["tk"]/d["off"]:.0%}) | first at home {f0:.0%} -> {f1:.0%} | visitor first in own area post {vis1:.0%}')
