
from astropy.table import Table

def main():
    cat = Table.read("../data/hlsp_hlf_hst_60mas_goodss_v2.1_catalog.fits")
    print("Number of rows:", len(cat))
    print("Column names:")
    for name in cat.colnames:
        print(name)

if __name__== "__main__":
    main()

