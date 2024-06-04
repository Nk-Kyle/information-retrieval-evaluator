from base import BaseQueryReader

class CacmQueryReader(BaseQueryReader):
    def get_queries(self):
        queries = []
        with open(self.file_path, "r") as f:
            # Get whole sections delimited by ".I"
            sections = f.read().split(".I")[1:]

            for section in sections:
                # Get the query_id
                query_id = int(section.split()[0])
                lines = section.strip().split('\n')
                
                # Find the index of '.W'
                content_start_index = lines.index('.W') + 1
                
                # Join lines of content until the next section delimiter
                content_lines = []
                for line in lines[content_start_index:]:
                    if line.startswith('.I') or line.startswith('.A') or line.startswith('.N'):  # Check for the start of the next section
                        break
                    content_lines.append(line.strip())
                
                # Extract the content
                query = " ".join(content_lines)

                queries.append(
                    {
                        "query_id": query_id,
                        "query": query
                    }
                )

        return queries

if __name__ == "__main__":
    import os

    file_path = "data/cacm.qry"

    # Change dir if to run
    print("Current working directory:", os.getcwd())
    if os.getcwd().endswith("src"):
        file_path = "irsystem/cacm/" + file_path
    elif os.getcwd().endswith("irsystem"):
        file_path = "cacm/" + file_path
    print("Current working directory after alteration:", os.getcwd())

    reader = CacmQueryReader(file_path)
