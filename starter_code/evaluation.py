from starter_code.utils import load_segmentation

import numpy as np
import nibabel as nib


def evaluate(case_id, predictions):
    # Handle case of softmax output
    if len(predictions.shape) == 4:
        predictions = np.argmax(predictions, axis=-1)

    # Check predictions for type and dimensions
    if not isinstance(predictions, (np.ndarray, nib.Nifti1Image)):
        raise ValueError("Predictions must by a numpy array or Nifti1Image")
    if isinstance(predictions, nib.Nifti1Image):
        predictions = predictions.get_data()

    if not np.issubdtype(predictions.dtype, np.integer):
        predictions = np.round(predictions)
    predictions = predictions.astype(np.uint8)

    # Load ground truth segmentation
    gt = load_segmentation(case_id).get_data()

    # Make sure shape agrees with case
    if not predictions.shape == gt.shape:
        raise ValueError(
            ("Predictions for case {} have shape {} "
            "which do not match ground truth shape of {}").format(
                case_id, predictions.shape, gt.shape
            )
        )

    try:
        # Compute tumor+kidney Dice
        tk_pd = np.greater(predictions, 0)
        tk_gt = np.greater(gt, 0)
        tk_dice = 2*np.logical_and(tk_pd, tk_gt).sum()/(
            tk_pd.sum() + tk_gt.sum()
        )
    except ZeroDivisionError:
        return 0.0, 0.0

    try:
        # Compute tumor Dice
        tu_pd = np.greater(predictions, 1)
        tu_gt = np.greater(gt, 1)
        tu_dice = 2*np.logical_and(tu_pd, tu_gt).sum()/(
            tu_pd.sum() + tu_gt.sum()
        )
    except ZeroDivisionError:
        return tk_dice, 0.0

    return tk_dice, tu_dice

