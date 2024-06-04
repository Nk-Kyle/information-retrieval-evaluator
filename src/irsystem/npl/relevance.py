from base import BaseRelevanceReader


class NplRelevanceReader(BaseRelevanceReader):
    def get_relevances(self):

        relevances = []
        with open(self.file_path, "r") as f:
            lines = f.readlines()

            index = 0
            while True:
                line = lines[index]
                query_id = int(line)

                relevant_ids = []

                while True:
                    index += 1
                    line = lines[index]

                    if line.strip() == "/":
                        break
                    relevant_ids.extend(int(id_) for id_ in line.split())

                relevances.append(
                    {"query_id": query_id, "docs_id": relevant_ids})

                index += 1
                if index >= len(lines):
                    break

        return relevances


if __name__ == "__main__":
    import os

    file_path = "data/npl.rel"

    # Change dir if to run
    print("Current working directory:", os.getcwd())
    if os.getcwd().endswith("src"):
        file_path = "irsystem/npl/" + file_path
    elif os.getcwd().endswith("irsystem"):
        file_path = "npl/" + file_path
    print("Current working directory after alteration:", os.getcwd())

    reader = NplRelevanceReader(file_path)
    # Debug breakpoint
    pass
