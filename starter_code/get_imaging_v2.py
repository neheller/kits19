from pathlib import Path
import shutil
import os
import sys
import time

import requests

imaging_url = "https://kits19.sfo2.digitaloceanspaces.com/"
imaging_name_tmplt = "master_{:05d}.nii.gz"
temp_f = Path(__file__).parent / "temp.tmp"


def get_destination(i, create):
    destination = Path(__file__).parent.parent /\
        "data" / "case_{:05d}".format(i) / "imaging.nii.gz"
    if create and not destination.parent.exists():
        destination.parent.mkdir()
    return destination


def cleanup(msg):
    if temp_f.exists():
        temp_f.unlink()
    print(msg)
    sys.exit()


def download(cid):
    remote_name = imaging_name_tmplt.format(cid)
    url = imaging_url + remote_name
    try:
        with requests.get(url, stream=True) as r:
            with temp_f.open('wb') as f:
                shutil.copyfileobj(r.raw, f)
        shutil.move(str(temp_f), str(get_destination(cid, True)))
    except KeyboardInterrupt:
        cleanup("KeyboardInterrupt")
    except Exception as e:
        cleanup(str(e))


if __name__ == "__main__":
    if not Path("data").exists():
        Path("data").mkdir()
    left_to_download = []
    for i in range(300):
        dst = get_destination(i, False)
        if not dst.exists():
            left_to_download = left_to_download + [i]

    print("{} cases to download...".format(len(left_to_download)))
    for i, cid in enumerate(left_to_download):
        print("{}/{}... ".format(i+1, len(left_to_download)))
        download(cid)