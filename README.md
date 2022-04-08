# viet-aligner
Aligner vietnamese text and audio clip


```sh
sudo apt install -y sox libsox-fmt-mp3
```

### Install MFA

```sh
conda create -n kaldi python=3.9.12
conda activate kaldi
conda install -c conda-forge kaldi montreal-forced-aligner
```

### Download datasets

```sh
python download_infore.py --output-dir data
python download_vivos.py --output-dir data
python download_common_voice.py --output-dir data
python download_fpt_open_speech.py --output-dir data
```

### Train acoustic model

```sh
python create_lexicon.py --data-dir data
mfa train --clean -o mfa_vi_model -t ./mfa_tmp ./data ./data/lexicon.txt mfa_output
```