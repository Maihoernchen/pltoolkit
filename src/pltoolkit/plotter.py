from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt


class PltCollection:
    """
    Sammlung von Plot- und Exportfunktionen für ein Scaff-Objekt.
    """

    def __init__(self, scaff):
        self.scaff = scaff
        self.plots = []

    # ------------------------------------------------------------------

    def plot2d(
        self,
        xname,
        yname,
        title=None,
        xlabel=None,
        ylabel=None,
        legend=True,
    ):
        """
        Erstellt einen 2D-Plot aller geladenen Dateien.
        """

        fig, ax = plt.subplots()

        xcols = self.scaff.column(xname)
        ycols = self.scaff.column(yname)

        for filename in self.scaff.data:

            ax.plot(
                xcols[filename],
                ycols[filename],
                label=filename,
            )

        if title:
            ax.set_title(title)

        if xlabel:
            ax.set_xlabel(xlabel)

        if ylabel:
            ax.set_ylabel(ylabel)

        if legend:
            ax.legend()

        self.plots.append(fig)
        plt.show()

    # ------------------------------------------------------------------

    def saveplot(self, filename=None, index=0):
        """
        Speichert den Plot als SVG.
        """

        if not self.plots:
            raise ValueError("Es wurde noch kein Plot erzeugt.")

        if filename is None:

            source = Path(self.scaff.filenames[index])

            filename = source.with_name(
                source.stem + "_plot.svg"
            )

        self.plots[index].savefig(filename)

        print(f"Plot gespeichert: {filename}")

    # ------------------------------------------------------------------

    def savedatfiles(self):
        """
        Speichert jede Spalte jeder Datei separat.

        Beispiel:

            10.txt

        wird zu

            10_x.dat
            10_y.dat
            10_t.dat
        """

        if not self.scaff.columns:
            raise ValueError(
                "Keine Spalten vorhanden. "
                "Scaff(generate_columns=True) verwenden."
            )

        for filepath in self.scaff.filenames:

            filepath = Path(filepath)

            basename = filepath.stem
            outdir = filepath.parent
            filename = filepath.name

            for colname, columns in self.scaff.columns.items():

                data = columns[filename]

                outfile = outdir / f"{basename}_{colname}.dat"

                np.savetxt(
                    outfile,
                    data,
                    fmt="%.10g",
                    header=colname,
                    comments="",
                )

                print(f"Gespeichert: {outfile}")