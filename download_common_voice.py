"""
Download and prepare infore dataset
"""
import os
from argparse import ArgumentParser
from pathlib import Path

import pooch
from pooch import Untar
from tqdm.cli import tqdm

from normalize_text import normalize_text


def download_cv():
    files = pooch.retrieve(
        url="https://huggingface.co/datasets/ntt123/infore/resolve/main/cv-corpus-8.0-2022-01-19-vi.tar.gz",
        known_hash="38782df109852d3cbc6a7b788bfa3a745648c1886a4e81acd2a600b529a4fbe5",
        processor=Untar(),
        progressbar=True,
    )
    data_dir = Path(sorted(files)[0]).parent.parent
    return data_dir


parser = ArgumentParser()
parser.add_argument("--output-dir", type=Path, default="data")
args = parser.parse_args()


data_dir = download_cv()

meta_file = data_dir / "validated.tsv"

f = open(meta_file, "r", encoding="utf-8")

for line in tqdm(f.readlines()[1:]):
    ident, path, text, *_ = line.strip().split("\t")
    spk = ident[:10]
    mp3_file = data_dir / "clips" / path
    if not mp3_file.is_file():
        continue
    text = normalize_text(text)

    out_dir = args.output_dir / f"common_voice_spk_{spk}"
    out_dir.mkdir(parents=True, exist_ok=True)
    wav_file = out_dir / (mp3_file.stem + ".wav")
    os.system(f"sox {mp3_file} -r 16k -b 16 -c 1 --norm=-3 {wav_file}")
    txt_file = wav_file.with_suffix(".txt")

    with open(txt_file, "w", encoding="utf-8") as f:
        f.write(text)
