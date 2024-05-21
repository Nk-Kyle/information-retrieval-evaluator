from base.choices import TFMode, IDFMode, NormMode
import pandas as pd


class Converter:
    @staticmethod
    def convert(
        tftable: pd.DataFrame,
        wc_dict: dict,
        tfmode: TFMode = TFMode.N,
        idfmode: IDFMode = IDFMode.N,
        normmode: NormMode = NormMode.N,
    ) -> pd.DataFrame:
        """
        Convert the document statistics using the specified modes.

        Args:
            tftable (pd.DataFrame): The term frequency table. Rows are documents and columns are terms.
            wc_dict (dict): A dictionary where the keys are document IDs and the values are the word counts.
            tfmode (TFMode): The term frequency mode.
            idfmode (IDFMode): The inverse document frequency mode.
            normmode (NormMode): The normalization mode.

        Returns:
            pd.DataFrame: The converted document statistics.
        """

        # Calculate the tf values
        if tfmode == TFMode.N:
            value_table = tftable.copy(deep=True)
        elif tfmode == TFMode.L:
            value_table = tftable.map(lambda x: 1 + x if x > 0 else 0)
        elif tfmode == TFMode.A:
            max_tf = tftable.max(axis=1)
            value_table = tftable.div(max_tf, axis=0).mul(0.5).add(0.5)
        elif tfmode == TFMode.B:
            value_table = tftable.map(lambda x: 1 if x > 0 else 0)

        # Calculate the idf values
        if idfmode == IDFMode.N:
            pass
        elif idfmode == IDFMode.T:
            value_table = value_table.mul(
                pd.Series(wc_dict).apply(lambda x: 1 / x), axis=1
            )

        # Calculate the normalization values
        if normmode == NormMode.N:
            pass
        elif normmode == NormMode.C:
            value_table = value_table.div(
                value_table.pow(2).sum(axis=1).pow(0.5), axis=0
            )

        return value_table


if __name__ == "__main__":
    from adi.reader import AdiDocReader

    import os

    file_path = "adi/data/adi.all"

    print("Current working directory:", os.getcwd())
    if os.getcwd().endswith("src"):
        file_path = "irsystem/" + file_path
    reader = AdiDocReader(file_path)
    converter = Converter()
    res = converter.convert(
        reader.tf_table, reader.wc_table, TFMode.A, IDFMode.T, NormMode.C
    )
    print(res)
