from base import BaseDocReader


class AdiDocReader(BaseDocReader):
    def get_docs(self):
        """
        Parse the file into a list of documents.

        Returns:
            list: A list of dictionaries, where each dictionary represents a document.

        i.e. Adi collection:
        .I 2
        .T
        a new efficient structure-matching procedure and its application
        to automatic retrieval systems .
        .A
        G. SALTON
        E. H. SUSSENGUTH, JR .
        .W
        a new automatic method is presented for
        the comparison of two-dimensional line patterns .  retrieval
        applications include the matching of chemical
        structures, the comparison of syntactically analyzed excerpts
        extracted from documents and search requests, and
        the matching of document identifications consisting of twodimensional
        graphs with query identifications .

        Becomes:
        [
            {
                'doc_id': 2,
                'title': 'a new efficient structure-matching procedure and its application to automatic retrieval systems',
                'content': 'a new automatic method is presented for the comparison of two-dimensional line patterns .  retrieval applications include the matching of chemical structures, the comparison of syntactically analyzed excerpts extracted from documents and search requests, and the matching of document identifications consisting of twodimensional graphs with query identifications .',
            }
        ]
        """

        docs = []
        with open(self.file_path, "r") as f:
            # Get whole sections delimited by ".I"
            sections = f.read().split(".I")[1:]

            for section in sections:
                # Get the doc_id
                doc_id = int(section.split()[0])

                # Get the title
                title = section.split(".T")[1].split(".A")[0].strip().replace("\n", " ")

                # Get the author
                if ".A" not in section:
                    author = "Unknown"
                else:
                    author = section.split(".A")[1].split(".W")[0].strip()

                # Get the content
                content = section.split(".W")[1].strip()

                docs.append(
                    {
                        "doc_id": doc_id,
                        "title": title,
                        "author": author,
                        "content": content,
                    }
                )

        return docs


if __name__ == "__main__":
    import os

    file_path = "data/adi.all"

    # Change dir if to run
    print("Current working directory:", os.getcwd())
    if os.getcwd().endswith("src"):
        file_path = "irsystem/adi/" + file_path
    elif os.getcwd().endswith("irsystem"):
        file_path = "adi/" + file_path
    print("Current working directory after alteration:", os.getcwd())

    reader = AdiDocReader(file_path)
