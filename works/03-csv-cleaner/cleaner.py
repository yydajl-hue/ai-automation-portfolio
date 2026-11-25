"""Local CSV/XLSX merge and cleaning; no network calls."""
from pathlib import Path
from io import BytesIO
import pandas as pd


def read_table(source, filename=None):
    name = filename or str(source)
    data = Path(source).read_bytes() if isinstance(source, (str, Path)) else source.getvalue()
    if name.lower().endswith('.csv'):
        for encoding in ('utf-8-sig', 'gb18030'):
            try:
                return pd.read_csv(BytesIO(data), encoding=encoding, dtype=str, keep_default_na=False, skip_blank_lines=False)
            except UnicodeDecodeError:
                continue
        raise ValueError(f'Unsupported CSV encoding: {name}')
    if name.lower().endswith('.xlsx'):
        return pd.read_excel(BytesIO(data), engine='openpyxl', dtype=str, keep_default_na=False)
    raise ValueError(f'Unsupported file: {name}')


def merge_tables(tables):
    normalized = []
    for table in tables:
        df = table.copy()
        df.columns = [str(c).strip() for c in df.columns]
        if df.columns.duplicated().any():
            raise ValueError('Duplicate column names after trimming')
        normalized.append(df)
    if not normalized:
        raise ValueError('Upload at least one table')
    return pd.concat(normalized, ignore_index=True, sort=False)


def clean_data(df, *, trim=True, drop_empty=True, deduplicate=True, subset=None, fill_value=None):
    result = df.copy()
    if trim:
        result = result.apply(lambda col: col.map(lambda x: x.strip() if isinstance(x, str) else x))
    result = result.replace(r'^\s*$', pd.NA, regex=True)
    before = len(result)
    missing_before = int(result.isna().sum().sum())
    if drop_empty:
        result = result.dropna(how='all')
    empty_removed = before - len(result)
    duplicates_removed = 0
    if deduplicate:
        if subset:
            if not set(subset).issubset(result.columns):
                raise ValueError('Unknown deduplication column')
            # Missing keys are not evidence that two records are duplicates.
            eligible = result[list(subset)].notna().all(axis=1)
            mask = eligible & result.duplicated(subset=list(subset), keep='first')
        else:
            mask = result.duplicated(keep='first')
        duplicates_removed = int(mask.sum())
        result = result.loc[~mask]
    if fill_value is not None:
        result = result.fillna(fill_value)
    stats = {'input_rows': before, 'output_rows': len(result), 'empty_rows_removed': empty_removed,
             'duplicate_rows_removed': duplicates_removed, 'missing_cells_before': missing_before,
             'missing_cells_after': int(result.isna().sum().sum())}
    return result.reset_index(drop=True), stats
