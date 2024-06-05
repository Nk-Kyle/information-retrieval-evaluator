from base import BaseDocReader


class CacmDocReader(BaseDocReader):
    def get_docs(self):
        docs = []
        doc = {}
        key = None
        with open(self.file_path, "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith(".I"):
                    if doc:
                        docs.append(doc)
                    doc = {
                        "doc_id": int(line.split()[1]),
                        "title": "",
                        "author": "",
                        "bibliography": "",
                        "content": "",
                    }
                    key = None
                elif line.startswith(".T"):
                    key = "title"
                elif line.startswith(".A"):
                    key = "author"
                elif line.startswith(".B"):
                    key = "bibliography"
                elif line.startswith(".W"):
                    key = "content"
                elif line.startswith((".N", ".X", ".I")):
                    key = None
                elif key:
                    doc[key] += line + " "

            if doc:
                docs.append(doc)

        return docs


if __name__ == "__main__":
    import os

    file_path = "data/cacm.all"

    # Change dir if to run
    print("Current working directory:", os.getcwd())
    if os.getcwd().endswith("src"):
        file_path = "irsystem/cacm/" + file_path
    elif os.getcwd().endswith("irsystem"):
        file_path = "cacm/" + file_path
    print("Current working directory after alteration:", os.getcwd())

    reader = CacmDocReader(file_path)
