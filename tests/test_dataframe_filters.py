import pandas as pd
from dataframe_filters import (
    filter_by_flag_and_label,
    filter_by_project_name_version,
    filter_by_project_name_version_and_scanner,
    filter_rows_with_string_in_column,
)


def test_filter_by_project_name_version():
    df = pd.DataFrame({
        'project_name_version': ['Project A v1', 'Project B v1', 'Project A v2'],
        'data': [1, 2, 3]
    })

    filtered_df = filter_by_project_name_version(df, 'Project A v1')
    assert len(filtered_df) == 1
    assert filtered_df['data'].values[0] == 1

def test_filter_by_project_name_version_and_scanner():
    df = pd.DataFrame({
        'project_name_version': ['Project A v1', 'Project B v1', 'Project A v2'],
        'scanner_name': ['Scanner 1', 'Scanner 2', 'Scanner 1'],
        'data': [1, 2, 3]
    })

    filtered_df = filter_by_project_name_version_and_scanner(df, 'Project A v1', 'Scanner 1')
    assert len(filtered_df) == 1
    assert filtered_df['data'].values[0] == 1

def test_filter_by_flag_and_label():
    df = pd.DataFrame({
        'flag': [1, 2, 1],
        'label': [0, 1, 0],
        'data': [1, 2, 3]
    })

    filtered_df = filter_by_flag_and_label(df, 1, 0)
    assert len(filtered_df) == 1
    assert filtered_df['data'].values[0] == 1

def test_filter_rows_with_string_in_column():
    df = pd.DataFrame({
        'column1': ['abc', 'def', 'ghi'],
        'column2': ['jkl', 'mno', 'pqr'],
        'data': [1, 2, 3]
    })

    filtered_df = filter_rows_with_string_in_column(df, 'column1', 'd')
    assert len(filtered_df) == 1
    assert filtered_df['data'].values[0] == 2