#!/usr/bin/env python3
"""
Loads attribute fields and vocabulary from csv files into templatebuilder class instances.
"""

from csv import reader
from MarinegeoTemplateBuilder import classes


def loadfields(fields):
    if isinstance(fields, list):
        rows = fields
    elif fields.endswith('.csv'):
        rows = loadfieldsCSV(fields)
    else:
        raise ValueError("Unknown fields input type.")
    return rows



def loadfieldsCSV(csv):
    """
    Load attribute fields from a csv file
    :param csv: path to a csv file with the following fields -
        sheet, fieldName, fieldDefintion, fieldType, formatString, lookup, unit, minValue, maxValue
    :return: a list of instances of the templatebuilder Field class
    """
    headerItems = ['sheet', 'fieldName', 'fieldDefinition', 'fieldType', 'formatString',
                   'loopup', 'unit', 'minValue', 'maxValue']

    # http://dangoldin.com/2016/01/10/cleanest-way-to-read-a-csv-file-with-python/
    with open(csv, 'r', encoding='utf-8-sig') as f:
        r = reader(f, delimiter=',')
        header = next(r)  # skip header

        if header != headerItems:
            raise ValueError("Input file is not properly formatted. Unknown items in the header.")

        rows = [classes.Field(*l) for l in r]  # read in each row as an instance of the Field class
    return rows


def loadvocab(vocab):
    if isinstance(vocab, list):
        rows = vocab
    elif vocab.endswith('.csv'):
        rows = loadvocabCVS(vocab)
    else:
        raise ValueError("Unknown vocab input type.")
    return rows



def loadvocabCVS(csv):
    """
    Loads dropdown vocab definitions from a csv file
    :param csv: path to a csv file with fieldName, code, definition
    :return: a list of templatebuilder Vocab class instances
    """

    headerItems = ["fieldName", "code", "definition"]

    with open(csv, 'r', encoding='utf-8-sig') as f:
        r = reader(f, delimiter=',')
        header = next(r)  # skip header

        if header != headerItems:
            raise ValueError("Input file is not properly formatted. Unknown items in the header.")

        rows = [classes.Vocab(*l) for l in r]

    # add each of the vocabulary terms to the Vocab tab
    for i in rows:
        i.add2vocab()  # function is defined in the Vocab class

    return rows
