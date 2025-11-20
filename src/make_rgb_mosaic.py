"""
This script is to create an RGB HUDF mosaic using:
    blue: HLF GOODS-S F435W (60mas)
    green: HLF GOOD-S F606W (60mas)
    red: XDF HUDF F814W (60mas) <- chose this because my red was too blue before
    
    then: save as a png
"""

import numpy as np
from astropy.io import fits
from astropy.io import fits
from astropy.visualization import PercentileInterval, AsinhStretch
import matplotlib.pyplot as plt
from astropy.wcs import WCS
from astropy.wcs.utils import pixel_to_skycoord, skycoord_to_pixel

def load_fits(filename):
    data, hdr = fits.getdata(filename, header=True)
    wcs = WCS(hdr)
    return data.astype(np.float32), wcs

def match_cutout(source_data, source_wcs, ref_wcs, ny, nx):
    """
    finds RA/Dec and converts corners to RA/Dec values to pixel coords. Then the source array is sliced
    """
    corners_ref = np.array([
        [0, 0],
        [0, ny],
        [nx, 0],
        [nx, ny]
        ])
    # converting ref pixels
    sky = pixel_to_skycoord(corners_ref[:,0], corners_ref[:,1], ref_wcs)

    # converting RA/Dec to pixel coordinates
    sx, sy = skycoord_to_pixel(sky, source_wcs)

    xmin = int(np.min(sx))
    xmax = int(np.max(sx))
    ymin = int(np.min(sy))
    ymax = int(np.max(sy))

    return source_data[ymin:ymax, xmin:xmax]

def scale_band(data, p_low=1.0, p_high=99.7):
    lo, hi = np.percentile(data, [p_low, p_high])
    if hi <= lo:
        # avoid divide-by-zero if something pathological happens
        return np.zeros_like(data, dtype=np.float32)

    scaled = np.clip((data - lo) / (hi - lo), 0, 1)
    stretched = np.arcsinh(5 * scaled)
    stretched /= stretched.max()
    return stretched

def make_rgb_and_axes():
    """
    Build the XDF RGB mosaic and return fig, ax, WCS, and cutout shape.
    """
    r_data, r_wcs = load_fits("../data/hlsp_xdf_hst_acswfc-60mas_hudf_f814w_v1_sci.fits")
    g_data, g_wcs = load_fits("../data/hlsp_xdf_hst_acswfc-60mas_hudf_f606w_v1_sci.fits")
    b_data, b_wcs = load_fits("../data/hlsp_xdf_hst_acswfc-60mas_hudf_f435w_v1_sci.fits")

    ny, nx = r_data.shape

    b_cut = match_cutout(b_data, b_wcs, r_wcs, ny, nx)
    g_cut = match_cutout(g_data, g_wcs, r_wcs, ny, nx)
    r_cut = r_data.copy()

    hmin = min(b_cut.shape[0], g_cut.shape[0], r_cut.shape[0])
    wmin = min(b_cut.shape[1], g_cut.shape[1], r_cut.shape[1])

    b_cut = b_cut[:hmin, :wmin]
    g_cut = g_cut[:hmin, :wmin]
    r_cut = r_cut[:hmin, :wmin]

    # you can keep these simple, or plug in your tuned parameters
    r = scale_band(r_cut)
    g = scale_band(g_cut)
    b = scale_band(b_cut)

    rgb = np.dstack([r, g, b])

    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111, projection=r_wcs)

    ax.imshow(rgb, origin="lower")
    ax.set_xlabel("RA")
    ax.set_ylabel("Dec")
    ax.set_title("XDF RGB Mosaic")
    ax.grid(color="white", alpha=0.3)

    return fig, ax, r_wcs, hmin, wmin


def make_rgb():
    """
    build the RGB mosaic and save to a PNG.
    """
    fig, ax, _, _, _ = make_rgb_and_axes()
    plt.tight_layout()
    plt.savefig("../plots/xdf_rgb.png", dpi=300)
    print("saved")

if __name__ == "__main__":
    make_rgb()
