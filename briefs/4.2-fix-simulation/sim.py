import random, statistics as st, datetime as dt
from load import *
random.seed(7)
C=load()
W0,W1=dt.datetime(2026,8,10),dt.datetime(2026,9,7)   # 4-week metric window = 11.2%
END=dt.datetime(2026,9,7)
pre=[c for c in C if c['t']<REL]; post=[c for c in C if c['t']>=REL]
def rates(S, who=None):
    o=[x for c in S for r,x in c['chain'] if who is None or r in who]
    n=len(o); return {k:o.count(k)/n for k in 'ynm'}, n
P_all,_=rates(pre); Q_all,_=rates(post)
STAY=P_all['m']/Q_all['m']            # share of post-4.2 misses that stay misses at 90s
take_share={r:(lambda d:d['y']/(d['y']+d['n']))(rates(pre,{r})[0]) for r in NAMES}
F_pre,_=rates(pre,set(FOUR)); F_post,_=rates(post,set(FOUR))
print('stay-miss prob at 90s %.3f'%STAY, 'four pre',{k:round(v,3) for k,v in F_pre.items()},'four post',{k:round(v,3) for k,v in F_post.items()})

# ---------- scoring ----------
def step(s,o,miss_cost):
    d={'y':0.08,'n':-0.12,'m':-miss_cost}[o]; return max(0,min(1,s+d))
def decay(s,days,hl):
    return s if not hl else 0.5+(s-0.5)*0.5**(days/hl)
def replay(calls, miss_cost=0.12, hl=None):
    s={r:0.5 for r in NAMES}; last={r:calls[0]['t'] for r in NAMES}; low={r:1 for r in NAMES}; at11={}
    for c in calls:
        if c['t']>=REL and not at11: at11=dict(s)
        for r,o in c['chain']:
            s[r]=decay(s[r],(c['t']-last[r]).total_seconds()/86400,hl); last[r]=c['t']
            s[r]=step(s[r],o,miss_cost)
            if c['t']>=REL: low[r]=min(low[r],s[r])
    for r in NAMES: s[r]=decay(s[r],(END-last[r]).total_seconds()/86400,hl)
    return at11,low,s
def convert(calls, stay):
    out=[]
    for c in calls:
        if c['t']<REL: out.append(c); continue
        ch=[]
        for r,o in c['chain']:
            if o=='m' and random.random()>stay:
                o='y' if random.random()<take_share[r] else 'n'
            ch.append((r,o))
            if o=='y': break
        out.append(dict(c,chain=ch))
    return out
def metric(calls, areas=None):
    Wc=[c for c in calls if W0<=c['t']<W1 and (areas is None or c['area'] in areas)]
    return 100*sum(1 for c in Wc if not any(o=='y' for _,o in c['chain']))/len(Wc)
def postmetric(calls, areas=None, inv=False):
    Wc=[c for c in calls if c['t']>=REL and (areas is None or ((c['area'] in areas)!=inv))]
    return 100*sum(1 for c in Wc if not any(o=='y' for _,o in c['chain']))/len(Wc)

HOMEA={HOME[r] for r in FOUR}
print('\n== DIRECT REPLAY (observed pings held fixed) ==')
print('baseline metric %.1f  post-only %.1f  four-home post %.1f  other post %.1f'%(metric(C),postmetric(C),postmetric(C,HOMEA),postmetric(C,HOMEA,True)))
print('pre-4.2: four-home %.1f other %.1f'%(
  100*sum(1 for c in pre if c['area'] in HOMEA and not any(o=='y' for _,o in c['chain']))/sum(1 for c in pre if c['area'] in HOMEA),
  100*sum(1 for c in pre if c['area'] not in HOMEA and not any(o=='y' for _,o in c['chain']))/sum(1 for c in pre if c['area'] not in HOMEA)))

def show(label, runs):
    # runs: list of (low,end) dicts
    line=label.ljust(34)
    for r in FOUR:
        lows=[x[0][r] for x in runs]; ends=[x[1][r] for x in runs]
        line+=' %s low %.2f end %.2f |'%(NAMES[r][:7].ljust(7),st.median(lows),st.median(ends))
    others=[r for r in NAMES if r not in FOUR]
    nb=st.median([sum(1 for r in others if x[0][r]<0.4) for x in runs])
    print(line,' others<0.4:',nb)

for lab,mc,hl in [('current rule',0.12,None),('misses cost 0',0,None),('misses cost half',0.06,None),('ease back hl14',0.12,14),('ease back hl7',0.12,7),('miss0 + ease14',0,14)]:
    a,l,e=replay(C,mc,hl); show(lab,[(l,e)])
N=400
for stay,lab in [(STAY,'90s'),((1+STAY)/2,'90s half-effect')]:
    for rl,mc,hl in [('',0.12,None),(' + miss0',0,None),(' + misshalf',0.06,None),(' + ease14',0.12,14)]:
        runs=[];ms=[];pm=[];hm=[];om=[]
        for i in range(N):
            cc=convert(C,stay); a,l,e=replay(cc,mc,hl); runs.append((l,e))
            if rl=='': ms.append(metric(cc)); pm.append(postmetric(cc)); hm.append(postmetric(cc,HOMEA)); om.append(postmetric(cc,HOMEA,True))
        show(lab+rl,runs)
        if ms: print('   metric 4wk %.1f (10-90%%: %.1f-%.1f)  post-only %.1f  four-home %.1f other %.1f'%(st.median(ms),sorted(ms)[N//10],sorted(ms)[9*N//10],st.median(pm),st.median(hm),st.median(om)))
