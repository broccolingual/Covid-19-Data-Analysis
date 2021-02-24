import csv
import math

import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

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
    df["testedPositive_diff"] = df["testedPositive"].diff(1).dropna()
    df = df.copy()
    df.drop(columns=["prefectureNameJ", "prefectureNameE", "year", "month", "date", "datetime"], inplace=True)
    print(df.dtypes)
    print(df)

    df.to_csv(f"./output/{pref}.csv")

    del df["testedPositive"], df["peopleTested"], df["hospitalized"], df["discharged"], df["deaths"]

    df = df[("2021/1/24" <= df.index) & (df.index <= "2021/2/24")]

    plt.figure()
    ax = df.plot(secondary_y=["effectiveReproductionNumber",], style=["-", "-"], grid=False, mark_right=False, figsize=(12, 4))
    
    # view settings
    desc = df.describe()
    ax.set_ylim(math.floor(desc["testedPositive_diff"]["min"]) - 1, math.ceil(desc["testedPositive_diff"]["max"]) + 1)
    # ax.right_ax.set_ylim(math.floor(desc["effectiveReproductionNumber"]["min"]) - 1, math.ceil(desc["effectiveReproductionNumber"]["max"]) + 1)

    # grid settings
    ax.grid(True, linestyle=':')

    # label settings
    plt.title(pref)
    ax.set_ylabel("Tested Positive")
    ax.right_ax.set_ylabel("Effective Reproduction Number")
    ax.set_xlabel("Date")

    plt.savefig(f"./output/{pref}.png")
    plt.close("all")
