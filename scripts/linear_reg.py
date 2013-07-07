#! /usr/bin/python2
# -*- coding: utf-8 -*-
from create_table import *
from pylab import *
from sklearn import linear_model, gaussian_process
import matplotlib.pyplot as plt


def draw_plot(filename, data):

    l = plot([ d.get_costs_length() for d in data],[ 1 for i in data ], 'ro')
    ax = gca()
    ax.yaxis.set_visible(False)

    fig = gcf()
    fig.set_size_inches(10,2)

    setp(l, 'markersize', 10)
    setp(l, 'markerfacecolor', 'grey')

    plt.savefig(filename,dpi=100)

def regression(filename, data, name):

    x = [ d.get_length_vector() + [1] for d in data ]
    y = [ d.get_costs() for d in data ]
    names = [ d.description + " in " + d.place for d in data ]

    clf = linear_model.ARDRegression(compute_score=True)
    clf.fit(x,y)
    result = clf.coef_
    print result

    with open(filename, "w") as out:

        lines = [
            "\\newcommand{\\reg_%s_normal}{%0.2f}" % (name, result[1]),
            "\\newcommand{\\reg_%s_tunnel}{%0.2f}" % (name, result[0]),
            "\\begin{tabular}{llll}",
            "Strecke & \multicolumn{2}{c}{Kosten} & Fehler\\\\",
            "& geschätzt & tatsächlich & \\\\",
            "\\hline"
            ]

        for name,xv,yv in zip(names,x,y):

            pred = 0
            for xi, ci in zip(xv, result):
                pred += xi*ci

            lines.append("%s, %0.2f, %0.2f, %d %%\\\\" % (
                    name,
                    pred,
                    yv,
                    (pred - yv)*100/yv))


        lines.append("\\end{tabular}")
        out.write("\n".join(lines))





if __name__ == "__main__":
    data = readCsvFile(sys.argv[1])


    trams = list(filter(lambda x: x.tram and x.length and (x.costs or x.estimated_costs), data))
    subs = list(filter(lambda x: x.subway and x.length and (x.costs or x.estimated_costs), data))

    regression("/dev/stdout", trams, "tram")
    draw_plot("fig1.svg", trams)

    regression("/dev/stdout", subs, "subway")
    draw_plot("fig2.svg", subs)


