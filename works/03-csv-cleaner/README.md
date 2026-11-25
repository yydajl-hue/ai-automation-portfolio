# Excel / CSV Data Cleaner · Excel 数据清洗工具

A lightweight, local data processing tool for merging, cleaning and exporting multiple Excel and CSV files.

面向中小企业的本地数据处理工具，支持多表合并、数据去重、缺失值处理及报表导出。

## 1. Business Problems · 解决的业务问题

- Repetitive manual spreadsheet processing.
- Duplicate records across multiple files.
- Inconsistent formatting and missing values.
- Time-consuming monthly data consolidation.

- 重复性的人工表格处理工作。
- 多份业务文件中存在重复记录。
- 数据格式不统一、存在缺失值。
- 每月汇总业务数据耗时较长。

## 2. Features · 核心功能

- Multiple Excel and CSV file uploads.
- Automatic table merging.
- Full-row or selected-column deduplication.
- Empty row removal.
- Whitespace trimming and column name normalization.
- Optional missing value filling.
- Preservation of text identifiers and leading zeros.
- Before-and-after data previews.
- Cleaning statistics and Excel/CSV export.

- 支持批量上传 Excel 和 CSV 文件。
- 自动合并多份数据表。
- 支持全行去重和指定字段去重。
- 删除完全空白的记录。
- 清理文本及列名中的多余空格。
- 可选缺失值填充。
- 保留文本编号及前导零。
- 清洗前后数据对比。
- 自动生成统计报告，支持 Excel/CSV 导出。

## 3. Technology Stack · 技术栈

| Component / 组件 | Technology / 技术 |
|---|---|
| Programming language | Python |
| Data processing | pandas |
| Excel processing | openpyxl |
| Web interface | Streamlit |
| Processing environment | Local computer |

## 4. Workflow · 工作流程

Upload files → Merge tables → Configure cleaning rules → Clean data → Review results → Export files

上传文件 → 合并数据 → 配置清洗规则 → 执行清洗 → 查看结果 → 导出文件

## 5. Test Results · 测试结果

Test dataset: three synthetic sales order files.

测试数据：三份自造模拟销售订单文件。

| Metric / 指标 | Result / 结果 |
|---|---:|
| Input files / 输入文件 | 3 |
| Original records / 原始记录 | 15 |
| Empty rows removed / 删除空白行 | 3 |
| Duplicate rows removed / 删除重复行 | 3 |
| Cleaned records / 清洗后记录 | 9 |
| Missing cells before / 清洗前缺失单元格 | 14 |
| Missing cells after / 清洗后缺失单元格 | 1 |
| Automated tests / 自动化测试 | 11/11 passed |

All 11 automated tests passed in the development user's local environment. The results apply to the supplied test cases.

全部11项自动化测试已在本机开发环境中通过。测试成绩仅适用于当前测试用例。

Test evidence / 测试材料:

- `sample-data/`
- `docs/test-results.csv`
- `docs/before.csv`
- `docs/after.csv`

## 6. Getting Started · 快速开始

Install dependencies:

`python -m pip install -r requirements.txt`

Run automated tests:

`python eval.py`

Start the web application:

`python -m streamlit run app.py`

Open http://localhost:8501 in your browser and upload your files.

在浏览器中打开网页，上传文件、选择清洗规则并下载处理结果。

## 7. Use Cases · 适用场景

- E-commerce order consolidation / 电商订单汇总
- Sales reporting / 销售数据报表
- Customer list deduplication / 客户名单去重
- Inventory data cleaning / 库存数据清洗
- Monthly administrative reports / 行政月度报表

## 8. Data Privacy · 数据隐私

Data is processed locally without external AI APIs. Original input files are not modified.

数据在本地处理，无需调用外部大模型 API，不修改原始输入文件。

## 9. Limitations · 当前限制

- Supported file formats: CSV and XLSX.
- Only the first worksheet of each Excel file is imported.
- Cleaning rules must be selected according to actual business requirements.
- Conflicting records require business-specific handling.

- 支持 CSV 和 XLSX 文件。
- 当前仅读取每个 Excel 文件的第一个工作表。
- 清洗规则需要根据实际业务需求选择。
- 存在业务冲突的记录需要制定专门的处理规则。

## 10. Demo · 项目演示

Screen recording: Coming soon.

项目录屏演示：待上传。