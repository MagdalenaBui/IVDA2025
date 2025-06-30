from pandas import read_csv, DataFrame

def load_data(path):
    return read_csv(path, quotechar="'")
    #return read_csv(path, quotechar="'").drop_duplicates()