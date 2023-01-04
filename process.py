import csv
import json
import hashlib
import random
import os

HKENGAGE_SRC = "hkengage.gov.hk.txt"
with open(HKENGAGE_SRC) as f:
    data = {}
    for line in f.readlines():
        if "\t" in line:
            u, c = line.strip().split("\t")
            ce = c.split("/")[0].strip()
            cc = c.split("/")[1].strip()
            if u != "大學名稱":
                if ce not in data:
                    data[ce] = {"cc": cc, "u": [u]}
                else:
                    data[ce]["u"].append(u)

IMMD_SRC = "immd.gov.hk.txt"
with open(IMMD_SRC) as f:
    for line in f.readlines():
        line = line.replace("U.S.A", "USA").replace("Britain", "UK").strip()
        flag = False
        this_cc = ""
        for ce in data:
            if ce in line:
                flag = True
                this_ce = ce

        if flag:
            if len(line.rsplit(this_ce, 1)) != 2:
                print(line.rsplit(this_ce, 1))
                # none

            if (
                line.rsplit(this_ce, 1)[0].strip().replace("The ", "")
                not in data[this_ce]["u"]
            ):
                print(line.rsplit(this_ce, 1)[0].strip().replace("The ", ""))

                # Special cases
                # University of Hong Kong / 香港大學
                # Chinese University of Hong Kong / 香港中文大學
                # The Hong Kong University of Science and Technology / 香港科技大學
                # Hong Kong Polytechnic University / 香港理工大學
                # Trinity College Dublin, The University of Dublin
                # King’s College London

RESULT = "result.tsv"
with open(RESULT, "w") as f:
    for ce in data:
        f.write(f'{data[ce]["cc"]}\t{ce}\t{len(data[ce]["u"])}\n')
        for u in data[ce]["u"]:
            f.write(f" \t{u}\t \n")
