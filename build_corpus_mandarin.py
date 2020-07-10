import sys, csv, os
from pathlib import Path
from shutil import copy
from tqdm import tqdm

wavdir = Path(sys.argv[1])
txtdir = Path(sys.argv[2])
outdir = Path(sys.argv[3])

if not outdir.is_dir():
    outdir.mkdir()

for wav_fp in tqdm(wavdir.glob("*.wav")):

    # check for corresponding .txt
    if not (txtdir / (wav_fp.stem + ".txt")).is_file():
        continue

    # check it hasn't been copied over already
    if (outdir / wav_fp.name).is_file():
        continue

    # copy wav and txt files into outdir
    copy(wav_fp, outdir)
    copy(txtdir / (wav_fp.stem + ".txt"), outdir)
