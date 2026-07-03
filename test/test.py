from pltoolkit import dataimport as di
from pltoolkit import plotter as plotter

scaff = di.Scaff(
    directory="~/Documents/unineu/pl2/data/10",
    includes=".txt",
    generate_columns=True,
)

plots = plotter.PltCollection(scaff)

plots.plot2d(
    xname="t",
    yname="y",
    title="Test Plot",
    xlabel="Zeit",
    ylabel="y",
)

plots.saveplot()
plots.savedatfiles()