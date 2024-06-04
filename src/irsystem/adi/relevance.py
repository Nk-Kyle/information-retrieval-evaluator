# mac requirements:
# import sys
# import os

# script_dir = os.path.dirname(os.path.abspath(__file__))
# parent_dir = os.path.dirname(script_dir)
# sys.path.append(parent_dir)

from base import BaseRelevanceReader


class AdiRelevanceReader(BaseRelevanceReader):
    def get_relevances(self):
        """
        Parse the file into a list of relevance judgments.

        Returns:
            list: A list of dictionaries, where each dictionary represents a query's relevance judgment.
        
        i.e. ADI collection:
        1   17   0   0.000000   
        1   46   0   0.000000   
        1   62   0   0.000000   
        2   12   0   0.000000   
        2   71   0   0.000000  
        to
        [
            {
                "query_id": 1,
                "docs_id": [17, 46, 62],
            },
            {
                "query_id": 2,
                "docs_id": [12, 71],
            }
        ]

        """
        relevances = []
        with open(self.file_path, "r") as f:
            lines = f.readlines()
            last_query_id = None
            for line in lines:
                query_id, doc_id, _, _ = line.split()
                query_id, doc_id = int(query_id), int(doc_id)
                if query_id != last_query_id:
                    relevances.append({"query_id": query_id, "docs_id": [doc_id]})
                    last_query_id = query_id
                else:
                    relevances[-1]["docs_id"].append(doc_id)
        return relevances

    def convert_to_dict(self):
        """
        Convert list to dictionary for fast lookups.

        Returns:
            dict: A dictionary where the query_id is the key 
                  and the list of relevant documents is the value.
        """
        relevances_dict = {}
        for relevance in self.relevances:
            relevances_dict[relevance["query_id"]] = relevance["docs_id"]
        return relevances_dict
    
if __name__ == "__main__":
    import os

    file_path = "data/adi.rel"

    # Change dir if to run
    print("Current working directory:", os.getcwd())
    if os.getcwd().endswith("src"):
        file_path = "irsystem/adi/" + file_path
    elif os.getcwd().endswith("irsystem"):
        file_path = "adi/" + file_path
    print("Current working directory after alteration:", os.getcwd())

    reader = AdiRelevanceReader(file_path)