from redshift_catalogs import crossmatch_photoz_specz
import matplotlib.pyplot as plt

_, _, matched = crossmatch_photoz_specz()

fig, ax = plt.subplots()
ax.scatter(matched["z_spec"], matched["z_phot"], s=10, c="k", alpha=0.6)
ax.plot([0,6], [0,6], "red", lw=1) 
ax.set_xlim(0, 6)
ax.set_ylim(0, 6)
ax.set_xlabel("z_spec")
ax.set_ylabel("z_phot")
ax.set_title("Joint distribution of z_phot vs z_spec")
fig.savefig("../plots/zphot_vs_zspec.png", dpi=300)
