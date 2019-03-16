from pathlib import Path

import nibabel as nib


def load_case(cid):
    # Resolve location where data should be living
    data_path = Path(__file__).parent.parent / "data"
    if not data_path.exists():
        raise IOError(
            "Data path, {}, could not be resolved".format(str(data_path))
        )

    # Get case_id from provided cid
    try:
        cid = int(cid)
        case_id = "case_{:05d}".format(cid)
    except ValueError:
        case_id = cid

    # Make sure that case_id exists under the data_path
    case_path = data_path / case_id
    if not case_path.exists():
        raise ValueError(
            "Case could not be found \"{}\"".format(case_path.name)
        )

    vol = nib.load(str(case_path / "imaging.nii.gz"))
    seg = nib.load(str(case_path / "segmentation.nii.gz"))
    return vol, seg
