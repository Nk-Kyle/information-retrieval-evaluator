from base import BaseRelevanceReader


class CacmRelevanceReader(BaseRelevanceReader):
    def get_relevances(self):

        relevances = []
        with open(self.file_path, "r") as f:
            lines = f.readlines()
            last_query_id = None
            for line in lines:
                query_id, doc_id, _, _ = line.split()
                query_id, doc_id = int(query_id), int(doc_id)
                if query_id != last_query_id:
                    relevances.append(
                        {"query_id": query_id, "docs_id": [doc_id]})
                    last_query_id = query_id
                else:
                    relevances[-1]["docs_id"].append(doc_id)
        return relevances


if __name__ == "__main__":
    import os

    file_path = "data/cacm.rel"

    # Change dir if to run
    print("Current working directory:", os.getcwd())
    if os.getcwd().endswith("src"):
        file_path = "irsystem/cacm/" + file_path
    elif os.getcwd().endswith("irsystem"):
        file_path = "cacm/" + file_path
    print("Current working directory after alteration:", os.getcwd())

    reader = CacmRelevanceReader(file_path)
    # Debug breakpoint
    pass
