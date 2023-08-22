import os

import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib_venn import venn2, venn3
from sklearn import metrics


def _create_plot_data(set_values):

    # grab input sets
    A = set_values['A']
    B = set_values['B']
    C = set_values['C']
    D = set_values['D']
    E = set_values['E']

    # Define the intersection sizes
    A_not_B = A - B
    B_not_C = B - C
    C_not_D = C - D
    D_not_E = D - E

    B_not_A = B - A
    C_not_B = C - B
    D_not_C = D - C
    E_not_D = E - D
    
    A_and_B = A & B
    B_and_C = B & C
    C_and_D = C & D
    D_and_E = D & E
    A & D 
    B & D

    A_not_B_union_D = A - (B | D)
    B_not_A_union_D = B - (A | D)
    A_and_B_minus_D = (A & B) - D
    D_not_A_union_B = D - (A | B)
    A_and_D_minus_B = (A & D) - B
    B_and_D_minus_A = (B & D) - A
    A_and_B_and_D = (A & B) & D 
    
    # Define the sizes of the datasets
    len(A)
    len(B)
    len(C)
    len(D)
    len(E)
    
    size_A_not_B = len(A_not_B)
    size_B_not_C = len(B_not_C)
    size_C_not_D = len(C_not_D)
    size_D_not_E = len(D_not_E)

    size_B_not_A = len(B_not_A)
    size_C_not_B = len(C_not_B)
    size_D_not_C = len(D_not_C)
    size_E_not_D = len(E_not_D)

    size_A_and_B = len(A_and_B)
    size_B_and_C = len(B_and_C)
    size_C_and_D = len(C_and_D)
    size_D_and_E = len(D_and_E)

    set_A_not_B_union_D = len(A_not_B_union_D)
    set_B_not_A_union_D = len(B_not_A_union_D)
    set_A_and_B_minus_D = len(A_and_B_minus_D)
    set_D_not_A_union_B = len(D_not_A_union_B)
    set_A_and_D_minus_B = len(A_and_D_minus_B)
    set_B_and_D_minus_A = len(B_and_D_minus_A)
    set_A_and_B_and_D = len(A_and_B_and_D)

    return {
        'AB':  (size_A_not_B, size_B_not_A, size_A_and_B),
        'BC':  (size_B_not_C, size_C_not_B, size_B_and_C),
        'CD':  (size_C_not_D, size_D_not_C, size_C_and_D),
        'DE':  (size_D_not_E, size_E_not_D, size_D_and_E),
        'ABD': (set_A_not_B_union_D, set_B_not_A_union_D, set_A_and_B_minus_D,
                set_D_not_A_union_B, set_A_and_D_minus_B, set_B_and_D_minus_A,
                set_A_and_B_and_D), 
    } 

def _visualize_set_similarities(plot_title, project_name, set_names, 
                                set_values, set_legends, output_file=None):

    # Create the figure and subplots
    fig, axs = plt.subplots(3, 2, figsize=(10, 12))

    # Set a title for the entire subplot grid
    fig.suptitle(plot_title, fontsize=12)

    # Adjust the spacing between the title and subplots
    plt.subplots_adjust(top=0.9)

    # Evaluate the values for the venn2 and venn3 plots and return them in a dictionary
    dic_values = _create_plot_data(set_values)  

    # Create Venn diagrams and add to subplots

    # venn 2 diagrams
    venn_AB = venn2(subsets=dic_values['AB'], set_labels=set_names['AB'], ax=axs[1, 0], 
                    alpha=0.5)
    venn_BC = venn2(subsets=dic_values['BC'], set_labels=set_names['BC'], ax=axs[1, 1], 
                    alpha=0.5)
    venn_CD = venn2(subsets=dic_values['CD'], set_labels=set_names['CD'], ax=axs[2, 0], 
                    alpha=0.5)
    venn_DE = venn2(subsets=dic_values['DE'], set_labels=set_names['DE'], ax=axs[2, 1], 
                    alpha=0.5)

    # Customize colors if desired
    patch_10 = venn_AB.get_patch_by_id('10')
    if patch_10 is not None:
        patch_10.set_color('blue')

    patch_01 = venn_AB.get_patch_by_id('01')
    if patch_01 is not None:
        patch_01.set_color('orange')
    
    patch_10 = venn_BC.get_patch_by_id('10')
    if patch_10 is not None:
        patch_10.set_color('orange')

    patch_01 = venn_BC.get_patch_by_id('01')
    if patch_01 is not None:
        patch_01.set_color('green')
        patch_01.set_hatch('////') 

    patch_10 = venn_CD.get_patch_by_id('10')
    if patch_10 is not None:
        patch_10.set_color('green')

    patch_01 = venn_CD.get_patch_by_id('01')
    if patch_01 is not None:
        patch_01.set_color('purple')

    patch_10 = venn_DE.get_patch_by_id('10')
    if patch_10 is not None:
        patch_10.set_color('purple')

    patch_01 = venn_DE.get_patch_by_id('01')
    if patch_01 is not None:
        patch_01.set_color('gray')
        patch_01.set_hatch('////') 

    # venn 3 diagram
    venn_ABD = venn3(subsets=dic_values['ABD'], set_labels=set_names['ABD'], 
                     ax=axs[0, 0], alpha=0.5) 
    
    # Customize colors if desired
    patch_100 = venn_ABD.get_patch_by_id('100')
    if patch_100 is not None:
        patch_100.set_color('blue')

    patch_010 = venn_ABD.get_patch_by_id('010')
    if patch_010 is not None:
        patch_010.set_color('orange')

    patch_001 = venn_ABD.get_patch_by_id('001')
    if patch_001 is not None:
        patch_001.set_color('purple')
    
    # Set titles for subplots
    axs[0, 0].set_title('A vs. B vs. D')
    axs[1, 0].set_title('A vs. B')
    axs[1, 1].set_title('B vs. C')
    axs[2, 0].set_title('C vs. D')
    axs[2, 1].set_title('D vs. E')

    # Create the legend in subplot 0,1
    legend_elements = [
        Patch(facecolor='blue', edgecolor='white', label=set_legends['A']),
        Patch(facecolor='orange', edgecolor='white', label=set_legends['B']),
        Patch(facecolor='green', edgecolor='white', linewidth=1, hatch='////', 
              label=set_legends['C']),
        Patch(facecolor='purple', edgecolor='white', label=set_legends['D']),
        Patch(facecolor='gray', edgecolor='white', linewidth=1, hatch='////', 
              label=set_legends['E']),
    ]
    axs[0, 1].legend(handles=legend_elements, loc='upper right', fontsize=12, 
                     frameon=False)

    # Hide the legend subplot axes
    axs[0, 1].axis('off')

    # Adjust layout
    plt.tight_layout()

    if output_file:
        # Check if output folder exists
        output_folder = f"../output/{project_name}"
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
    
        # Save the plot to a file
        plt.savefig(os.path.join(output_folder, 
                                 output_file), dpi=300, bbox_inches='tight')
      

    # Show the plots
    plt.show()

def create_SBOM_similarity_plot(project_name, target_fields, scanner_data, 
                                output_file=None):
    # create plot title
    plot_title = (
        f"SBOM similarity plot for project {project_name} "
        f"with target field(s): {target_fields}"
    )
    
    # currently only one target field is implemented
    target_field = target_fields

    # define abbreviations for scanners
    scanner_labels = {
        'A': 'A',     # Gitlab
        'B': 'B',     # JA: JFrog Advanced Security
        'C': 'C',     # JX: Jfrog Xray
        'D': 'D',     # S: Syft
        'E': 'E'      # T: Trivy
    }

    # set scanner names (abbreviations)
    set_names = {
        'AB': (scanner_labels['A'], scanner_labels['B']),
        'BC': (scanner_labels['B'], scanner_labels['C']),
        'CD': (scanner_labels['C'], scanner_labels['D']),
        'DE': (scanner_labels['D'], scanner_labels['E']),
        'ABD':(scanner_labels['A'], scanner_labels['B'], scanner_labels['D'])
    }

    set_values = {
        'A': set(scanner_data['gitlab_cont'][target_field]),
        'B': set(scanner_data['jfrog_advanced_security_cont'][target_field]),
        'C': set(scanner_data['jfrog_cont'][target_field]),
        'D': set(scanner_data['syft_cont'][target_field]),
        'E': set(scanner_data['trivy_cont'][target_field])
    }

    set_legends = {
        'A': 'A: Gitlab',
        'B': 'B: JFrog Advanced Security',
        'C': 'C: JFrog Xray',
        'D': 'D: Syft',
        'E': 'E: Trivy'
    }

    _visualize_set_similarities(plot_title, project_name, set_names, set_values, set_legends, 
                               output_file)
    
def create_SBOM_confusion_matrix(project_name, scanner_names, scanner_data_df, output_file=None):

    plot_title = f"Confusion matrix for project {project_name}"

    # Create the figure and subplots
    fig, axes = plt.subplots(3, 2, figsize=(10, 12))

    # Set a title for the entire subplot grid
    fig.suptitle(plot_title, fontsize=12)

    # Adjust the spacing between the title and subplots
    plt.subplots_adjust(top=0.9)

    fig_index = [(0, 0), (1, 0), (1, 1), (2,0), (2,1)]

    # Iterate over the scanners and populate each subplot
    for i, scanner in enumerate(scanner_names):
        # Get the actual and predicted values for the current scanner
        actual = scanner_data_df['labeling'].replace({'TP': 1, 'FP': 0}).to_numpy()
        predicted = (
            scanner_data_df[f"pred_{scanner}"]
            .replace({'P': 1, 'N': 0})
            .to_numpy())

        # Compute the confusion matrix
        confusion_matrix = metrics.confusion_matrix(actual, predicted)

        # Create a ConfusionMatrixDisplay object
        cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix=confusion_matrix, 
                                                    display_labels=[False, True])

        # Plot the confusion matrix on the current subplot
        cm_display.plot(ax=axes[fig_index[i]]) # type: ignore
        axes[fig_index[i]].set_title(scanner)

        # Remove the grid from each subplot
        axes[fig_index[i]].grid(False)

    # Hide the subplot at position (0, 1)
    axes[0, 1].remove()

    # Adjust spacing between subplots
    plt.subplots_adjust(wspace=0.4, hspace=0.4)
    
    # Adjust the spacing between subplots
    plt.tight_layout()

    if output_file:
        # Check if output folder exists
        output_folder = f"../output/{project_name}"
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
    
        # Save the plot to a file
        plt.savefig(os.path.join(output_folder, 
                                 output_file), dpi=300, bbox_inches='tight')


    # Show the plot
    plt.show()