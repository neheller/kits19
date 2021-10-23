from pathlib import Path
import argparse

import numpy as np
from imageio import imwrite
from PIL import Image

from starter_code.utils import load_case


# Constants
DEFAULT_KIDNEY_COLOR = [255, 0, 0]
DEFAULT_TUMOR_COLOR = [0, 0, 255]
DEFAULT_HU_MAX = 512
DEFAULT_HU_MIN = -512
DEFAULT_OVERLAY_ALPHA = 0.3
DEFAULT_PLANE = "axial"


def hu_to_grayscale(volume, hu_min, hu_max):
    # Clip at max and min values if specified
    if hu_min is not None or hu_max is not None:
        volume = np.clip(volume, hu_min, hu_max)

    # Scale to values between 0 and 1
    mxval = np.max(volume)
    mnval = np.min(volume)
    im_volume = (volume - mnval)/max(mxval - mnval, 1e-3)

    # Return values scaled to 0-255 range, but *not cast to uint8*
    # Repeat three times to make compatible with color overlay
    im_volume = 255*im_volume
    return np.stack((im_volume, im_volume, im_volume), axis=-1)


def class_to_color(segmentation, k_color, t_color):
    # initialize output to zeros
    shp = segmentation.shape
    seg_color = np.zeros((shp[0], shp[1], shp[2], 3), dtype=np.float32)

    # set output to appropriate color at each location
    seg_color[np.equal(segmentation,1)] = k_color
    seg_color[np.equal(segmentation,2)] = t_color
    return seg_color


def overlay(volume_ims, segmentation_ims, segmentation, alpha):
    # Get binary array for places where an ROI lives
    segbin = np.greater(segmentation, 0)
    repeated_segbin = np.stack((segbin, segbin, segbin), axis=-1)
    # Weighted sum where there's a value to overlay
    overlayed = np.where(
        repeated_segbin,
        np.round(alpha*segmentation_ims+(1-alpha)*volume_ims).astype(np.uint8),
        np.round(volume_ims).astype(np.uint8)
    )
    return overlayed


def visualize(cid, destination, hu_min=DEFAULT_HU_MIN, hu_max=DEFAULT_HU_MAX, 
    k_color=DEFAULT_KIDNEY_COLOR, t_color=DEFAULT_TUMOR_COLOR,
    alpha=DEFAULT_OVERLAY_ALPHA, plane=DEFAULT_PLANE, less_ram=False):

    plane = plane.lower()

    plane_opts = ["axial", "coronal", "sagittal"]
    if plane not in plane_opts:
        raise ValueError((
            "Plane \"{}\" not understood. " 
            "Must be one of the following\n\n\t{}\n"
        ).format(plane, plane_opts))

    # Prepare output location
    out_path = Path(destination)
    if not out_path.exists():
        out_path.mkdir()  

    # Load segmentation and volume
    vol, seg = load_case(cid)
    spacing = vol.affine
    vol = vol.get_data()
    seg = seg.get_data()
    seg = seg.astype(np.int32)
    
    vol_ims = None
    seg_ims = None
    if not less_ram:
        # Convert to a visual format
        vol_ims = hu_to_grayscale(vol, hu_min, hu_max).astype(np.uint8)
        seg_ims = class_to_color(seg, k_color, t_color).astype(np.uint8)
    
    # Save individual images to disk
    if plane == plane_opts[0]:
        if less_ram:
            for j in range(vol.shape[0]):
                vol_ims = hu_to_grayscale(vol[j:j+1], hu_min, hu_max)
                seg_ims = class_to_color(seg[j:j+1], k_color, t_color)

                viz_ims = overlay(vol_ims, seg_ims, seg[j:j+1], alpha)
                for i in range(viz_ims.shape[0]):
                    fpath = out_path / ("{:05d}.png".format(j))
                    imwrite(str(fpath), viz_ims[i])

        else:
            # Overlay the segmentation colors
            viz_ims = overlay(vol_ims, seg_ims, seg, alpha)
            for i in range(viz_ims.shape[0]):
                fpath = out_path / ("{:05d}.png".format(i))
                imwrite(str(fpath), viz_ims[i])

    if plane == plane_opts[1]:
        # I use sum here to account for both legacy (incorrect) and 
        # fixed affine matrices
        spc_ratio = np.abs(spacing[2,0])/np.abs(spacing[0,2])

        if less_ram:
            for j in range(vol.shape[1]):
                vol_ims = hu_to_grayscale(vol[:,j:j+1], hu_min, hu_max).astype(np.uint8)
                seg_ims = class_to_color(seg[:,j:j+1], k_color, t_color).astype(np.uint8)

                for i in range(vol_ims.shape[1]):
                    fpath = out_path / ("{:05d}.png".format(j))
                    vol_im = np.array(Image.fromarray(
                        vol_ims[:,i,:]
                    ).resize((
                            int(vol_ims.shape[2]),
                            int(vol_ims.shape[0]*spc_ratio)
                        ), resample=Image.BICUBIC
                    ))
                    seg_im = np.array(Image.fromarray(
                        seg_ims[:,i,:]
                    ).resize((
                            int(vol_ims.shape[2]),
                            int(vol_ims.shape[0]*spc_ratio)
                        ), resample=Image.NEAREST
                    ))
                    sim = np.array(Image.fromarray(
                        seg[:,j,:]
                    ).resize((
                            int(vol_ims.shape[2]),
                            int(vol_ims.shape[0]*spc_ratio)
                        ), resample=Image.NEAREST
                    ))
                    viz_im = overlay(vol_im, seg_im, sim, alpha)
                    imwrite(str(fpath), viz_im)

        else:
            for i in range(vol_ims.shape[1]):
                fpath = out_path / ("{:05d}.png".format(i))
                vol_im = np.array(Image.fromarray(
                    vol_ims[:,i,:]
                ).resize((
                        int(vol_ims.shape[2]),
                        int(vol_ims.shape[0]*spc_ratio)
                    ), resample=Image.BICUBIC
                ))
                seg_im = np.array(Image.fromarray(
                    seg_ims[:,i,:]
                ).resize((
                        int(vol_ims.shape[2]),
                        int(vol_ims.shape[0]*spc_ratio)
                    ), resample=Image.NEAREST
                ))
                sim = np.array(Image.fromarray(
                    seg[:,i,:]
                ).resize((
                        int(vol_ims.shape[2]),
                        int(vol_ims.shape[0]*spc_ratio)
                    ), resample=Image.NEAREST
                ))
                viz_im = overlay(vol_im, seg_im, sim, alpha)
                imwrite(str(fpath), viz_im)


    if plane == plane_opts[2]:
        # I use sum here to account for both legacy (incorrect) and 
        # fixed affine matrices
        spc_ratio = np.abs(spacing[2,0])/np.abs(spacing[1,1])

        if less_ram:
            for j in range(vol.shape[2]):
                vol_ims = hu_to_grayscale(vol[:,:,j:j+1], hu_min, hu_max).astype(np.uint8)
                seg_ims = class_to_color(seg[:,:,j:j+1], k_color, t_color).astype(np.uint8)

                for i in range(vol_ims.shape[2]):
                    fpath = out_path / ("{:05d}.png".format(j))
                    vol_im = np.array(Image.fromarray(
                        vol_ims[:,:,i]
                    ).resize((
                            int(vol_ims.shape[1]),
                            int(vol_ims.shape[0]*spc_ratio)
                        ), resample=Image.BICUBIC
                    ))
                    seg_im = np.array(Image.fromarray(
                        seg_ims[:,:,i]
                    ).resize((
                            int(vol_ims.shape[1]),
                            int(vol_ims.shape[0]*spc_ratio)
                        ), resample=Image.NEAREST
                    ))
                    sim = np.array(Image.fromarray(
                        seg[:,:,j]
                    ).resize((
                            int(vol_ims.shape[1]),
                            int(vol_ims.shape[0]*spc_ratio)
                        ), resample=Image.NEAREST
                    ))
                    viz_im = overlay(vol_im, seg_im, sim, alpha)
                    imwrite(str(fpath), viz_im)

        else:
            for i in range(vol_ims.shape[2]):
                fpath = out_path / ("{:05d}.png".format(i))
                vol_im = np.array(Image.fromarray(
                    vol_ims[:,:,i]
                ).resize((
                        int(vol_ims.shape[1]),
                        int(vol_ims.shape[0]*spc_ratio)
                    ), resample=Image.BICUBIC
                ))
                seg_im = np.array(Image.fromarray(
                    seg_ims[:,:,i]
                ).resize((
                        int(vol_ims.shape[1]),
                        int(vol_ims.shape[0]*spc_ratio)
                    ), resample=Image.NEAREST
                ))
                sim = np.array(Image.fromarray(
                    seg[:,:,i]
                ).resize((
                        int(vol_ims.shape[1]),
                        int(vol_ims.shape[0]*spc_ratio)
                    ), resample=Image.NEAREST
                ))
                viz_im = overlay(vol_im, seg_im, sim, alpha)
                imwrite(str(fpath), viz_im)


if __name__ == '__main__':
    # Parse command line arguments
    desc = "Overlay a case's segmentation and store it as a series of pngs"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument(
        "-c", "--case_id", required=True,
        help="The identifier for the case you would like to visualize"
    )
    parser.add_argument(
        "-d", "--destination", required=True,
        help="The location where you'd like to store the series of pngs"
    )
    parser.add_argument(
        "-u", "--upper_hu_bound", required=False, default=DEFAULT_HU_MAX,
        help="The upper bound at which to clip HU values"
    )
    parser.add_argument(
        "-l", "--lower_hu_bound", required=False, default=DEFAULT_HU_MIN,
        help="The lower bound at which to clip HU values"
    )
    parser.add_argument(
        "-p", "--plane", required=False, default=DEFAULT_PLANE,
        help=(
            "The plane in which to visualize the data"
            " (axial, coronal, or sagittal)"
        )
    )
    args = parser.parse_args()

    # Run visualization
    visualize(
        args.case_id, args.destination, 
        hu_min=args.lower_hu_bound, hu_max=args.upper_hu_bound,
        plane=args.plane
    )
