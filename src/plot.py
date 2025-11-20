import numpy as np
import matplotlib.pyplot as plt

from astropy.coordinates import SkyCoord
from astropy.wcs import WCS
from astropy.wcs.utils import skycoord_to_pixel
import astropy.units as u

from make_rgb_mosaic import load_fits, match_cutout, scale_band
from redshift_catalogs import crossmatch_photoz_specz

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def make_rgb_for_overlay():
    """Build XDF HUDF RGB and return fig, ax, WCS, and trimmed shape"""
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

    r = scale_band(r_cut)
    g = scale_band(g_cut)
    b = scale_band(b_cut)

    rgb = np.dstack([r, g, b])

    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111, projection=r_wcs)
    ax.imshow(rgb, origin="lower")

    ax.set_xlabel("RA")
    ax.set_ylabel("Dec")
    ax.set_title("XDF HUDF RGB with Redshifts")
    ax.grid(color="white", alpha=0.3)

    return fig, ax, r_wcs, hmin, wmin


def overlay_redshifts(ax, r_wcs, hmin, wmin):
    """
    overlays photometric-only and matched photo+spec galaxies
    """

    photo, spec, matched = crossmatch_photoz_specz()
    logger.info(f"Overlaying {len(photo)} photo-z and {len(matched)} matched photo+spec galaxies")
    
    if len(photo) == 0:
        logger.warning("No photometric redshift sources found")
        return 

    # Convert to sky coords
    c_photo = SkyCoord(photo["ra"]*u.deg, photo["dec"]*u.deg)
    c_matched = SkyCoord(matched["ra"]*u.deg, matched["dec"]*u.deg)

    # photo-only mask
    sep = c_photo.match_to_catalog_sky(c_matched)[1]
    photo_only = photo[sep > 1e-6*u.arcsec]

    # Convert pixel coords
    xp, yp = skycoord_to_pixel(SkyCoord(photo_only["ra"]*u.deg,
                                        photo_only["dec"]*u.deg),
                               r_wcs)

    xm, ym = skycoord_to_pixel(c_matched, r_wcs)

    # in-frame mask
    p_mask = (xp>=0)&(xp<wmin)&(yp>=0)&(yp<hmin)
    m_mask = (xm>=0)&(xm<wmin)&(ym>=0)&(ym<hmin)

    # plot photo-only
    ax.scatter(xp[p_mask], yp[p_mask],
               s=2, c="cyan", alpha=0.35,
               label="photo-z only", zorder=2)

    ax.scatter(xm[m_mask], ym[m_mask],
               s=18, facecolors="none",
               edgecolors="yellow", linewidths=2.0,
               label="photo+spec", zorder=4)

    ax.legend(loc="lower left", fontsize=8)

def main():
    fig, ax, r_wcs, hmin, wmin = make_rgb_for_overlay()
    overlay_redshifts(ax, r_wcs, hmin, wmin)
    plt.tight_layout()
    fig.savefig("../plots/xdf_hudf_rgb_redshifts.png", dpi=300)
    print("saved ../plots/xdf_hudf_rgb_redshifts.png")


if __name__ == "__main__":
    main()

