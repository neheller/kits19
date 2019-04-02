# KiTS19

The official [2019 KiTS Challenge](https://kits19.grand-challenge.org) repository.

## Before Cloning
This repository makes use of git-lfs. **Make sure to [install git-lfs](https://git-lfs.github.com/) before cloning!** It's very lightweight and works with Windows, Mac, and Linux. For Linux users, I'd recommend downloading and running the installer rather than using PackageCloud. You can verify the initialization by running 
```
user@host~$ git lfs --version
git-lfs/2.7.1 (GitHub; linux amd64; go 1.12; git 6b7fb6e3)
```

## Usage

To get the data for this challenge, please clone this repository (~20G). The `data/` directory is structured as follows

```
data
├── case_00000
|   ├── imaging.nii.gz
|   └── segmentation.nii.gz
├── case_00001
|   ├── imaging.nii.gz
|   └── segmentation.nii.gz
...
├── case_00209
|   ├── imaging.nii.gz
|   └── segmentation.nii.gz
└── kits.json
```

We've provided some basic Python scripts in `starter_code/` for loading and/or visualizing the data. They require the following:

* Python >= 3.5.2
* [scipy](https://www.scipy.org/)
* [numpy](http://www.numpy.org/)
* [nibabel](https://nipy.org/nibabel/)

### Loading Data

```python
from starter_code.utils import load_case

volume, segmentation = load_case("case_00123")
# or
volume, segmentation = load_case(123)
```

Will give you two `Nifty1Image`s. Their shapes will be `(num_slices, height, width)`, and their pixel datatypes will be `np.float32` and `np.uint8` respectively. In the segmentation, a value of 0 represents background, 1 represents kidney, and 2 represents tumor.

For information about using a `Nifty1Image`, see the [Nibabel Documentation](https://nipy.org/nibabel/manual.html#manual) ([Getting Started](https://nipy.org/nibabel/gettingstarted.html))

### Visualizing Data

The `visualize.py` file will dump a series of PNG files depicting a case's imaging with the segmentation label overlayed. By default, red represents kidney and blue represents tumor.

From Bash:

```bash
python3 starter_code/visualize.py -c case_00123 -d <destination>
# or
python3 starter_code/visualize.py -c 123 -d <destination>
```

From Python:

```python
from starter_code.visualize import visualize

visualize("case_00123", <destination (str)>)
# or
visualize(123, <destination (str)>)
```

### Voxel Spacing

Each `Nift1Image` object has an attribute called `affine`. This is a 4x4 matrix, and in our case, it takes the value `np.fill_diagonal([slice_thickness, pixel_width, pixel_width, 1])`. This information is also available in `data/kits.json`. Since this data was collected during routine clinical practice from many centers, these values vary quite a bit.

If there's interest, we're happy to create a branch with the data/segmentations transformed and interpolated to a fixed spacing (or perhaps several with one for each spacing). Let us know on [this issue](https://github.com/neheller/kits19/issues/1) if this would be useful to you.

### Labeling Errors

We've gone to great lengths to produce the best segmentation labels that we could. That said, *we're certainly not perfect*. In an attempt to strike a balance between quality and stability, we've decided on the following policy: 

If you find an problem with the data, please [submit an issue](https://github.com/neheller/kits19/issues/new) describing it. We will do our best to address all issues *submitted prior to April 5, 2019* by April 15. After that, the data and labels will be set in stone until the MICCAI deadline of July 29. You're welcome to keep submitting issues on this topic after April 5, but the fixes will not be made available until after the 2019 challenge.

### Reference

If this data is useful to your research, please cite the following [manuscript](https://arxiv.org/abs/1904.00445)
```
@misc{1904.00445,
Author = {Nicholas Heller and Niranjan Sathianathen and Arveen Kalapara and Edward Walczak and Keenan Moore and Heather Kaluzniak and Joel Rosenberg and Paul Blake and Zachary Rengel and Makinna Oestreich and Joshua Dean and Michael Tradewell and Aneri Shah and Resha Tejpaul and Zachary Edgerton and Matthew Peterson and Shaneabbas Raza and Subodh Regmi and Nikolaos Papanikolopoulos and Christopher Weight},
Title = {The KiTS19 Challenge Data: 300 Kidney Tumor Cases with Clinical Context, CT Semantic Segmentations, and Surgical Outcomes},
Year = {2019},
Eprint = {arXiv:1904.00445},
}
```
