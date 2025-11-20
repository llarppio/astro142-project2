from astropy.table import Table

t = Table.read("../data/Rafelski_UDF_speczlist15.txt", format="ascii")

print("Rows:", len(t))
print("Column names:", t.colnames)
print("\nFirst 5 rows:")
print(t[:5])

