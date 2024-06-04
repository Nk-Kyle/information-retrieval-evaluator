from base import BaseQueryReader

class MedQueryReader(BaseQueryReader):
    def get_queries(self):
        queries = []
        with open(self.file_path, "r") as f:
            # Get whole sections delimited by ".I"
            sections = f.read().split(".I")[1:]

            for section in sections:
                # Get the query_id
                query_id = int(section.split()[0])

                # Get the query
                query = section.split(".W")[1].strip().replace("\n", " ")

                queries.append(
                    {
                        "query_id": query_id,
                        "query": query
                    }
                )

        return queries

if __name__ == "__main__":
    import os

    file_path = "data/med.qry"

    # Change dir if to run
    print("Current working directory:", os.getcwd())
    if os.getcwd().endswith("src"):
        file_path = "irsystem/med/" + file_path
    elif os.getcwd().endswith("irsystem"):
        file_path = "med/" + file_path
    print("Current working directory after alteration:", os.getcwd())

    reader = MedQueryReader(file_path)
    # print(reader.queries)
