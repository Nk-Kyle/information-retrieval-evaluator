from base import BaseDocReader


class CranDocReader(BaseDocReader):
    def get_docs(self):
        """
        Parse the file into a list of documents.

        Returns:
            list: A list of dictionaries, where each dictionary represents a document.

        i.e. Cran collection:
        .I 2
        .T
        simple shear flow past a flat plate in an incompressible fluid of small
        viscosity .
        .A
        ting-yili
        .B
        department of aeronautical engineering, rensselaer polytechnic
        institute
        troy, n.y.
        .W
        simple shear flow past a flat plate in an incompressible fluid of small
        viscosity .
        in the study of high-speed viscous flow past a two-dimensional body it
        is usually necessary to consider a curved shock wave emitting from the
        nose or leading edge of the body .  consequently, there exists an
        inviscid rotational flow region between the shock wave and the boundary
        layer .  such a situation arises, for instance, in the study of the
        hypersonic viscous flow past a flat plate .  the situation is somewhat
        different from prandtl's classical boundary-layer problem . in prandtl's
        original problem the inviscid free stream outside the boundary layer is
        irrotational while in a hypersonic boundary-layer problem the inviscid
        free stream must be considered as rotational .  the possible effects of
        vorticity have been recently discussed by ferri and libby .  in the
        present paper, the simple shear flow past a flat plate in a fluid of small
        viscosity is investigated .  it can be shown that this problem can again
        be treated by the boundary-layer approximation, the only novel feature
        being that the free stream has a constant vorticity .  the discussion
        here is restricted to two-dimensional incompressible steady flow .

        Becomes:
        [
            {
                'doc_id': 2,
                'title': 'simple shear flow past a flat plate in an incompressible fluid of small viscosity .',
                'content': 'simple shear flow past a flat plate in an incompressible fluid of small viscosity .
                            in the study of high-speed viscous flow past a two-dimensional body it
                            is usually necessary to consider a curved shock wave emitting from the
                            nose or leading edge of the body .  consequently, there exists an
                            inviscid rotational flow region between the shock wave and the boundary
                            layer .  such a situation arises, for instance, in the study of the
                            hypersonic viscous flow past a flat plate .  the situation is somewhat
                            different from prandtl's classical boundary-layer problem . in prandtl's
                            original problem the inviscid free stream outside the boundary layer is
                            irrotational while in a hypersonic boundary-layer problem the inviscid
                            free stream must be considered as rotational .  the possible effects of
                            vorticity have been recently discussed by ferri and libby .  in the
                            present paper, the simple shear flow past a flat plate in a fluid of small
                            viscosity is investigated .  it can be shown that this problem can again
                            be treated by the boundary-layer approximation, the only novel feature
                            being that the free stream has a constant vorticity .  the discussion
                            here is restricted to two-dimensional incompressible steady flow .',
            }
        ]
        """

        docs = []
        with open(self.file_path, "r") as f:
            # Get whole sections delimited by ".I"
            sections = f.read().split(".I")[1:]

            for section in sections:
                # Get the doc_id
                doc_id = int(section.split()[0].strip())

                # Get the title
                title = section.split(".T")[1].split(".A")[0].strip().replace("\n", " ")

                # Get the author
                if ".A" not in section:
                    author = "Unknown"
                else:
                    author = section.split(".A")[1].split(".B")[0].strip()

                # Get the bibliography
                if ".B" in section:
                    bibliography = section.split(".B")[1].split(".W")[0].strip()
                else:
                    bibliography = "Unknown"

                # Get the content
                content = section.split(".W")[1].strip().replace("\n", " ")

                docs.append(
                    {
                        "doc_id": doc_id,
                        "title": title,
                        "author": author,
                        "bibliography": bibliography,
                        "content": content,
                    }
                )

        return docs


if __name__ == "__main__":
    import os

    file_path = "data/cran.all"

    # Change dir if to run
    print("Current working directory:", os.getcwd())
    if os.getcwd().endswith("src"):
        file_path = "irsystem/cran/" + file_path
    elif os.getcwd().endswith("irsystem"):
        file_path = "cran/" + file_path
    print("Current working directory after alteration:", os.getcwd())

    reader = CranDocReader(file_path)

    print(reader.docs[:2])
