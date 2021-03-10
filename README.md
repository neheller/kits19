# KiTS19

The official [2019 KiTS Challenge](https://kits19.grand-challenge.org) repository.

**Note**: The 2021 iteration of this challenge is in progress!
- [KiTS21 GitHub](https://github.com/neheller/kits21)
- [KiTS21 Homepage](https://kits21.kits-challenge.org/) (unfinished)

## Usage

To get the data for this challenge, please clone this repository (~500MB), and then run `get_imaging.py`. For example
```text
git clone https://github.com/neheller/kits19
cd kits19
pip3 install -r requirements.txt
python3 -m starter_code.get_imaging
```
This will download the much larger and static image files from a separate source. The `data/` directory should then be structured as follows

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

We've provided some basic Python scripts in `starter_code/` for loading and/or visualizing the data. 

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

Each `Nift1Image` object has an attribute called `affine`. This is a 4x4 matrix, and in our case, it takes the value
```
array([[0.                          , 0.                      , -1*captured_pixel_width , 0. ],
       [0.                          , -1*captured_pixel_width , 0.                      , 0. ],
       [-1*captured_slice_thickness , 0.                      , 0.                      , 0. ],
       [0.                          , 0.                      , 0.                      , 1. ]])
```
This information is also available in `data/kits.json`. Since this data was collected during routine clinical practice from many centers, these values vary quite a bit.

Since spatially inconsistent data might not be ideal for machine learning applications, we have created a branch called `interpolated` with the same data but with the same affine transformation for each patient.
```
array([[ 0.        ,  0.        , -0.78162497,  0.        ],
       [ 0.        , -0.78162497,  0.        ,  0.        ],
       [-3.        ,  0.        ,  0.        ,  0.        ],
       [ 0.        ,  0.        ,  0.        ,  1.        ]])
```

### Labeling Errors

We've gone to great lengths to produce the best segmentation labels that we could. That said, *we're certainly not perfect*. In an attempt to strike a balance between quality and stability, we've decided on the following policy: 

If you find an problem with the data, please [submit an issue](https://github.com/neheller/kits19/issues/new) describing it. 

## Challenge Results and References

The KiTS19 challenge was held in conjunction with MICCAI 2019 in Shenzhen, China. The official leaderboard for the challenge can be found [here](http://results.kits-challenge.org/miccai2019/), and the live leaderboard for new submissions can be found [on grand-challenge.org](https://kits19.grand-challenge.org/evaluation/results/). 

[A paper](https://www.sciencedirect.com/science/article/pii/S1361841520301857) describing the results and conclusions of the challenge has been accepted at Medical Image Analysis. For further reading, an in-depth description of how the dataset was collected an annotated can be found [on arxiv](https://arxiv.org/abs/1904.00445). If this data is useful to your research, please cite these papers as

```
@article{heller2020state,
  title={The state of the art in kidney and kidney tumor segmentation in contrast-enhanced CT imaging: Results of the KiTS19 Challenge},
  author={Heller, Nicholas and Isensee, Fabian and Maier-Hein, Klaus H and Hou, Xiaoshuai and Xie, Chunmei and Li, Fengyi and Nan, Yang and Mu, Guangrui and Lin, Zhiyong and Han, Miofei and others},
  journal={Medical Image Analysis},
  pages={101821},
  year={2020},
  publisher={Elsevier}
}
@article{heller2019kits19,
  title={The kits19 challenge data: 300 kidney tumor cases with clinical context, ct semantic segmentations, and surgical outcomes},
  author={Heller, Nicholas and Sathianathen, Niranjan and Kalapara, Arveen and Walczak, Edward and Moore, Keenan and Kaluzniak, Heather and Rosenberg, Joel and Blake, Paul and Rengel, Zachary and Oestreich, Makinna and others},
  journal={arXiv preprint arXiv:1904.00445},
  year={2019}
}
```
