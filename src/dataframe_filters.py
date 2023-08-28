import pandas as pd


def filter_by_project_name_version(df, project_name_version):
    """
    Filters the DataFrame based on the specified 'project_name_version'.

    Args:
        df (DataFrame): The input DataFrame.
        project_name_version (str): The project name and version to filter by.

    Returns:
        DataFrame: The filtered DataFrame.
    """
    if not isinstance(project_name_version, str):
        raise ValueError("'project_name_version' must be a string")
    
    return df[df['project_name_version'] == project_name_version]


def filter_by_project_name_version_and_scanner(df, project_name_version, scanner_name):
    """
    Filters the DataFrame based on the specified 'project_name_version' and 'scanner_name'.

    Args:
        df (DataFrame): The input DataFrame.
        project_name_version (str): The project name and version to filter by.
        scanner_name (str): The scanner name to filter by.

    Returns:
        DataFrame: The filtered DataFrame.
    """
    if not isinstance(project_name_version, str) or not isinstance(scanner_name, str):
        raise ValueError("'project_name_version' and 'scanner_name' must be strings")
    
    return df[((df['project_name_version'] == project_name_version) & 
               (df['scanner_name'] == scanner_name))]


def filter_by_flag_and_label(df, flag, label):
    """
    Filters the DataFrame based on the specified 'flag' and 'label'.

    Args:
        df (DataFrame): The input DataFrame.
        flag (int): The flag value to filter by.
        label (int): The label value to filter by.

    Returns:
        DataFrame: The filtered DataFrame.
    """
    if not isinstance(flag, int) or not isinstance(label, int):
        raise ValueError("'flag' and 'label' must be integer types")
    
    return df[(df['flag'] == flag) & (df['label'] == label)]


def filter_rows_with_string_in_column(df, column, string):
    """
    Filters the DataFrame based on the specified column containing the specified string.

    Args:
        df (DataFrame): The input DataFrame.
        column (str): The column to filter by.
        string (str): The string to search for in the specified column.

    Returns:
        DataFrame: The filtered DataFrame.

    Raises:
        ValueError: If the specified column does not exist in the DataFrame.
    """
    if not isinstance(column, str) or not isinstance(string, str):
        raise ValueError("'column' and 'string' must be strings")

    if column not in df.columns:
        raise ValueError(f"'{column}' is not a column of the DataFrame")
    
    return df[df[column].str.contains(string)]

def get_difference_between_scanners(df, project_name_version, 
                                    scanner_name1, scanner_name2, flag1, label1):
    """
    Filters the DataFrame based on the specified project name/version, scanner names, flag, and label.
    Returns the difference between the two resulting subsets.

    Args:
        df (DataFrame): The input DataFrame.
        project_name_version1 (str): The project name and version to filter by.
        scanner_name1 (str): The first scanner name to filter by.
        scanner_name2 (str): The second scanner name to filter by.
        flag1 (int): The flag value to filter by.
        label1 (int): The label value to filter by.

    Returns:
        DataFrame: The difference between the two resulting subsets.

    Raises:
        ValueError: If the input arguments are of the wrong type.
    """
    if not isinstance(project_name_version, str) or not isinstance(scanner_name1, str):
        raise ValueError("'project_name_version1' and 'scanner_name1' must be strings")
    if not isinstance(scanner_name2, str):
        raise ValueError("'scanner_name2' must be a string")
    if not isinstance(flag1, int) or not isinstance(label1, int):
        raise ValueError("'flag1' and 'label1' must be integers")

    df1_filtered = filter_by_project_name_version_and_scanner(df, project_name_version, scanner_name1)

    df1_FL = filter_by_flag_and_label(df1_filtered, flag1, label1)

    df2_filtered = filter_by_project_name_version_and_scanner(df, project_name_version, scanner_name2)

    df2_FL = filter_by_flag_and_label(df2_filtered, flag1, label1)

    data_set = set(df1_FL['name_version']) - set(df2_FL['name_version'])
    # Convert the set to a list of tuples
    data_list = [(value,) for value in data_set]

    return pd.DataFrame(data_list, columns=['artifacts'])