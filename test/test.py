import dataimport as di
import 2dplot

scaff = di.Scaff(
    directory="~/Documents/unineu/pl2/data/10",
    includes=".txt",
    generate_columns=True,
)

plots = 2dplot.PltCollection(scaff)

plots.plot2d(
    xname="t",
    yname="y",
    title="Test Plot",
    xlabel="Zeit",
    ylabel="y",
)

plots.saveplot()
plots.savedatfiles()