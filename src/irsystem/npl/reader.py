from base import BaseDocReader


class NplDocReader(BaseDocReader):
    def get_docs(self):
        docs = []
        with open(self.file_path, "r") as f:
            lines = f.readlines()

            doc_id = None
            content = []

            index = 0
            while True:
                line = lines[index]
                doc_id = int(line)

                while True:
                    index += 1
                    line = lines[index].strip()

                    if line.strip() == "/":
                        break

                    content.append(line)

                content = " ".join(content).strip()
                docs.append(
                    {
                        "doc_id": doc_id,
                        "content": content,
                    }
                )

                doc_id = None
                content = []

                index += 1
                if index >= len(lines):
                    break

        return docs


if __name__ == "__main__":
    import os

    file_path = "data/npl.all"

    # Change dir if to run
    print("Current working directory:", os.getcwd())
    if os.getcwd().endswith("src"):
        file_path = "irsystem/npl/" + file_path
    elif os.getcwd().endswith("irsystem"):
        file_path = "npl/" + file_path
    print("Current working directory after alteration:", os.getcwd())

    reader = NplDocReader(file_path)
