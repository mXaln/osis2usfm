import argparse
import xml.etree.ElementTree as Tree
import re
from argparse import Namespace
from pathlib import Path
from typing import Tuple, List

books = [
    {"sort": 1, "slug": "gen", "name": "Genesis"},
    {"sort": 2, "slug": "exo", "name": "Exodus"},
    {"sort": 3, "slug": "lev", "name": "Leviticus"},
    {"sort": 4, "slug": "num", "name": "Numbers"},
    {"sort": 5, "slug": "deu", "name": "Deuteronomy"},
    {"sort": 6, "slug": "jos", "name": "Joshua"},
    {"sort": 7, "slug": "jdg", "name": "Judges"},
    {"sort": 8, "slug": "rut", "name": "Ruth"},
    {"sort": 9, "slug": "1sa", "name": "1 Samuel"},
    {"sort": 10, "slug": "2sa", "name": "2 Samuel"},
    {"sort": 11, "slug": "1ki", "name": "1 Kings"},
    {"sort": 12, "slug": "2ki", "name": "2 Kings"},
    {"sort": 13, "slug": "1ch", "name": "1 Chronicles"},
    {"sort": 14, "slug": "2ch", "name": "2 Chronicles"},
    {"sort": 15, "slug": "ezr", "name": "Ezra"},
    {"sort": 16, "slug": "neh", "name": "Nehemiah"},
    {"sort": 17, "slug": "est", "name": "Esther"},
    {"sort": 18, "slug": "job", "name": "Job"},
    {"sort": 19, "slug": "psa", "name": "Psalms"},
    {"sort": 20, "slug": "pro", "name": "Proverbs"},
    {"sort": 21, "slug": "ecc", "name": "Ecclesiastes"},
    {"sort": 22, "slug": "sng", "name": "Song of Solomon"},
    {"sort": 23, "slug": "isa", "name": "Isaiah"},
    {"sort": 24, "slug": "jer", "name": "Jeremiah"},
    {"sort": 25, "slug": "lam", "name": "Lamentations"},
    {"sort": 26, "slug": "ezk", "name": "Ezekiel"},
    {"sort": 27, "slug": "dan", "name": "Daniel"},
    {"sort": 28, "slug": "hos", "name": "Hosea"},
    {"sort": 29, "slug": "jol", "name": "Joel"},
    {"sort": 30, "slug": "amo", "name": "Amos"},
    {"sort": 31, "slug": "oba", "name": "Obadiah"},
    {"sort": 32, "slug": "jon", "name": "Jonah"},
    {"sort": 33, "slug": "mic", "name": "Micah"},
    {"sort": 34, "slug": "nam", "name": "Nahum"},
    {"sort": 35, "slug": "hab", "name": "Habakkuk"},
    {"sort": 36, "slug": "zep", "name": "Zephaniah"},
    {"sort": 37, "slug": "hag", "name": "Haggai"},
    {"sort": 38, "slug": "zec", "name": "Zechariah"},
    {"sort": 39, "slug": "mal", "name": "Malachi"},
    {"sort": 41, "slug": "mat", "name": "Matthew"},
    {"sort": 42, "slug": "mrk", "name": "Mark"},
    {"sort": 43, "slug": "luk", "name": "Luke"},
    {"sort": 44, "slug": "jhn", "name": "John"},
    {"sort": 45, "slug": "act", "name": "Acts"},
    {"sort": 46, "slug": "rom", "name": "Romans"},
    {"sort": 47, "slug": "1co", "name": "1 Corinthians"},
    {"sort": 48, "slug": "2co", "name": "2 Corinthians"},
    {"sort": 49, "slug": "gal", "name": "Galatians"},
    {"sort": 50, "slug": "eph", "name": "Ephesians"},
    {"sort": 51, "slug": "php", "name": "Philippians"},
    {"sort": 52, "slug": "col", "name": "Colossians"},
    {"sort": 53, "slug": "1th", "name": "1 Thessalonians"},
    {"sort": 54, "slug": "2th", "name": "2 Thessalonians"},
    {"sort": 55, "slug": "1ti", "name": "1 Timothy"},
    {"sort": 56, "slug": "2ti", "name": "2 Timothy"},
    {"sort": 57, "slug": "tit", "name": "Titus"},
    {"sort": 58, "slug": "phm", "name": "Philemon"},
    {"sort": 59, "slug": "heb", "name": "Hebrews"},
    {"sort": 60, "slug": "jas", "name": "James"},
    {"sort": 61, "slug": "1pe", "name": "1 Peter"},
    {"sort": 62, "slug": "2pe", "name": "2 Peter"},
    {"sort": 63, "slug": "1jn", "name": "1 John"},
    {"sort": 64, "slug": "2jn", "name": "2 John"},
    {"sort": 65, "slug": "3jn", "name": "3 John"},
    {"sort": 66, "slug": "jud", "name": "Jude"},
    {"sort": 67, "slug": "rev", "name": "Revelation"},
]


class Converter:

    def __init__(self, input_dir: Path, output_dir: Path):
        self.input_dir = input_dir
        self.output_dir = output_dir

        self.book_slug = ""
        self.words = []
        self.word_parts = []
        self.subs = []

    def start(self):
        if self.input_dir is None:
            self.input_dir = Path(".")
        if self.output_dir is None:
            self.output_dir = Path(".")

        if not self.input_dir.is_dir():
            print("Input should be a directory")
            return
        if not self.output_dir.is_dir():
            print("Output should be a directory")
            return

        for file in self.input_dir.iterdir():
            self.process_xml(file)

    def process_xml(self, xml_file: Path):
        if xml_file.suffix != ".xml":
            return

        tree = Tree.parse(xml_file)
        root = tree.getroot()
        usfm = ""

        book = root.find("book")
        self.book_slug = book.attrib["osisID"]

        usfm += r"\id " + self.book_slug.upper() + "\n"
        usfm += r"\usfm " + "3.0\n"
        usfm += r"\ide " + "UTF-8\n"
        usfm += r"\h " + self.book_slug + "\n"
        usfm += r"\toc1 " + self.book_slug + "\n"
        usfm += r"\toc2 " + self.book_slug + "\n"
        usfm += r"\toc3 " + self.book_slug.capitalize() + "\n"
        usfm += r"\mt " + self.book_slug + "\n\n"

        for chapter in root.findall("book/chapter"):
            for verse in chapter.findall("verse"):
                self.words = []
                self.word_parts = []
                self.subs = []

                pre_text = verse.find("preText")
                pre_tags = self.split_tags(pre_text.text)

                verse_text = pre_tags

                self.map_words(verse.findall("*"))
                self.map_word_parts()

                for node in verse.findall("*"):
                    if node.tag == "w":
                        verse_text += self.process_word(node)
                    elif node.tag == "phrase":
                        verse_text += self.process_phrase(node)

                for sub in self.subs:
                    verse_text = re.sub(re.escape(sub[0]), sub[1], verse_text)

                usfm += verse_text

        usfm_file = Path(self.output_dir, f"{xml_file.stem}.usfm")

        with open(usfm_file, "w") as file:
            file.write(usfm)

    def process_word(self, word: Tree.Element):
        result = ""
        strongs = " "

        if "sub" in word.attrib:
            sub = word.attrib["sub"]
            self.subs.append((sub, word.text))
            return result

        if len(word.attrib) > 0:
            strongs += "|"

        for attr in word.attrib:
            attr_text = word.attrib[attr]
            attr_tag = self.usfm_word_tag(attr)
            attr_value = self.usfm_word_value(attr, attr_text)

            if attr_tag:
                strongs += f"{attr_tag}=\"{attr_value}\" "

        ulb_word = word.text
        source_word = word.attrib["text"] if "text" in word.attrib else ""

        occurrences = self.find_word_occurrences(ulb_word, source_word)
        result += f"\\zaln-s{strongs} {occurrences}\\*"

        for part in word.text.split():
            trimmed_part = self.r_trim_word(part)
            if len(trimmed_part) > 0:
                part_occurrences = self.find_word_part_occurrences(trimmed_part)
                result += f"\\w {part}|{part_occurrences}\\w*"

        result += f"\\zaln-e\\*\n"

        return result

    def process_phrase(self, phrase: Tree.Element):
        result = ""
        for node in phrase.findall("*"):
            if node.tag == "w":
                result += self.process_word(node)
            if node.tag == "phraseWords":
                result += node.text

        return f"{result}\n"

    def map_words(self, nodes: list[Tree.Element]):
        for node in nodes:
            if node.tag == "w":
                source = node.attrib["text"] if "text" in node.attrib else ""
                word = {"word": node.text, "source": source, "count": 0}
                self.words.append(word)
            elif node.tag == "phrase":
                self.map_words(node.findall("*"))

    def map_word_parts(self):
        for word in self.words:
            parts = word["word"].split()
            for part in parts:
                dic = {"word": self.r_trim_word(part), "source": word["source"], "count": 0}
                self.word_parts.append(dic)

    def find_word_occurrences(self, word, source):
        trimmed = self.r_trim_word(word)

        index = "word" if len(trimmed) > 0 else "source"
        search = word if len(trimmed) > 0 else source

        def func(w):
            if w[index] == search:
                w["count"] += 1
            return w

        self.words = list(map(func, self.words))
        found = [w for w in self.words if w[index] == search]

        occurrence = found[0]["count"] if len(found) > 0 else 0
        occurrences = len(found)
        return f"x-occurrence=\"{occurrence}\" x-occurrences=\"{occurrences}\""

    def find_word_part_occurrences(self, word):
        def func(p):
            if p["word"] == word:
                p["count"] += 1
            return p

        self.word_parts = list(map(func, self.word_parts))
        found = [p for p in self.word_parts if p["word"] == word]

        occurrence = found[0]["count"] if len(found) > 0 else 0
        occurrences = len(found)

        return f"x-occurrence=\"{occurrence}\" x-occurrences=\"{occurrences}\""

    @staticmethod
    def r_trim_word(word):
        trimmed = word
        if not word[-1].isalpha():
            trimmed = word.strip(word[-1])
        return trimmed

    @staticmethod
    def usfm_word_tag(tag_name):
        if tag_name == "strongs":
            return "x-strong"
        elif tag_name == "lemma":
            return "x-lemma"
        elif tag_name == "morph":
            return "x-morph"
        elif tag_name == "text":
            return "x-content"
        else:
            return None

    @staticmethod
    def align_strong_number(value, is_nt):
        if is_nt:
            number = f"{value[1:]}0"
            value = f"{value[0]}{number.zfill(5)}"

        return value

    @staticmethod
    def align_morph(value, is_nt):
        lang = "Gr" if is_nt else "He"
        value = re.sub(r"-", ",", value)
        return f"{lang},{value}"

    @staticmethod
    def split_tags(text: str):
        tags = text.split(f"\\")
        text = ""
        for tag in tags:
            tag = tag.strip()
            if tag == "":
                continue

            text += f"\\{tag}\n"
        return text

    @staticmethod
    def is_nt(slug: str):
        book = [b for b in books if b["slug"] == slug]
        if len(book) != 1:
            print(f"Unknown book: {slug}")
            return

        return book[0]["sort"] > 39

    def usfm_word_value(self, tag_name, tag_value):
        is_new_test = self.is_nt(self.book_slug)
        if tag_name == "strongs":
            return self.align_strong_number(tag_value, is_new_test)
        elif tag_name == "morph":
            return self.align_morph(tag_value, is_new_test)
        else:
            return tag_value


def get_arguments() -> Tuple[Namespace, List[str]]:
    """ Parse command line arguments """

    parser = argparse.ArgumentParser(description='Convert OSIS xml to USFM aligned')
    parser.add_argument('-i', '--input', type=lambda p: Path(p).absolute(), help='Input directory')
    parser.add_argument('-o', '--output', type=lambda p: Path(p).absolute(), help='Output directory')

    return parser.parse_known_args()


def main():
    """ Launch application """

    args, unknown = get_arguments()

    app = Converter(args.input, args.output)
    app.start()


if __name__ == "__main__":
    main()
