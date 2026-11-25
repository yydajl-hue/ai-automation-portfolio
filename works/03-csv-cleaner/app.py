"""Local Streamlit interface for the CSV/XLSX cleaner."""
from io import BytesIO
import pandas as pd
import streamlit as st
from cleaner import read_table, merge_tables, clean_data

st.set_page_config(page_title='Data Cleaner · 数据清洗', layout='wide')
st.title('Excel / CSV Data Cleaner · 数据清洗工具')
st.caption('本地处理 · 无需 AI API · 不修改原始文件')


def safe_export(df):
    # Prevent spreadsheet formula execution in exported user-controlled text.
    def escape(v):
        if isinstance(v, str) and v.lstrip().startswith(('=', '+', '-', '@')):
            # Preserve ordinary negative numeric values.
            try:
                float(v)
                return v
            except ValueError:
                return "'" + v
        return v
    out = df.apply(lambda col: col.map(escape))
    out.columns = [escape(str(c)) for c in df.columns]
    return out


files = st.file_uploader('上传多个 CSV / XLSX 文件', type=['csv', 'xlsx'], accept_multiple_files=True)
st.caption('Excel 仅读取第一个工作表；不同列名按列合并，缺少的列保留为空。')
if not files:
    st.info('请上传文件开始。可使用 sample-data 中的三个测试文件。')
    st.stop()
try:
    tables = [read_table(f, f.name) for f in files]
    raw = merge_tables(tables)
except Exception as exc:
    st.error(f'读取失败：{exc}')
    st.stop()
st.dataframe(pd.DataFrame({'文件': [f.name for f in files], '记录数': [len(t) for t in tables]}), hide_index=True)
with st.sidebar:
    st.header('清洗选项')
    trim = st.checkbox('清除文本首尾空格', True)
    drop_empty = st.checkbox('删除完全空白行', True)
    mode = st.radio('去重方式', ['指定字段去重', '全行去重', '不去重'])
    subset = None
    if mode == '指定字段去重':
        subset = st.multiselect('去重字段（保留第一条）', list(raw.columns), default=['order_id'] if 'order_id' in raw.columns else [])
    fill = st.checkbox('填充缺失值', False)
    fill_value = st.text_input('填充值', 'Unknown') if fill else None
    st.caption('缺失去重字段的记录会保留；空白单元格按缺失值处理。')
if mode == '指定字段去重' and not subset:
    st.warning('请选择至少一个去重字段，或切换去重方式。')
    st.stop()
try:
    cleaned, stats = clean_data(raw, trim=trim, drop_empty=drop_empty, deduplicate=mode != '不去重', subset=subset, fill_value=fill_value)
except Exception as exc:
    st.error(f'清洗失败：{exc}')
    st.stop()
a,b,c,d = st.columns(4)
a.metric('原始记录', stats['input_rows'])
b.metric('清洗后记录', stats['output_rows'])
c.metric('移除重复', stats['duplicate_rows_removed'])
d.metric('移除空白行', stats['empty_rows_removed'])
left,right = st.columns(2)
with left:
    st.subheader('清洗前')
    st.dataframe(raw, hide_index=True)
with right:
    st.subheader('清洗后')
    st.dataframe(cleaned, hide_index=True)
st.subheader('清洗统计报告')
labels = {'input_rows':'原始记录','output_rows':'清洗后记录','empty_rows_removed':'移除空白行','duplicate_rows_removed':'移除重复行','missing_cells_before':'处理前缺失单元格','missing_cells_after':'处理后缺失单元格'}
report = pd.DataFrame([{'metric': k, '指标': labels[k], 'value': v} for k,v in stats.items()])
st.dataframe(report, hide_index=True)
st.caption('缺失单元格数量变化包含删行和填充的影响。请检查去重结果后再用于业务。')
export = safe_export(cleaned)
col1,col2,col3 = st.columns(3)
col1.download_button('下载清洗后 CSV', export.to_csv(index=False).encode('utf-8-sig'), 'cleaned.csv', 'text/csv')
try:
    buf = BytesIO()
    with pd.ExcelWriter(buf, engine='openpyxl') as writer:
        export.to_excel(writer, sheet_name='Cleaned', index=False)
        report.to_excel(writer, sheet_name='Report', index=False)
    col2.download_button('下载 Excel（含报告）', buf.getvalue(), 'cleaned.xlsx', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
except Exception as exc:
    col2.warning(f'Excel 导出失败：{exc}')
col3.download_button('下载统计 CSV', report.to_csv(index=False).encode('utf-8-sig'), 'report.csv', 'text/csv')
st.caption('导出时对疑似公式的文本添加保护前缀；普通负数保留。CSV 中的编号请在 Excel 导入时指定为文本。')
