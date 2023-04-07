import sys
import urllib
import numpy
import spacy
import re
import argparse
from commonregex import CommonRegex
import nltk

redact_with = "\u2588"


def redact_names(data):
    name = ""
    name_list = []
    words = nltk.word_tokenize(data)
    tags = nltk.pos_tag(words)
    name_chunk = nltk.ne_chunk(tags, binary=False)

    for sub in name_chunk.subtrees():
        if sub.label() == "PERSON":
            person_list = []
            for item in sub.leaves():
                person_list.append(item[0])
            name = " ".join(person_list)
            if name not in name_list:
                name_list.append(name)

    return name_list


def redact_genders(data):
    genders_list = [
        "He",
        "She",
        "he",
        "she",
        "him",
        "her",
        "himself",
        "herself",
        "his",
        "hers",
        "man",
        "woman",
        "male",
        "female",
        "men",
        "women",
        "mr.",
        "Mr.",
        "Mrs." "mrs.",
        "Mr",
        "mr",
        "Miss",
        "miss",
        "Ms",
        "ms",
        "Mrs",
        "mrs",
    ]

    return genders_list


def redact_dates(data):
    text = CommonRegex(data)
    dates_list = text.dates

    # print(dates_list)

    return dates_list


def redact_phones(data):
    text = CommonRegex(data)
    phone_list = text.phones

    # print(phone_list)

    return phone_list


def redact_address(data):
    location = ""
    location_list = []

    words = nltk.word_tokenize(data)
    tags = nltk.pos_tag(words)
    add_chunk = nltk.ne_chunk(tags, binary=False)

    for sub in add_chunk.subtrees():
        if sub.label() == "GPE":
            add_list = []
            for item in sub.leaves():
                add_list.append(item[0])
            location = " ".join(add_list)
            if location not in location_list:
                location_list.append(location)

    return location_list


def redact_data(data, names_list, genders_list, dates_list, addresses_list, phone_list):
    all = names_list + genders_list + dates_list + addresses_list + phone_list

    for item in all:
        length = len(item)
        item = r"\b" + item + r"\b"
        block = length * redact_with
        data = re.sub(item, block, data)

    return data


def stats(
    stats_list,
    string_file,
    names_list,
    genders_list,
    dates_list,
    addresses_list,
    phone_list,
):
    stats = ""
    statistics = stats_list[0]

    stats += "Redaction statistics for input file {}\n".format(string_file)
    stats += "\n"
    stats += "The following number of names are redacted: {} \n".format(len(names_list))
    stats += "The following number of dates are redacted: {} \n".format(len(dates_list))
    stats += "The following number of addresses are redacted: {} \n".format(
        len(addresses_list)
    )
    stats += "The following number of phone numbers are redacted: {} \n".format(
        len(phone_list)
    )
    stats += "The following number of genders are redacted: {} \n".format(
        len(genders_list)
    )
    stats += "\n"
    stats += "\n"

    if statistics == "stdout":
        file_path = "docs/stats.txt"
        with open(file_path, "a", encoding="utf-8") as file:
            file.write(stats)
            file.close()

    return stats
