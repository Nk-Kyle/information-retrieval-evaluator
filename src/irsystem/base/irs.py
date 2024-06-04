# mac requirements:
# import sys
# import os

# script_dir = os.path.dirname(os.path.abspath(__file__))
# parent_dir = os.path.dirname(script_dir)
# sys.path.append(parent_dir)

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

    def eval(self, doc_weighting: WeightingTriplet, query_weighting: WeightingTriplet, rank_limit: int = 15):
        """
        Evaluates the system MAP for each query in the test collection using
        specified term weighting methods.

        Args:
            `doc_weighting`: term weighting method for documents
            `query_weighting` term weighting method for queries
        """

        # calculate tf-idf-normalized of documents
        term_weight = Converter.convert(
            self.doc_reader.tf_table,
            self.doc_reader.wc_table,
            doc_weighting.tf,
            doc_weighting.idf,
            doc_weighting.norm
        )
        term_weight = Converter.invert(term_weight)
        # term_weight is in df of format: term | doc_id | weight

        term_idfs = self.doc_reader.get_term_idfs()
        queries = self.query_reader.to_query_list()

        # calculate tfs of queries
        for query in queries:
            query.term_freqs = Converter.calc_term_frequency(
                query.tokens, query_weighting.tf
            )
            query.term_weights = query.term_freqs

        # calculate idfs of queries
        if query_weighting.idf == IDFMode.T:
            for query in queries:
                query.term_weights = dict(
                    (term, tf * term_idfs.get(term, 0))
                    for (term, tf)
                    in query.term_weights.items()
                )

        # normalize the query idfs
        if query_weighting.norm == NormMode.C:
            for query in queries:
                query.term_weights = Converter.normalize(
                    query.term_weights)
            # term_weights is in dict of format: term | weight

        # here we already have inverted files of queries and documents
        # we can now calculate the similarity for each query

        # first, create a nested dictionary from the term_weight DataFrame for fast lookups
        term_weight_dict = {}
        for idx, row in term_weight.iterrows():
            term = row['term']
            doc_id = row['doc_id']
            tfidf = row['tfidf']
            if term not in term_weight_dict:
                term_weight_dict[term] = {}
            term_weight_dict[term][doc_id] = tfidf

        # iterate through queries
        for query in queries:
            # initialize similarities dictionary
            query.similarities = {doc['doc_id']
                : 0 for doc in self.doc_reader.docs}

            # iterate through all terms in the query
            for term, weight in query.term_weights.items():
                if term in term_weight_dict:
                    # iterate through documents that have the term
                    for doc_id, tfidf in term_weight_dict[term].items():
                        if doc_id in query.similarities:
                            # calculate the similarity
                            query.similarities[doc_id] += weight * tfidf
        
        # sort by similarities
        for query in queries:
            query.similarities = dict(sorted(query.similarities.items(), key=lambda item: item[1], reverse=True))
        
        # calculate the MAP for each query
        sum = 0
        for query in queries:
            relevance_docs = self.relevance_reader.convert_to_dict()[query.id]
            retrieved_docs = list(query.similarities.keys())[:rank_limit]
            retrieved_relevance = 0
            map = 0
            for docs_id in retrieved_docs:
                if (docs_id in relevance_docs):
                    retrieved_relevance += 1
                    map += retrieved_relevance / (retrieved_docs.index(docs_id) + 1)
            map /= len(relevance_docs)
            sum += map
        average_map = sum/len(queries)
        return average_map

if __name__ == '__main__':
    from adi.reader import AdiDocReader
    from adi.query import AdiQueryReader
    from adi.relevance import AdiRelevanceReader
    import os
    import itertools
    import csv

    doc_path = "adi/data/adi.all"
    query_path = "adi/data/adi.qry"
    rel_path = "adi/data/adi.rel"

    print("Current working directory:", os.getcwd())
    if os.getcwd().endswith("src"):
        doc_path = "irsystem/" + doc_path
        query_path = "irsystem/" + query_path
        rel_path = "irsystem/" + rel_path

    # mac requirements:
    # base_path = os.path.dirname(os.path.abspath(__file__))
    # doc_path = os.path.join(base_path, "..", "adi", "data", "adi.all")
    # query_path = os.path.join(base_path, "..", "adi", "data", "adi.qry")
    # rel_path = os.path.join(base_path, "..", "adi", "data", "adi.rel")
    # doc_path = os.path.normpath(doc_path)
    # query_path = os.path.normpath(query_path)
    # rel_path = os.path.normpath(rel_path)

    # all combinations
    stem = False
    
    tfs = ['n', 'l', 'a', 'b']
    idfs = ['n', 't']
    norms = ['n', 'c']

    combinations = itertools.product(tfs, idfs, norms)
    combinations = [''.join(combo) for combo in combinations]

    irs = IRS(
        AdiDocReader(doc_path, stem=stem),
        AdiQueryReader(query_path, stem=stem),
        AdiRelevanceReader(rel_path)
    )

    with open('../adi/adi_nostem.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['doc.query', 'map'])
        
        count = 0
        for doc_combination in combinations:
            for query_combination in combinations:
                doc_weighting = WeightingTriplet.from_str(doc_combination)
                query_weighting = WeightingTriplet.from_str(query_combination)
                map_score = irs.eval(doc_weighting, query_weighting)
                writer.writerow([f"{doc_combination}.{query_combination}", map_score])
                count += 1
                print(f"{count}/256")

    print("CSV file created succesfully.")

