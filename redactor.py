import sys
import glob
import numpy
import main
import spacy
import argparse
import os

names = ""
genders = ""
dates = ""
addresses = ""
phone = ""


input_list = []
input_list = sys.argv
input_path = []
output_path = ""
flags = []
stats_list = []


for i in range(len(input_list)):
    if input_list[i] == "--input":
        input_path.append(input_list[i + 1])

    elif input_list[i] == "--output":
        output_path = input_list[i + 1]

    elif input_list[i] == "--stats":
        stats_list.append(input_list[i + 1])

    elif input_list[i].startswith("--"):
        flags.append(input_list[i][2:])

del input_list[0]

input_files = glob.glob(input_list[1])

for file in range(len(input_files)):
    string_file = str(input_files[file])

    input_file = open(string_file, encoding="utf-8")

    data = input_file.read()
    names_list = []
    genders_list = []
    dates_list = []
    addresses_list = []
    phone_list = []

    if "names" in flags:
        names_list = main.redact_names(data)

    if "genders" in flags:
        genders_list = main.redact_genders(data)

    if "dates" in flags:
        dates_list = main.redact_dates(data)

    if "addresses" in flags:
        addresses_list = main.redact_address(data)

    if "phone" in flags:
        phone_list = main.redact_phones(data)

    data = main.redact_data(
        data, names_list, genders_list, dates_list, addresses_list, phone_list
    )

    redact_stats = main.stats(
        stats_list,
        string_file,
        names_list,
        genders_list,
        dates_list,
        addresses_list,
        phone_list,
    )

    file = "docs/stats.txt"
    with open(file, "a", encoding="utf-8") as file:
        file.write(redact_stats)
        file.close()

    output_file = string_file
    output_file = output_file + ".redacted"
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(data)
        file.close()
    new_loc = (output_path) + (output_file)
    os.rename(output_file, new_loc)
