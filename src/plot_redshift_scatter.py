import logging
import matplotlib.pyplot as plt
from redshift_catalogs import crossmatch_photoz_specz

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

def main():
    # matched has both spec-z + photo-z for the same objects
    _, _, matched = crossmatch_photoz_specz()
    logger.info(f"Matched galaxies: {len(matched)}")

    fig, ax = plt.subplots(figsize=(5, 5))

    # the diagonal line represents a perfect 1:1 mapping
    ax.plot([0, 6], [0, 6], color="red", lw=1)

    # scatter of the actual values
    ax.scatter(
        matched["z_spec"],
        matched["z_phot"],
        s=12,
        c="black",
        alpha=0.6
    )

    ax.set_xlim(0, 6)
    ax.set_ylim(0, 6)

    ax.set_xlabel("Spectroscopic Redshift")
    ax.set_ylabel("Photometric Redshift")
    ax.set_title("Photometric vs. Spectroscopic Redshift")

    fig.savefig("../plots/zphot_vs_zspec.png", dpi=300)
    logger.info("Saved ../plots/zphot_vs_zspec.png")

if __name__ == "__main__":
    main()

