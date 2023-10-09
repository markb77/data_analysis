def label_sbom_data(scanner_data_df):

    # Reduce the number of columns
    col_names = ['name', 'version', 'name_proc1_version']
    scanner_data_df = scanner_data_df[col_names]

    # These 
    keys_to_extract = ['gitlab_cont', 'jfrog_advanced_security_cont', 'syft_cont']
    #
    labeling_data_frames = {key: project_scanner_data[key][target_field] for key in keys_to_extract}

    # create list with the 3 data frames that are the reference 
    labeling_data_frames_list = list(labeling_data_frames.values())

    # Apply the labeling function to scanner_data_df
    scanner_data_df['labeling'] = scanner_data_df.apply(lambda row: label_data(row, labeling_data_frames_list), axis=1)

    # Add predictions from all scanners (pred_<scanner_name>
    for col, df in zip(scanner_names, data_frames):
        scanner_data_df[f'pred_{col}'] = scanner_data_df.apply(lambda row: 'P' if (df[target_field] == row[target_field]).any() else 'N', axis=1)

    # label the predictions of the scanners
    return scanner_data_df.apply(eval_labels, axis=1, args=(scanner_names, ))


# Label the predictions A, B and C in label_A, label_B and label_C
def eval_labels(row, scanner_names):
    for col in scanner_names:
        if row[f'pred_{col}'] == 'P' and row['labeling'] == 'TP':
            row[f'label_{col}'] = 'TP'
        elif row[f'pred_{col}'] == 'P' and row['labeling'] == 'FP':
            row[f'label_{col}'] = 'FP'
        elif row[f'pred_{col}'] == 'N' and row['labeling'] == 'TP':
            row[f'label_{col}'] = 'FN'
        elif row[f'pred_{col}'] == 'N' and row['labeling'] == 'FP':
            row[f'label_{col}'] = 'TN'
    return row


# Helper function to label data
# if 2 of 3 data frames have the same value it is labeled as TP
def label_data(row, data_frames):
    count_sum = sum((df == row['name_proc1_version']).any() for df in data_frames)
    return 'TP' if count_sum >= 2 else 'FP'

