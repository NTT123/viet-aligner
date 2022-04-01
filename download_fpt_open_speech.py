"""
Download and prepare fpt open speech dataset
"""
import os
from argparse import ArgumentParser
from pathlib import Path

import pooch
from pooch import Unzip
from tqdm.cli import tqdm

from normalize_text import normalize_text


def download_fpt_open_speech_data():
    files = pooch.retrieve(
        url="https://huggingface.co/datasets/ntt123/infore/resolve/main/FPT-Open-Speech-Dataset.zip",
        known_hash="38daac2f6032c94841a75d40b99cd0071df6a3e2dcd2832f004cb73982f12706",
        processor=Unzip(),
        progressbar=True,
    )
    data_dir = Path(sorted(files)[0]).parent.parent
    return data_dir


parser = ArgumentParser()
parser.add_argument("--output-dir", type=Path, default="data")
args = parser.parse_args()


data_dir = download_fpt_open_speech_data()

meta_file = data_dir / "transcriptAll.txt"
f = open(meta_file, "r", encoding="utf-8")
for line in tqdm(f.readlines()):
    ident, text, _ = line.split("|")
    try:
        text = normalize_text(text)
    except:
        continue
    mp3_file = data_dir / "mp3" / ident
    out_dir = args.output_dir / "fpt_open_speech_spk"
    out_dir.mkdir(parents=True, exist_ok=True)
    wav_file = out_dir / (mp3_file.stem + ".wav")
    os.system(f"sox {mp3_file} -r 16k -b 16 -c 1 --norm=-3 {wav_file}")
    txt_file = wav_file.with_suffix(".txt")

    with open(txt_file, "w", encoding="utf-8") as f:
        f.write(text)
