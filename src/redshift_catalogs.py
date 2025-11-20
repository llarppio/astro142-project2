from astropy.table import Table
from astropy.coordinates import SkyCoord
import astropy.units as u
import numpy as np

PHOTOZ_FILE = "../data/uvudf_rafelski_2015.fits"
SPECZ_FILE  = "../data/Rafelski_UDF_speczlist15.txt"


def load_uvudf_photoz():
    """
    UVUDF HUDF catalog (Rafelski+ 2015) as photo-z sample.
    """
    t = Table.read(PHOTOZ_FILE)

    # column names from inspect_uvudf_catalog.py
    ra_col  = "RA"
    dec_col = "DEC"
    z_col   = "Z_BPZ"

    t = t[[ra_col, dec_col, z_col]].copy()
    t.rename_columns([ra_col, dec_col, z_col], ["ra", "dec", "z_phot"])
    
    t['ra'] = np.array(t['ra']).astype(float)
    t['dec'] = np.array(t['dec']).astype(float)
    t['z_phot'] = np.array(t['z_phot']).astype(float)

    mask = t["z_phot"] > 0
    return t[mask]


def load_uvudf_specz():
    """
    Rafelski_UDF_speczlist15.txt as spec-z sample.
    """
    t = Table.read(SPECZ_FILE, format="ascii")

    ra_col  = "col2"
    dec_col = "col3"
    z_col   = "col4"

    t = t[[ra_col, dec_col, z_col]].copy()
    t.rename_columns([ra_col, dec_col, z_col], ["ra", "dec", "z_spec"])

    mask = t["z_spec"] > 0
    return t[mask]


def crossmatch_photoz_specz(max_sep_arcsec=0.6):
    photo = load_uvudf_photoz()
    spec  = load_uvudf_specz()

    ra_photo  = np.array(photo["ra"], dtype=float)
    dec_photo = np.array(photo["dec"], dtype=float)
    ra_spec   = np.array(spec["ra"], dtype=float)
    dec_spec  = np.array(spec["dec"], dtype=float)

    c_photo = SkyCoord(ra_photo, dec_photo, unit="deg")
    c_spec  = SkyCoord(ra_spec,  dec_spec,  unit="deg")

    idx, sep2d, _ = c_photo.match_to_catalog_sky(c_spec)
    match_mask = sep2d < (max_sep_arcsec * u.arcsec)

    matched_photo = photo[match_mask]
    matched_spec  = spec[idx[match_mask]]

    matched = Table()
    matched["ra"]     = matched_photo["ra"]
    matched["dec"]    = matched_photo["dec"]
    matched["z_phot"] = matched_photo["z_phot"]
    matched["z_spec"] = matched_spec["z_spec"]

    print("photo-z size :", len(photo))
    print("spec-z size  :", len(spec))
    print("matched size :", len(matched))

    return photo, spec, matched


if __name__ == "__main__":
    photo, spec, matched = crossmatch_photoz_specz()
    print(matched[:10])

