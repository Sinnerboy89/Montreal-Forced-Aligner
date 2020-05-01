import sys, csv, os
from pathlib import Path
from shutil import copy
from tqdm import tqdm

input_dir = Path(sys.argv[1])
output_dir = Path(sys.argv[2])
if not output_dir.is_dir():
    output_dir.mkdir()

tsvfile = csv.reader(open(sys.argv[3], "r"), delimiter="\t")

for row in tqdm(tsvfile):
    if row[0] == "client_id":
        continue

    speaker_id = row[0]
    utt_id = row[1].split("_")[3].split(".")[0]
    mp3_path = input_dir / f"{row[1]}"
    txt_path = output_dir / f"{speaker_id}_{utt_id}.txt"
    wav_path = output_dir / f"{speaker_id}_{utt_id}.wav"

    if (wav_path).is_file():
        continue

    open(txt_path, "w").write(row[2])
    cmd = " ".join(["sox", "-R", str(mp3_path), str(wav_path), "rate", "-v", "16000"])
    os.system(cmd)
