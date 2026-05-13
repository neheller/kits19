from pathlib import Path
from shutil import move
import os
import sys
import time

from tqdm import tqdm
import requests
import numpy as np

HF_DATASET_REPO = "neheller/KiTS-Challenge-Imaging"
HF_DATASET_REVISION = "main"
HF_DATASET_BASE_URL = (
    "https://huggingface.co/datasets/{}/resolve/{}"
    .format(HF_DATASET_REPO, HF_DATASET_REVISION)
)
temp_f = Path(__file__).parent / "temp.tmp"


def get_destination(i):
    destination = Path("__file__").parent.parent /\
        "data" / "case_{:05d}".format(i) / "imaging.nii.gz"
    if not destination.parent.exists():
        destination.parent.mkdir()
    return destination


def cleanup(bar, msg):
    bar.close()
    if temp_f.exists():
        temp_f.unlink()
    print(msg)
    sys.exit()


if __name__ == "__main__":
    left_to_download = []
    for i in range(300):
        if not get_destination(i).exists():
            left_to_download = left_to_download + [i]


    print("{} cases to download...".format(len(left_to_download)))
    for i, cid in enumerate(left_to_download):
        print("Download {}/{}: ".format(
            i+1, len(left_to_download)
        ))
        destination = get_destination(cid)
        uri = "{}/images/case_{:05d}.nii.gz".format(HF_DATASET_BASE_URL, cid)

        chnksz = 1000
        tries = 0
        while True:
            try:
                tries = tries + 1
                response = requests.get(uri, stream=True)
                break
            except Exception as e:
                print("Failed to establish connection with server:\n")
                print(str(e) + "\n")
                if tries < 1000:
                    print("Retrying in 30s")
                    time.sleep(30)
                else:
                    print("Max retries exceeded")
                    sys.exit()

        try:
            with temp_f.open("wb") as f:
                bar = tqdm(
                    unit="KB", 
                    desc="case_{:05d}".format(cid), 
                    total=int(
                        np.ceil(int(response.headers["content-length"])/chnksz)
                    )
                )
                for pkg in response.iter_content(chunk_size=chnksz):
                    f.write(pkg)
                    bar.update(int(len(pkg)/chnksz))

                bar.close()
            move(str(temp_f), str(destination))
        except KeyboardInterrupt:
            cleanup(bar, "KeyboardInterrupt")
        except Exception as e:
            cleanup(bar, str(e))



