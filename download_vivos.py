"""
Download and prepare infore dataset
"""
import shutil
from argparse import ArgumentParser
from pathlib import Path

import pooch
from pooch import Untar
from tqdm.cli import tqdm

from normalize_text import normalize_text


def download_vivos_data():
    files = pooch.retrieve(
        url="https://huggingface.co/datasets/ntt123/infore/resolve/main/vivos.tar.gz",
        known_hash="147477f7a7702cbafc2ee3808d1c142989d0dbc8d9fce8e07d5f329d5119e4ca",
        processor=Untar(),
        progressbar=True,
    )
    data_dir = Path(sorted(files)[0]).parent
    return data_dir


parser = ArgumentParser()
parser.add_argument("--output-dir", type=Path, default="data")
args = parser.parse_args()


data_dir = download_vivos_data()

for split in ["test", "train"]:
    root = data_dir / split
    dic = {}
    for l in open(root / "prompts.txt", "r", encoding="utf-8").readlines():
        ident, *text = l.split(" ")
        text = " ".join(text)
        dic[ident] = normalize_text(text)

    wav_files = root.glob("waves/*/*.wav")
    for wav_file in tqdm(wav_files):
        spk = wav_file.parent.name
        out_dir = args.output_dir / f"vivos_spk_{spk}"
        out_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy(wav_file, out_dir)
        with open(out_dir / (wav_file.stem + ".txt"), "w", encoding="utf-8") as f:
            f.write(dic[wav_file.stem])
