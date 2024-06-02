from typing import Dict, List
from base.choices import TFMode, IDFMode, NormMode
import math
import pandas as pd
import warnings
# Suppress FutureWarning messages
warnings.simplefilter(action='ignore', category=FutureWarning)


class Converter:
    @staticmethod
    def convert(
        tftable: pd.DataFrame,
        wc_table: dict,
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
            value_table = tftable.map(
                lambda x: 1 + math.log(x) if x > 0 else 0)
        elif tfmode == TFMode.A:
            # axis = 1 -> by row
            max_tf = tftable.max(axis=1)
            value_table = tftable.div(max_tf, axis=0).mul(0.5).add(0.5)
        elif tfmode == TFMode.B:
            value_table = tftable.map(lambda x: 1 if x > 0 else 0)

        # Calculate the idf values
        if idfmode == IDFMode.N:
            pass
        elif idfmode == IDFMode.T:
            idf_table = pd.Series(
                {term: math.log(len(tftable) / wc)
                 for term, wc in wc_table.items()}
            )
            # axis = 0?
            value_table = value_table.mul(idf_table, axis=1)

        # Calculate the normalization values
        if normmode == NormMode.N:
            pass
        elif normmode == NormMode.C:
            value_table = value_table.div(
                value_table.pow(2).sum(axis=1).pow(0.5), axis=0
            )

        return value_table

    @staticmethod
    def invert(value_table: pd.DataFrame) -> pd.DataFrame:
        """
        Invert the document statistics.

        Args:
            value_table (pd.DataFrame): The document statistics to invert.

        Returns:
            pd.DataFrame: The inverted document statistics, as inverted file.
        """

        # for each term, get the list of documents that contain it
        # each row is a term, column 1 is the document id, column 2 is the tf-idf value
        # term can be repeated in the first column, i.e. multiple rows with the same term but different document id, index on term
        inverted_file = pd.DataFrame(columns=["term", "doc_id", "tfidf"])
        for term in value_table.columns:
            # get the documents that contain the term
            docs = value_table[value_table[term] > 0][term]
            # create a dataframe with the term and the document id and tfidf value
            term_df = pd.DataFrame(
                {"term": term, "doc_id": docs.index, "tfidf": docs.values})
            # concatenate the dataframe to the inverted file
            inverted_file = pd.concat([inverted_file, term_df])

        return inverted_file

    @staticmethod
    def calc_term_frequency(
        terms: List[str],
        mode: TFMode
    ) -> Dict[str, float]:
        """
        Calculates term frequency value for a sequence of terms
        using specified valuation method.

        Args:
            `terms`: a list of terms of which term frequency is 
                     to be calculated
            `mode`: term frequency valuation method

        Returns:
            A dictionary mapping each term to its frequency value.
        """

        raw_tfs: Dict[str, float] = {}

        for term in terms:
            if term not in raw_tfs:
                raw_tfs[term] = 0
            raw_tfs[term] += 1

        match mode:
            case TFMode.N:
                return raw_tfs
            case TFMode.L:
                return dict(
                    (term, 1 + math.log(tf))
                    for (term, tf)
                    in raw_tfs.items()
                )
            case TFMode.A:
                max_freq = max(raw_tfs.values())
                return dict(
                    (term, .5 + .5 * tf / max_freq)
                    for (term, tf)
                    in raw_tfs.items()
                )
            case TFMode.B:
                return dict(
                    (term, 1)
                    for (term, _)
                    in raw_tfs.items()
                )

    @staticmethod
    def normalize(term_weights: Dict[str, float]) -> Dict[str, float]:
        """
        Normalizes term weights vector by its length. 

        Args:
            `term_weights`: term weights vector to be normalized

        Returns:
            Normalized term weights vector.
        """
        magnitude = math.sqrt(sum(tf * tf for tf in term_weights.values()))
        return dict(
            (term, tf / magnitude)
            for (term, tf)
            in term_weights.items()
        )


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
        reader.tf_table, reader.wc_table, TFMode.N, IDFMode.T, NormMode.N
    )
    res = converter.invert(res)
