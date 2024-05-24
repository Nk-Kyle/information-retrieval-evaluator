from base.relevance import BaseRelevanceReader
from base.reader import BaseDocReader
from base.query import BaseQueryReader
from base.choices import IDFMode, NormMode, WeightingTriplet
from base.converter import Converter


class IRS:
    """
    Stands for Information Retrieval System. This class acts as a wrapper
    around lower-level reader classes. This class is also responsible for
    evaluating the system performance on a given test collection.
    """

    doc_reader: BaseDocReader
    query_reader: BaseQueryReader
    relevance_reader: BaseRelevanceReader

    def __init__(
        self,
        doc_reader: BaseDocReader,
        query_reader: BaseQueryReader,
        relevance_reader: BaseRelevanceReader
    ):
        self.doc_reader = doc_reader
        self.query_reader = query_reader
        self.relevance_reader = relevance_reader

    def eval(self, doc_weighting: WeightingTriplet, query_weighting: WeightingTriplet):
        """
        Evaluates the system MAP for each query in the test collection using
        specified term weighting methods.

        Args:
            `doc_weighting`: term weighting method for documents
            `query_weighting` term weighting method for queries
        """

        term_weight = Converter.convert(
            self.doc_reader.tf_table,
            self.doc_reader.wc_table,
            doc_weighting.tf,
            doc_weighting.idf,
            doc_weighting.norm
        )
        term_weight = Converter.invert(term_weight)

        term_idfs = self.doc_reader.get_term_idfs()
        queries = self.query_reader.to_query_list()

        for query in queries:
            query.term_freqs = Converter.calc_term_frequency(
                query.tokens, query_weighting.tf
            )

        if query_weighting.idf == IDFMode.T:
            for query in queries:
                query.term_weights = dict(
                    (term, tf * term_idfs.get(term, 0))
                    for (term, tf)
                    in query.term_freqs.items()
                )

        if query_weighting.norm == NormMode.C:
            for query in queries:
                query.term_weights = Converter.normalize(
                    query.term_weights)

        # TODO: actually evaluate the MAP for each query


if __name__ == '__main__':
    from adi.reader import AdiDocReader
    from adi.query import AdiQueryReader
    import os

    doc_path = "adi/data/adi.all"
    query_path = "adi/data/adi.qry"

    print("Current working directory:", os.getcwd())
    if os.getcwd().endswith("src"):
        doc_path = "irsystem/" + doc_path
        query_path = "irsystem/" + query_path

    irs = IRS(
        AdiDocReader(doc_path),
        AdiQueryReader(query_path),
        None
    )
    weighting = WeightingTriplet.from_str("atc")

    irs.eval(weighting, weighting)
