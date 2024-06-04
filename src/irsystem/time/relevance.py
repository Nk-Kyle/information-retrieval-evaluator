from base import BaseRelevanceReader


class TimeRelevanceReader(BaseRelevanceReader):
    def get_relevances(self):

        relevances = []
        with open(self.file_path, "r") as f:
            lines = f.readlines()

            for line in lines:
                if line.strip() == "":
                    continue

                [query_id, *doc_ids] = [int(id_) for id_ in line.split()]
                relevances.append(
                    {"query_id": query_id, "docs_id": doc_ids})

        return relevances


if __name__ == "__main__":
    import os

    file_path = "data/time.rel"

    # Change dir if to run
    print("Current working directory:", os.getcwd())
    if os.getcwd().endswith("src"):
        file_path = "irsystem/time/" + file_path
    elif os.getcwd().endswith("irsystem"):
        file_path = "time/" + file_path
    print("Current working directory after alteration:", os.getcwd())

    reader = TimeRelevanceReader(file_path)
    # Debug breakpoint
    pass
