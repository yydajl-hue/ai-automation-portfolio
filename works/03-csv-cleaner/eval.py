"""Run from project directory: python eval.py"""
from pathlib import Path
import pandas as pd
from cleaner import read_table, merge_tables, clean_data

ROOT = Path(__file__).resolve().parent
files = [ROOT/'sample-data'/f for f in ('sales_october.csv','sales_november.xlsx','sales_december.csv')]
raw = merge_tables([read_table(f) for f in files])
clean, stats = clean_data(raw, subset=['order_id'])
checks = {
    'three files merged': len(raw) == 15,
    'blank rows removed': stats['empty_rows_removed'] == 3,
    'duplicate IDs removed': stats['duplicate_rows_removed'] == 3,
    'output rows': len(clean) == 9,
    'leading zero preserved': '001' in clean.order_id.tolist(),
    'text trimmed': clean.loc[clean.order_id == '001','product'].iloc[0] == 'Keyboard',
    'missing cell preserved': pd.isna(clean.loc[clean.order_id == '003','customer'].iloc[0]),
    'source unchanged': raw.iloc[0]['product'] == ' Keyboard ',
    'missing keys not deduplicated': len(clean_data(pd.DataFrame({'id':['',''], 'v':['a','b']}),subset=['id'])[0]) == 2,
    'optional fill': clean_data(raw,subset=['order_id'],fill_value='Unknown')[0].isna().sum().sum() == 0,
    'full row dedup': len(clean_data(pd.DataFrame({'v':['a',' a ']}))[0]) == 1,
}
for name, ok in checks.items():
    print(f"{'OK' if ok else 'FAIL'}  {name}")
print('\nStatistics:', stats)
out = ROOT/'docs'; out.mkdir(exist_ok=True)
pd.DataFrame([{'test':name,'passed':bool(ok)} for name,ok in checks.items()]).to_csv(out/'test-results.csv',index=False,encoding='utf-8-sig')
raw.to_csv(out/'before.csv',index=False,encoding='utf-8-sig')
clean.to_csv(out/'after.csv',index=False,encoding='utf-8-sig')
print(f'Score: {sum(checks.values())}/{len(checks)}')
raise SystemExit(0 if all(checks.values()) else 1)
