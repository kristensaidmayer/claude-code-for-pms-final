import datetime as dt, math
from load import *
C=load()
def is_home(r,a): return HOME[r]==a
s={r:0.5 for r in NAMES}; touched=set(); clean=[]; allpost=[]
pairs_pre={}; area_pre={}
for c in C:
    f=c['chain'][0][0]; homes=[r for r in NAMES if is_home(r,c['area'])]
    if c['t']<REL:
        area_pre[c['area']]=area_pre.get(c['area'],0)+1
        if f not in homes: pairs_pre[(f,c['area'])]=pairs_pre.get((f,c['area']),0)+1
    else:
        involved={r for r,_ in c['chain']}|set(homes)
        rec=dict(c=c,first=f,homes=homes,sc={r:s[r] for r in involved},clean=not (involved & touched))
        allpost.append(rec)
        for r,_ in c['chain']: touched.add(r)
    for r,o in c['chain']: s[r]=max(0,min(1,s[r]+(0.08 if o=='y' else -0.12)))
cl=[x for x in allpost if x['clean']]
vf=[x for x in cl if x['first'] not in x['homes']]
print(f'CLEAN post-4.2 callouts (no one involved had any post-4.2 ping yet, so scores = 11 Aug values): {len(cl)}; out-of-area first: {len(vf)}')
pre_rate=sum(pairs_pre.values())/sum(area_pre.values())
k,n=len(vf),len(cl); p=sum(math.comb(n,i)*pre_rate**i*(1-pre_rate)**(n-i) for i in range(k,n+1))
print(f'pre-4.2 out-of-area-first rate {pre_rate:.0%}; chance of >= {k}/{n} if nothing changed: {p:.4f}')
print('\nEach clean out-of-area-first case:')
for x in vf:
    c=x['c']; v=x['first']; h=max(x['homes'],key=lambda r:x['sc'][r])
    dH=x['sc'][v]-x['sc'][h]
    pr=pairs_pre.get((v,c['area']),0); ar=area_pre[c['area']]
    print(f"{c['t']:%d %b %H:%M} {AREAS[c['area']]:12s} first: {NAMES[v]:15s}(hist {x['sc'][v]:.2f}) home: {NAMES[h]:15s}(hist {x['sc'][h]:.2f})  "
          f"pre-4.2 this visitor went first here {pr}/{ar} ({pr/ar:.0%})  | flip needs visitor >= {max(0,45*dH):.1f} min closer, chain {''.join(r+o for r,o in c['chain'])}")
print('\nPre-4.2 out-of-area-first by hour of day vs post (all post callouts):')
def hr(h): return 'night 22-06' if h>=22 or h<6 else 'day 06-22'
for lab,S in [('pre',[c for c in C if c['t']<REL]),('post',[c for c in C if c['t']>=REL])]:
    for b in ['night 22-06','day 06-22']:
        T=[c for c in S if hr(c['t'].hour)==b]; v=[c for c in T if not is_home(c['chain'][0][0],c['area'])]
        print(f'  {lab:4s} {b}: {len(v)}/{len(T)} = {len(v)/len(T):.0%}')
print('\nTop recurring out-of-area-first pairs pre-4.2 (visitor -> area): count / area callouts')
for (v,a),k in sorted(pairs_pre.items(),key=lambda x:-x[1])[:12]:
    post=sum(1 for x in allpost if x['first']==v and x['c']['area']==a); pa=sum(1 for x in allpost if x['c']['area']==a)
    print(f'  {NAMES[v]:15s} -> {AREAS[a]:12s} pre {k:2d}/{area_pre[a]:3d} ({k/area_pre[a]:.0%})   post {post:2d}/{pa:2d} ({post/max(1,pa):.0%})')
new=[(x['first'],x['c']['area']) for x in allpost if x['first'] not in x['homes'] and (x['first'],x['c']['area']) not in pairs_pre]
print('\nPost-4.2 out-of-area-first offers from pairs that NEVER happened pre-4.2:',len(new),'of',sum(1 for x in allpost if x['first'] not in x['homes']))
from collections import Counter; print(' ',Counter(f'{NAMES[v]}->{AREAS[a]}' for v,a in new).most_common(8))
