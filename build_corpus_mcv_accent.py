import sys, logging, csv
from pathlib import Path
from shutil import copy
from tqdm import tqdm

sys.path.append(str(Path.home() / "cereproc/v48_gen"))
from lib.buildfuncs import multithreadedcalls, MultiCall

log = logging.getLogger("libritts_build")
handler = logging.StreamHandler()
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
handler.setFormatter(formatter)
log.addHandler(handler)

input_dir = Path(sys.argv[1])
output_dir = Path(sys.argv[2])
if not output_dir.is_dir():
    output_dir.mkdir()

ctr = 0
procs = []
with open(sys.argv[3], "r") as f:
    tsvfile = csv.reader(f, delimiter="\t")
    for row in tqdm(tsvfile):
        if row[0] == "client_id":
            continue

        ctr += 1
        if row[7] != sys.argv[4]:
            continue

        speaker_id = row[0]
        utt_id = row[1].split("_")[3].split(".")[0]
        mp3_path = input_dir / f"{row[1]}"
        txt_path = output_dir / f"{speaker_id}_{utt_id}.txt"
        wav_path = output_dir / f"{speaker_id}_{utt_id}.wav"

        if (wav_path).is_file():
            continue

        open(txt_path, "w").write(row[2])
        cmd = ["sox", "-R", str(mp3_path), str(wav_path), "rate", "-v", "16000"]
        procs.append(MultiCall(cmd))
        multithreadedcalls(procs, log, max_workers=4)
