import re, datetime as dt
NAMES=dict(zip("ABCDEFGHIJKLMNOP",["Captain Vantage","Cindermark","Corporal Ashgrove","Farlight","Halfmoon","Ironvale","Meteor Mite","Nightwell","Sgt. Bulwark","Sgt. Falkirk","Stormwrack","The Drift","The Gale","The Longcast","The Undertow","Vesper"]))
AREAS=dict(zip("abcdefghijklmno",["Eastgate","Foundry Row","Greenway","Harborside","Hillcrest","Kingsbridge","Lakeshore","Midtown","Mill District","Northfield","Old Town","Riverside","Southport","Uptown","Westbury"]))
HOME=dict(A='e',B='i',C='j',D='n',E='o',F='l',G='a',H='h',I='b',J='f',K='m',L='c',M='a',N='g',O='d',P='k')
FOUR=['D','G','O','P']
REL=dt.datetime(2026,8,12)
def load():
    out=[]
    for tok in open('chains.txt').read().split():
        t=dt.datetime(2026,int(tok[0:2]),int(tok[2:4]),int(tok[4:6]),int(tok[6:8]))
        area=tok[8]; chain=[(tok[i],tok[i+1]) for i in range(9,len(tok),2)]
        out.append(dict(t=t,area=area,chain=chain))
    return out
