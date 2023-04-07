import pytest
import main

data = "My name is John Smith and I live in Colorado. I was born on July 4, 1989. My phone number is (281)-330-8004. My best friends name is Peyton Manning and he was born on November 20, 1970."
names = ['John Smith', 'Peyton Manning']
genders = ['he']
dates = ['July 4, 1989', 'November 20, 1970']
phone = ['(281)-330-8004']
location = ['Colorado']

def test_names():
    names_list = main.redact_names(data)

    assert len(names_list) == 2


def test_genders():
    genders_list = main.redact_genders(data)

    if len(genders_list) == 27:
        assert True
    else:
        assert False


def test_dates():
    dates_list = main.redact_dates(data)

    assert len(dates_list) == 2


def test_phones():
    phone_list = main.redact_phones(data)

    assert len(phone_list) == 1


def test_addresses():
    location_list = main.redact_address(data)

    assert len(location_list) == 1


def test_redaction():
    test_data = main.redact_data(data, names, genders, dates, phone, location)

    for i in test_data:
        if i == '\u2588':
            assert True

def test_statistics():
    stats_list = 'stdout'

    stats = main.stats(stats_list,data, names, genders, dates, phone, location)

    if stats != " ":
        assert True
    else:
        assert False
