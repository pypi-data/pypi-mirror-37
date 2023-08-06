import matplotlib

matplotlib.use('Agg')

import matplotlib.pyplot as plt
import os
import pandas as pd
import seaborn as sns

from .stats import lc


def lorenz_curve(
    x,
    out_file,
    xlabel="Fraction of Samples",
    ylabel="Fraction of On Target Reads",
    title="Read Distribution",
):
    """Generate Lorenz curve plot of `x` to file `out_file`. Outfile is PDF.

    Args:
        x (list): list or array of positive numbers
        out_file (str): path of output file (PDF)
        xlabel (Optional[str]): x-label
        ylabel (Optional[str]): y-label
        title (Optional[str]): Plot title

    Returns:
        str: out_file
    """
    sns.set(style='ticks', palette='muted', color_codes=True)
    p, L, _ = lc(x)
    # Save this [x, y] to out_file.csv
    with open("%s.csv" % os.path.splitext(out_file)[0], 'w') as fh:
        print("FractionOfSamples", "Equal", "Actual", sep=",", file=fh)
        for x, y in zip(p, L):
            print(x, x, y, sep=",", file=fh)
    plt.plot(p, L, linewidth=3)
    plt.plot([0., max(L)], color='k', linewidth=3, linestyle='dashed')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.savefig(out_file, bbox_inches='tight', format='pdf')
    plt.close()


def read_joining_summary_plot(
    a,
    b,
    out_file,
    colors= ['r', 'b'],
    labels= ['Unjoined', 'Joined'],
    xlabel='Read count',
    ylabel='Density',
):
    sns.set(style='ticks', palette='muted', color_codes=True)
    xmax = max([a.max(), b.max()])
    pa = sns.distplot(
        a,
        hist=False,
        color=colors[0],
        kde_kws={"color": colors[0], "lw": 3, "label": labels[0]},
    )
    pa = sns.distplot(
        b,
        hist=False,
        color=colors[1],
        ax=pa,
        kde_kws={"color": colors[1], "lw": 3, "label": labels[1]},
    )
    pa.legend(frameon=True)
    pa.set(xlim=(0, xmax), xlabel=xlabel, ylabel=ylabel)
    # plt.setp(pa, yticks=[])
    plt.savefig(out_file, bbox_inches='tight', format='pdf')
    plt.close()


def heatmap_by_group(df, out_file, values, index, column, groupby):
    """Plot a heatmap of values per group of grouped pandas.DataFrame.

    Args:
        df (pandas.DataFrame): pd.DataFrame object
        out_file (str): out file path with .pdf extension
        values (str): column label of df which will represent the data being plotted
        index (str): column label of df which will represent the rows
        column (str): column label of df which will represent the columns
        groupby (str): column label of df by which to group
    """
    sns.set(style='darkgrid')
    grouped_df = df.groupby([groupby])
    fig, axes = plt.subplots(
        figsize=(6, 12), nrows=grouped_df.ngroups, sharex=True, sharey=True
    )
    col_labels = df[column].unique()
    row_labels = df[index].unique()
    for key, ax in zip(sorted(grouped_df.groups.keys()), axes.flatten()):
        tdf = pd.pivot_table(
            grouped_df.get_group(key), values=values, index=index, columns=column
        )
        # fix for partial plates
        for i in col_labels:
            if i not in tdf.columns:
                tdf[i] = pd.np.nan
        for i in row_labels:
            if i not in tdf.index:
                tdf = tdf.append(pd.Series(name=i))
        # make the plot
        p = sns.heatmap(tdf, ax=ax, cbar=True, linewidth=1, cmap="YlGnBu")
        p.set(ylabel="", xlabel="", title=key)
    plt.savefig(out_file, bbox_inches="tight", format="pdf")
    plt.close()
