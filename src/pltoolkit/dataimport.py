from pathlib import Path
import pandas as pd


class Scaff:
    """
    Klasse zum Einlesen mehrerer CSV- oder JSON-Dateien.

    Unterstützt:
    - absolute Pfade
    - relative Pfade
    - Einlesen kompletter Verzeichnisse
    - Filter nach Dateiendung oder Dateinamen
    """

    def __init__(
        self,
        filenames=None,
        directory=None,
        filetype=None,
        exclude_type=None,
        includes=None,
        excludes=None,
        skip=1,
        generate_columns=False,
    ):

        # Dictionary mit allen geladenen DataFrames
        self.data = {}

        # Speichert, ob Daten numerisch sind
        self.scale = {}

        # Gemeinsame Spalten
        self.columns = {}

        self.filenames = []

        # ----------------------------------------------------------
        # Dateiliste erzeugen
        # ----------------------------------------------------------

        if filenames:

            # Alle Pfade vereinheitlichen
            self.filenames = [Path(f).resolve() for f in filenames]

        elif directory:

            directory = Path(directory).resolve()

            if not directory.exists():
                raise FileNotFoundError(directory)

            self.filenames = [
                file
                for file in directory.iterdir()
                if file.is_file()
            ]

        else:
            raise ValueError(
                "Entweder 'filenames' oder 'directory' angeben."
            )

        # ----------------------------------------------------------
        # Filter anwenden
        # ----------------------------------------------------------

        if filetype:
            self.filenames = [
                f for f in self.filenames if f.suffix == filetype
            ]

        if exclude_type:
            self.filenames = [
                f for f in self.filenames if f.suffix != exclude_type
            ]

        if includes:
            self.filenames = [
                f for f in self.filenames if includes in f.name
            ]

        if excludes:
            self.filenames = [
                f for f in self.filenames if excludes not in f.name
            ]

        # ----------------------------------------------------------
        # Dateien laden
        # ----------------------------------------------------------

        for file in self.filenames:
            self.data[file.name] = self.load(file, skip)

        # ----------------------------------------------------------
        # Gemeinsame Spalten erzeugen
        # ----------------------------------------------------------

        if generate_columns and self.data:

            first = next(iter(self.data.values()))

            for column in first.columns:
                self.columns[column] = self.column(column)

    # ======================================================================

    def load(self, path: Path, skip=1):
        """
        Lädt eine CSV- oder JSON-Datei.
        """

        path = Path(path)

        # JSON
        if path.suffix.lower() == ".json":
            return pd.read_json(path, dtype=str)

        # CSV
        df = pd.read_csv(
            path,
            sep=";",
            skiprows=skip,
            dtype=str,
        )

        # Leere Spalten entfernen
        df = df.dropna(axis=1, how="all")

        # Versuch numerischer Konvertierung
        try:

            df = (
                df
                .apply(lambda c: c.str.replace(",", "."))
                .astype(float)
            )

            self.scale[path.name] = 2

        except ValueError:

            print(f"Warnung: '{path.name}' enthält Textdaten.")

            self.scale[path.name] = 1

        return df

    # ======================================================================

    def column(self, name):
        """
        Gibt eine Spalte aller geladenen Dateien zurück.

        Rückgabe:
            {
                "Datei1.csv": ndarray,
                "Datei2.csv": ndarray
            }
        """

        result = {}

        for filename, df in self.data.items():

            if name not in df.columns:
                continue

            column = df[name]

            if self.scale.get(filename, 0) >= 2:
                column = column.to_numpy(dtype=float)

            result[filename] = column

        return result