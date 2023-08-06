import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import seaborn as sns

from .stats import lc

# sns.set(context='paper', palette='deep', style='whitegrid')
sns.set(style='ticks', palette='muted', color_codes=True)


def lorenz_curve(x, outfile, xlabel="Fraction of Samples", ylabel="Fraction of On Target Reads", title="Read Distribution"):
    """Generate Lorenz curve plot as of `x` to file `outfile`. Outfile is PDF.

    Args:
        x (list): list or array of positive numbers
        outfile (str): path of output file (PDF)
        xlabel (Optional[str]): x-label
        ylabel (Optional[str]): y-label
        title (Optional[str]): Plot title

    Returns:
        str: outfile
    """
    p, L, _ = lc(x)
    plt.plot(p, L, linewidth=3)
    plt.plot([0., max(L)], color='k', linewidth=3, linestyle='dashed')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.savefig(outfile, bbox_inches='tight', format='pdf')
    plt.close()


def read_joining_summary_plot(a, b, outfile, colors=['r', 'b'],
                              labels=['Unjoined', 'Joined'],
                              xlabel='Read count', ylabel='Density'):
    xmax = max([a.max(), b.max()])
    pa = sns.distplot(a, hist=False, color=colors[0],
                 kde_kws={"color":colors[0], "lw":3, "label":labels[0]})
    pa = sns.distplot(b, hist=False, color=colors[1], ax=pa,
                 kde_kws={"color":colors[1], "lw":3, "label":labels[1]})

    pa.legend(frameon=True)
    pa.set(xlim=(0, xmax), xlabel=xlabel, ylabel=ylabel)
    # plt.setp(pa, yticks=[])
    plt.savefig(outfile, bbox_inches='tight', format='pdf')
    plt.close()
