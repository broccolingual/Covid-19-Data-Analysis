import csv
import datetime
import math
import sys
import time

import pandas as pd
import pytz
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

CSV_PATH = "./prefectures.csv"
pref_list = set()

csv_input = pd.read_csv(filepath_or_buffer=CSV_PATH, encoding="utf-8", sep=",")

def main(days=30):
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
        # print(df.dtypes)
        print(df)

        df.to_csv(f"./output/{pref}.csv")

        del df["testedPositive"], df["peopleTested"], df["hospitalized"], df["discharged"], df["deaths"]

        tokyo = pytz.timezone("Asia/Tokyo")
        tokyo_datetime_now = tokyo.localize(datetime.datetime.now())
        tokyo_datetime_past = datetime.timedelta(days=days)
        df = df[((tokyo_datetime_now - tokyo_datetime_past).strftime("%Y-%m-%d") <= df.index) & (df.index <= tokyo_datetime_now.strftime("%Y-%m-%d"))]

        # plot
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax = df.plot(y=["testedPositive_diff"], label=["TestedPositive"], style=["-", "-"], figsize=(10, 4))
        ax = df.plot(secondary_y=["effectiveReproductionNumber"], label=["Effective Reproduction Number"], style=["-", "-"], figsize=(10, 4))
        
        # view settings
        desc = df.describe()
        # ax.set_ylim(math.floor(desc["testedPositive_diff"]["min"]) - 1, math.ceil(desc["testedPositive_diff"]["max"]) + 1)
        # ax.right_ax.set_ylim(math.floor(desc["effectiveReproductionNumber"]["min"]) - 1, math.ceil(desc["effectiveReproductionNumber"]["max"]) + 1)

        # grid settings
        ax.grid(True, linestyle=':')

        # label settings
        plt.title(pref)
        ax.set_ylabel("Tested Positive")
        ax.right_ax.set_ylabel("Effective Reproduction Number", rotation=-90)
        ax.set_xlabel("Date")
        ax.right_ax.yaxis.set_label_coords(1.06, 0.5)

        plt.tight_layout() 
        plt.savefig(f"./output/{pref}.png")
        plt.close("all")

if __name__ == "__main__":
    # period settings
    days = 30
    if len(sys.argv) == 2:
        days = int(sys.argv[1])

    start = time.time()
    main(days=days)
    end = time.time()
    print("\nElapsed Time: {:.2f}s".format(end-start))