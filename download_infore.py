"""
Download and prepare infore dataset
"""
import shutil
from argparse import ArgumentParser
from pathlib import Path

import pooch
from pooch import Unzip
from tqdm.cli import tqdm
from normalize_text import normalize_text


def download_infore_data():
    files = pooch.retrieve(
        url="https://huggingface.co/datasets/ntt123/infore/resolve/main/infore_16k.zip",
        known_hash="0c9b2fd6962fd6706fa9673f94a9f1ba534edf34691247ae2be0ff490870ccd7",
        processor=Unzip(),
        progressbar=True,
    )
    data_dir = Path(sorted(files)[0]).parent
    return data_dir


parser = ArgumentParser()
parser.add_argument("--output-dir", type=Path, default="data")
args = parser.parse_args()


data_dir = download_infore_data()
text_files = sorted(data_dir.glob("*.txt"))
wav_files = [f.with_suffix(".wav") for f in text_files]

out_dir = args.output_dir / "infore_spk"
out_dir.mkdir(parents=True, exist_ok=True)

for text_file, wav_file in zip(tqdm(text_files), wav_files):
    text = open(text_file).read()
    if "\t" in text:
        continue

    text = normalize_text(text)

    shutil.copy(text_file, out_dir)
    shutil.copy(wav_file, out_dir)
