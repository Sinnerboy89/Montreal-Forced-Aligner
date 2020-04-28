import sys, logging
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

# NOTE: local storage on mill used
input_dir = Path(sys.argv[1])
output_dir = Path(sys.argv[2])

# wav files - resample down to 16k as we're copying/renaming
procs = []
for wav in tqdm(input_dir.glob("*/*/*.wav")):
    wav_name_split = wav.name.split("_")
    speaker_id = int(wav_name_split[0])
    wav_name_split[0] = f"{speaker_id:04}"
    wav_name_new = "_".join(wav_name_split)
    outfile = output_dir / wav_name_new
    if (outfile).is_file():
        continue
    cmd = ["sox", "-R", str(wav), str(outfile), "rate", "-v", "16000"]
    procs.append(MultiCall(cmd))
    multithreadedcalls(procs, log, max_workers=20)

# txt files - just copy over with rename
for txt in tqdm(input_dir.glob("*/*/*.normalized.txt")):
    txt_name_split = txt.name.split("_")
    speaker_id = int(txt_name_split[0])
    txt_name_split[0] = f"{speaker_id:04}"
    txt_name_new = "_".join(txt_name_split)

    # if it's there already, don't copy
    if (output_dir / txt_name_new).is_file():
        continue

    # if corresponding wav can't be found, don't copy
    corresponding_wav = Path(
        str(output_dir / txt_name_new).replace(".normalized", "")
    ).with_suffix(".wav")
    if not corresponding_wav.is_file():
        continue

    copy(txt, output_dir / txt_name_new)
