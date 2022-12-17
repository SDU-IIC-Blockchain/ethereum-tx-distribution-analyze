import matplotlib
import matplotlib.pyplot as plt
import csv
from matplotlib.ticker import PercentFormatter, ScalarFormatter
import seaborn as sns

SAVE_FIG_FORMAT = 'pgf'

if __name__ == '__main__':
    sns.set_style('whitegrid')
    # https://stackoverflow.com/a/39566040

    SMALL_SIZE = 18  # 8
    MEDIUM_SIZE = 24  # 10
    BIGGER_SIZE = 24  # 12

    plt.rc('font', size=13)  # controls default text sizes
    plt.rc('axes', titlesize=SMALL_SIZE)  # fontsize of the axes title
    plt.rc('axes', labelsize=MEDIUM_SIZE)  # fontsize of the x and y labels
    plt.rc('xtick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
    plt.rc('ytick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
    plt.rc('legend', fontsize=SMALL_SIZE)  # legend fontsize
    plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

    if SAVE_FIG_FORMAT == 'pgf':
        # https://matplotlib.org/stable/tutorials/text/pgf.html
        matplotlib.use('pgf')
        plt.rcParams.update({
            "text.usetex": True,
            "pgf.texsystem": "pdflatex",
            "pgf.preamble": "\n".join([
                r"\usepackage[utf8x]{inputenc}",
                r"\usepackage[T1]{fontenc}",
                r"\usepackage{cmbright}",
            ]),
            "pgf.rcfonts": False,
            "font.serif": [],  # use latex default
            "font.sans-serif": [],  # use latex default
            "font.monospace": [],  # use latex default
            "font.family": "serif",
        })
    else:
        plt.rcParams.update({
            "text.usetex": False,
            "font.family": 'Times New Roman',
        })

    # cmap = sns.cubehelix_palette()

    with open('distribute.csv', 'r') as f:
        reader = csv.reader(f)
        headers = next(reader)
        datas = [[] for _ in headers]

        for row in reader:
            for i, data in enumerate(row):
                datas[i].append(int(data))

        my_bins = {
            1: [200 * i for i in range(0, 8)],
            2: [4000000 * i for i in range(0, 9)],
        }

        my_colors = {
            1: "#2b6f39",
            2: "#d38fc5",
        }

        assert len(headers) - 1 == 2
        # assume the first column is x and other columns are y
        for i in range(1, len(headers)):
            # plt.plot(data[0], data[i], label=headers[i])
            plt.figure(figsize=(6, 5)).clear()
            # https://qa.ostack.cn/qa/?qa=239242/
            counts, bins, patches = plt.hist(
                datas[i],
                bins=my_bins[i],
                color=my_colors[i],
                # ec='black', lw=0.7,
                weights=[100 / len(datas[i])] * len(datas[i]),
            )
            ax = plt.gca()
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.yaxis.set_major_formatter(PercentFormatter(100))
            plt.bar_label(patches, fmt='%.2f%%')
            plt.xticks(bins)  # https://stackoverflow.com/a/66363887
            ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
            plt.xlabel(headers[i] + ' in a Block')
            plt.ylabel('Proportion')
            plt.savefig(f'hist_{i}.{SAVE_FIG_FORMAT}', bbox_inches='tight')

        # for i in range(1, len(headers)):
        #     plt.figure().clear()
        #     plt.plot(datas[0], datas[i], label=headers[i])
        #     plt.xlabel(headers[0])
        #     plt.ylabel(headers[i])
        #     plt.savefig(f'plot_{i}.pdf')
