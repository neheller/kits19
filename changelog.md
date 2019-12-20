# KiTS19 Changelog

## December 20, 2019 -- Label Corrections from After the Freeze
* Removed a fluid collection in spleen from kidney label of case_00015
* A large cystic lesion in case_00037 has been relabeled from 'cyst' to tumor
* Location and extents of tumors in cases 23 and 125 were fixed


## April 15, 2019 -- Amended Training Data Release

* Improved visualization
  * `visualize.py` now allows for a `--plane` argument (`-p`) where you can specify `axial`, `coronal`, or `sagittal`.
  * The pixels will be interpolated to an aspect ratio consistent with the real world in all cases.
* Cropped cases 22, 61, and 117
  * These had a second series at a different contrast phase appended to the end of their z-dimensions ([#6](https://github.com/neheller/kits19/issues/6)).
* Parapelvic cysts and hydronephrosis were corrected
  * Case 155 had a cyst that was originally mistaken for hydro ([#10](https://github.com/neheller/kits19/issues/10)).
  * Case 166 had hydro that was originally mistaken for a cyst  ([#11](https://github.com/neheller/kits19/issues/11)).
* Fixed holes in tumor and kidney annotations
  * Thresholds were adjusted to avoid the exclusion of hypodense tissue in kidney and tumor interiors  ([#12](https://github.com/neheller/kits19/issues/12)).
* Four cases were replaced entirely
  * The tumors in cases 60 and 174 were complex cysts. The decision was made to exclude these from our cohort to avoid ambiguity with other cysts labeled as kidney.
  * The tumor in case 15 was actually a blown out lower pole.
  * The tumor in case 102 was actually an adrenal cortical carcinoma abutting the kidney.
* The pelvic kidney in case 40 was annotated
  * This was missed in the original release
* The hilum issues in case 42 were corrected
  * On both the left and right side, the upper pole hilums were not handled correctly.
* The affine matrices were corrected
  * In the initial release, the slice thickness was incorrect for many thin-cut cases  ([#8](https://github.com/neheller/kits19/issues/8)).
  * In the initial release, the affine matrices were incorrectly flipped along the horizontal axis  ([#9](https://github.com/neheller/kits19/issues/9)).

## March 15, 2019  -- Initial Training Data Release

* 210 Cases in original spacing were added, along with some starter code to visualize the imaging and segmentation labels in the axial plane.
