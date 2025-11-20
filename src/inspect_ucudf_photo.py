from astropy.table import Table

t = Table.read("../data/uvudf_rafelski_2015.fits")

print("Rows:", len(t))
print("Column names:")
for name in t.colnames:
    print(name)

print("\nFirst 5 rows:")
print(t[:5])

