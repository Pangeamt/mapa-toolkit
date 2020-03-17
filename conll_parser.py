import time
from prettytable import PrettyTable


class ConllParser():

    @staticmethod
    def _parse_token(token: str, sentence, token_index: int):
        token = token.rstrip().split(" ")
        sentence[0].append(token[0])
        tags = token[1:]
        for i, tag in enumerate(tags):
            try:
                sentence[i + 1].append(tag)
            except IndexError:
                sentence.append(["O"] * token_index)
                sentence[i + 1].append(tag)
        if len(token) < len(sentence):
            for i in range(len(token), len(sentence)):
                sentence[i].append("O")

    @staticmethod
    def parse(text: str):
        doc = []
        sentence = [[]]
        i = 0
        for token in text:
            if token == "\n":
                if not sentence == [[]]:
                    doc.append(sentence)
                    sentence = [[]]
                    i = 0
            elif token[0:2] == "- ":
                yield doc
                doc = []
                i = 0
            else:
                ConllParser._parse_token(token, sentence, i)
                i += 1
        yield doc

    @staticmethod
    def parse_file(path: str):
        with open(path, "r") as file:
            for doc in ConllParser.parse(file):
                # Uncomment for debug
                # for sentence in doc:
                #     table = PrettyTable()
                #     table.add_column("Tokens", sentence[0])
                #     for i in range(1, len(sentence)):
                #         table.add_column(f"Tag {i}", sentence[i])
                #     print(table)
                #     time.sleep(10)
                yield doc
