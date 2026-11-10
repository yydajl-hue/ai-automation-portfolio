# 03 · Excel/CSV cleaner · Excel/CSV 清洗工具

**Maps to service package ⑤ (small tools and data scripts) · 对应服务包 ⑤**

## Problem · 问题
Merging several spreadsheets, removing duplicates and producing a report by hand takes hours every week and is easy to get wrong.
多张表格手工合并、去重、做报表，每周耗时数小时，还容易出错。

## What it does · 功能
Upload several Excel/CSV files → merge → de-duplicate → export a cleaned file and a summary report.
上传多个 Excel/CSV → 合并 → 去重 → 导出清洗后的文件和汇总报表。

## Stack · 技术
Python 3.11 · pandas · Streamlit

## Run it · 运行
```bash
python -m venv .venv
.venv\Scripts\activate
pip install pandas openpyxl streamlit
streamlit run app.py
```

## Test results · 测试结果
_Fill in after testing._

- 3 synthetic dirty datasets in `sample-data/` · 3 份自造脏数据
- Before/after screenshots for each in `docs/` · 每份的处理前后对比截图
- Rows in → rows out, duplicates removed: __ → __, __ · 行数变化与去重数

## Demo · 演示
_2–3 minute screen recording (no face): link TBD · 2–3 分钟录屏（不露脸）_

## Notes · 备注
All data is synthetic. · 所有数据均为自造。
