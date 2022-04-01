"""
Create a lexicon file from data
"""
from argparse import ArgumentParser
from pathlib import Path
from tqdm.cli import tqdm


parser = ArgumentParser()
parser.add_argument("--data-dir", type=Path, required=True)
args = parser.parse_args()

txt_files = sorted(args.data_dir.glob("*/*.txt"))

words = []
for f in tqdm(txt_files):
    text = open(f, "r", encoding="utf-8").read()
    words.extend(text.lower().split())


words = sorted(set(words))

with open(args.data_dir / "lexicon.txt", "w", encoding="utf-8") as f:
    for word in words:
        phones = " ".join(list(word))
        f.write(f"{word}\t {phones}\n")
