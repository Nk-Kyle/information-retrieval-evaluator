from base import BaseDocReader


class TimeDocReader(BaseDocReader):
    def get_docs(self):
        docs = []
        with open(self.file_path, "r") as f:
            # Get whole sections delimited by "*TEXT"
            sections = f.read().split("*TEXT")[1:]
            id = 1

            for section in sections:
                if '*STOP' in section:
                    section = section.split('*STOP')[0]

                if section.strip():  # Ensure the section is not empty
                    lines = section.strip().split('\n')
                    doc_id = id
                    
                    content = " ".join(line.strip() for line in lines[1:] if line.strip())

                    docs.append(
                        {
                            "doc_id": doc_id,
                            "content": content,
                        }
                    )

                    id += 1

        return docs


if __name__ == "__main__":
    import os

    file_path = "data/time.all"

    # Change dir if to run
    print("Current working directory:", os.getcwd())
    if os.getcwd().endswith("src"):
        file_path = "irsystem/time/" + file_path
    elif os.getcwd().endswith("irsystem"):
        file_path = "time/" + file_path
    print("Current working directory after alteration:", os.getcwd())

    reader = TimeDocReader(file_path)
