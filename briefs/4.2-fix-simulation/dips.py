import datetime as dt
from load import *
C=load(); END=dt.datetime(2026,9,7)
pings={r:[] for r in NAMES}
for c in C:
    for r,o in c['chain']: pings[r].append((c['t'],o,HOME[r]==c['area']))
def wk(r,a,b): return 7*sum(1 for t,_,_ in pings[r] if a<=t<b)/max(1e-9,(b-a).total_seconds()/86400)
rows=[]
for r in NAMES:
    s=0.5; hist=[]; inside=False; P=pings[r]
    for i,(t,o,h) in enumerate(P):
        s_before=s; s=max(0,min(1,s+(0.08 if o=='y' else -0.12))); hist.append(o)
        last=hist[-10:]; rate=last.count('y')/len(last)
        if len(hist)>=10 and rate<0.6 and not inside:
            inside=True; st=dict(r=r,start=t,s0=s_before,minS=s,i0=i,miss=0,td=0,away=0,n=0)
        if inside:
            st['minS']=min(st['minS'],s); st['n']+=1; st['miss']+=o=='m'; st['td']+=o=='n'; st['away']+=not h
            if rate>=0.6:
                inside=False; st['end']=t; st['s_end']=s; rows.append(st)
    if inside: st['end']=None; st['s_end']=s; rows.append(st)
    final={r:s}
    pings[r+'_final']=s
print('Every stretch where the take rate over the last 10 pings fell below 60%:\n')
for st in rows:
    r=st['r']; a=st['start']
    before=wk(r,a-dt.timedelta(days=14),a); after_end=st['end'] or END
    during=wk(r,a,after_end) if (after_end-a).days>=1 else float('nan')
    # recovery: first date score >= 0.7 after the stretch start (or never)
    s=0.5; rec=None
    for t,o,h in pings[r]:
        s=max(0,min(1,s+(0.08 if o=='y' else -0.12)))
        if t>a and rec is None and s>=0.7 and st['minS']<0.7: rec=t
    print(f"{NAMES[r]:18s} {a:%d %b}-{(st['end'].strftime('%d %b') if st['end'] else 'still open')} | score {st['s0']:.2f} -> low {st['minS']:.2f} -> {st['s_end']:.2f} | "
          f"{st['n']} pings in stretch: {st['miss']} missed, {st['td']} turned down, {st['away']} out-of-area | pings/wk before {before:4.1f}, during {during:4.1f} | "
          f"{'post-4.2' if a>=REL else 'pre-4.2'} | back to 0.7: {rec.strftime('%d %b') if rec else ('n/a' if st['minS']>=0.7 else 'NEVER')}")
print('\nFinal scores 6 Sep:', {NAMES[r]:round(pings[r+'_final'],2) for r in NAMES})
