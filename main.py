import csv

import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

CSV_PATH = "./prefectures.csv"
pref_list = set()

csv_input = pd.read_csv(filepath_or_buffer=CSV_PATH, encoding="utf-8", sep=",")

# make sorted prefecture list
pref_list = {d[4] for d in csv_input.values}
pref_list = sorted(pref_list)
print(len(pref_list))
print(pref_list)

for pref in pref_list:
    df = csv_input[(csv_input["prefectureNameE"].isin([pref]))]
    df.insert(0, "datetime", df["year"].astype(str) + "-" + df["month"].astype(str) + "-" + df["date"].astype(str))
    df.index = pd.to_datetime(df["datetime"])
    df["testedPositive_diff"] = df["testedPositive"].diff(1).fillna(0)
    df = df.copy()
    df.drop(columns=["prefectureNameJ", "prefectureNameE", "year", "month", "date", "datetime"], inplace=True)
    print(df.dtypes)
    print(df)

    df.to_csv(f"./output/{pref}.csv", index=False)

    plt.figure()
    df["testedPositive_diff"].plot()
    plt.savefig(f"./output/{pref}.png")
    plt.close("all")