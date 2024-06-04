from base import BaseQueryReader

class TimeQueryReader(BaseQueryReader):
    def get_queries(self):
        queries = []
        with open(self.file_path, "r") as f:
            # Get whole sections delimited by "*FIND"
            sections = f.read().split("*FIND")[1:]

            for section in sections:
                if '*STOP' in section:
                    section = section.split('*STOP')[0]

                if section.strip():  # Ensure the section is not empty
                    lines = section.strip().split('\n')
                    
                    query_id = int(lines[0].strip())
                    
                    query = " ".join(line.strip() for line in lines[1:] if line.strip())

                    queries.append(
                        {
                            "query_id": query_id,
                            "query": query
                        }
                )

        return queries

if __name__ == "__main__":
    import os

    file_path = "data/time.que"

    # Change dir if to run
    print("Current working directory:", os.getcwd())
    if os.getcwd().endswith("src"):
        file_path = "irsystem/time/" + file_path
    elif os.getcwd().endswith("irsystem"):
        file_path = "time/" + file_path
    print("Current working directory after alteration:", os.getcwd())

    reader = TimeQueryReader(file_path)
