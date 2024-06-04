from base import BaseDocReader


class MedDocReader(BaseDocReader):
    def get_docs(self):
        docs = []
        with open(self.file_path, "r") as f:
            # Get whole sections delimited by ".I"
            sections = f.read().split(".I")[1:]

            for section in sections:
                # Get the doc_id
                doc_id = int(section.split()[0])

                # Get the content
                content = section.split(".W")[1].strip()

                lines = content.split("\n")

                processed_lines = []
                for line in lines:
                    # Strip leading/trailing whitespace and replace tabs with spaces
                    clean_line = line.strip().replace("\t", " ")

                    if clean_line:
                        processed_lines.append(clean_line)

                final_content = ' '.join(processed_lines)

                docs.append(
                    {
                        "doc_id": doc_id,
                        "content": final_content,
                    }
                )

        return docs


if __name__ == "__main__":
    import os

    file_path = "data/med.all"

    # Change dir if to run
    print("Current working directory:", os.getcwd())
    if os.getcwd().endswith("src"):
        file_path = "irsystem/med/" + file_path
    elif os.getcwd().endswith("irsystem"):
        file_path = "med/" + file_path
    print("Current working directory after alteration:", os.getcwd())

    reader = MedDocReader(file_path)