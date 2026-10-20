"""Every review-table cell vs Air-Way's raw extract (07_RAW_EXTRACTS/<root>.csv, header row), by column name."""
import csv,os,re,collections,sys,glob,openpyxl
S=sys.argv[1]
def norm(pn):
    pn=pn.upper().replace(' UNPL','').strip()
    t=[str(int(x)) if x.isdigit() else x for x in pn.split('-')]
    return '-'.join(x for x in t if x!='O')
def num(x):
    try: return float(str(x).strip())
    except: return None
raw={}
for f in glob.glob('07_RAW_EXTRACTS/*.csv'):
    L=open(f,encoding='utf-8',errors='replace').read().splitlines()
    if not L or not L[0].startswith('Part'): continue
    sep='|' if '|' in L[0] else ','
    hdr=[h.strip() for h in L[0].split(sep)]
    rows={norm(l.split(sep)[0]):[c.strip() for c in l.split(sep)] for l in L[1:] if l.strip()}
    raw[os.path.basename(f)[:-4]]=(hdr,rows)
# 6400 has no header: Part|B1|B2|L5|C4|D(1)|D(2)
L=open('07_RAW_EXTRACTS/6400.csv').read().splitlines()
raw['6400']=(['Part','B1','B2','D1','HEXB','D3','D4'],{norm(l.split('|')[0]):l.split('|') for l in L if l.strip()})
ALIAS={'C1HEX':['C1'],'HEXB':['C4','HEXB'],'D1':['D1','D_1']}
out=[];stat=collections.Counter()
for f in sorted(glob.glob('04_DESIGN_TABLES/DesignTable_*.xlsx')):
    if f.endswith('_SW2.xlsx'): continue
    root=os.path.basename(f)[12:-5]
    sw2=f[:-5]+'_SW2.xlsx'; built=set()
    if os.path.exists(sw2):
        for r in openpyxl.load_workbook(sw2,read_only=True).worksheets[0].iter_rows(values_only=True):
            if r and r[0]: built.add(str(r[0]))
    rk=root if root in raw else (root.rstrip('L') if root.rstrip('L') in raw else None)
    if rk is None: continue
    hdr,rows=raw[rk]
    ws=openpyxl.load_workbook(f,read_only=True).worksheets[0]; th=None
    for r in ws.iter_rows(values_only=True):
        if th is None:
            if r and '$PRP@PartNo' in r: th=list(r)
            continue
        if not r or not r[0]: continue
        d=dict(zip(th,r)); pn=str(r[0])
        if d.get('$PRP@ScopeAction')!='BUILD': continue
        aw=rows.get(norm(pn))
        if aw is None:
            # 2501L etc: Air-Way has "2501-L-..." keys
            aw=rows.get(norm(pn).replace(root+'-',rk+'-',1))
        if aw is None: stat['row_not_in_aw']+=1; continue
        for col in th:
            if not col or '@' not in col or col.startswith('$'): continue
            base=col.split('@')[0]
            cands=[base]+ALIAS.get(base,[])
            idx=next((hdr.index(c) for c in cands if c in hdr),None)
            if idx is None or idx>=len(aw): continue
            a=num(aw[idx]); v=num(d.get(col))
            if a is None or v is None: continue
            stat['cells']+=1
            if abs(a-v)<=0.005: continue      # equal or rounding-only (2-decimal print)
            txt=(str(d.get('$PRP@AxialSource') or '')+' || '+str(d.get('$COMMENT') or ''))
            segs=[s for s in re.split(r'[;|]',txt) if base in s]
            why=' ; '.join(s.strip() for s in segs)[:400]
            k=('OMi' if re.search(r'OMi|A19|A20',why) else 'Brennan' if re.search(r'Brennan|BRENNAN|measured|MEASURED',why) else 'misprint' if re.search(r'misprint|wrong|suspect|AS-PRINTED|impossib',why,re.I) else 'rule' if re.search(r'rule|raised',why) else 'unexplained')
            out.append(dict(root=root,cfg=pn,col=col,current=v,airway=a,delta=round(v-a,4),built=pn in built,status=d.get('$PRP@DataStatus'),dimsrc=d.get('$PRP@DimSource'),kind=k,why=why))
            stat[k]+=1
print(stat)
w=csv.DictWriter(open(f'{S}/aw_audit.csv','w',newline=''),fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
c=collections.Counter((o['kind'],o['built']) for o in out); print(c)
for k in ('Brennan','misprint','rule','unexplained'):
    print('==',k)
    for o in [o for o in out if o['kind']==k][:12]: print(' ',o['cfg'],o['col'],o['current'],'AW',o['airway'],'|',o['why'][:160])
