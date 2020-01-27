import pandas as pd
import argparse

ap = argparse.ArgumentParser()
args = vars(ap.parse_args())

df = pd.read_csv("yc_cos_list.csv")
co_descp = df['description']
print(co_descp.head())
