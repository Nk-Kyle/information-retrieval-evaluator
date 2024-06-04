from base import BaseQueryReader

class CranQueryReader(BaseQueryReader):
    def get_queries(self):
        """
        Parse the file into a list of queries.

        Returns:
            list: A list of dictionaries, where each dictionary represents a query.

        i.e. Cran query:
        .I 004
        .W
        what problems of heat conduction in composite slabs have been solved so far .
        Becomes:
        [
            {
                'query_id': 4,
                'query': 'what problems of heat conduction in composite slabs have been solved so far .',
            }
        ]
        """

        queries = []
        with open(self.file_path, "r") as f:
            count = 1
            # Get whole sections delimited by ".I"
            sections = f.read().split(".I")[1:]

            for section in sections:
                # Get the query_id
                # NOTE: query_id uses count
                # query_id = int(section.split()[0])
                query_id = count
                count += 1

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

    file_path = "data/cran.qry"

    # Change dir if to run
    print("Current working directory:", os.getcwd())
    if os.getcwd().endswith("src"):
        file_path = "irsystem/cran/" + file_path
    elif os.getcwd().endswith("irsystem"):
        file_path = "cran/" + file_path
    print("Current working directory after alteration:", os.getcwd())

    reader = CranQueryReader(file_path)
    print(reader.queries)
