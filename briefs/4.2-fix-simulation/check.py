from load import *
C=load()
print(len(C), sum(len(c['chain']) for c in C))
pre=[c for c in C if c['t']<REL]; post=[c for c in C if c['t']>=REL]
for lab,S in (('pre',pre),('post',post)):
    pings=[o for c in S for _,o in c['chain']]
    un=sum(1 for c in S if not any(o=='y' for _,o in c['chain']))
    print(lab,len(S),'unanswered',un,round(100*un/len(S),1),'miss%',round(100*pings.count('m')/len(pings),1))
# 4-week windows
for end in [dt.datetime(2026,8,31),dt.datetime(2026,9,6)]:
    for start_off in (27,28):
        st=end-dt.timedelta(days=start_off)
        W=[c for c in C if st<=c['t']<end+dt.timedelta(days=1)]
        un=sum(1 for c in W if not any(o=='y' for _,o in c['chain']))
        print('window',st.date(),end.date(),len(W),un,round(100*un/len(W),1))
