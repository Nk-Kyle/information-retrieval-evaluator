from base import BaseQueryReader

class NplQueryReader(BaseQueryReader):
    def get_queries(self):
        queries = []
        with open(self.file_path, "r") as f:
            lines = f.readlines()

            query_id = None
            query = []

            index = 0
            while True:
                line = lines[index]
                query_id = int(line)

                while True:
                    index += 1
                    line = lines[index].strip()

                    if line.strip() == "/":
                        break

                    query.append(line)

                query = " ".join(query).strip()
                queries.append(
                    {
                        "query_id": query_id,
                        "query": query
                    }
                )

                query_id = None
                query = []

                index += 1
                if index >= len(lines):
                    break

        return queries

if __name__ == "__main__":
    import os

    file_path = "data/npl.qry"

    # Change dir if to run
    print("Current working directory:", os.getcwd())
    if os.getcwd().endswith("src"):
        file_path = "irsystem/npl/" + file_path
    elif os.getcwd().endswith("irsystem"):
        file_path = "npl/" + file_path
    print("Current working directory after alteration:", os.getcwd())

    reader = NplQueryReader(file_path)
    # print(reader.queries)
