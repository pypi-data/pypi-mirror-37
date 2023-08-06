#!/usr/bin/env python3
"""
Validation rules
"""

from MarinegeoTemplateBuilder.construct import *
from MarinegeoTemplateBuilder.classes import Field
import datetime
import string


def validateList(field):
    """
    Validates items in a list. The items should be part of controlled vocabulary list which are Excel named ranges.
    The excel named range is set to be the same as the fieldName
    :param field: instance of the Field class
    :return: validator
    """
    validator = {'validate': 'list', 'error_type': warnLevel, 'source': f'={field.fieldName}'}
    return validator


def validateFkey(field, allFields=Field.schemaFields):
    """
    Validates items from another column in the worksheet. The other column must be defined in the lookup field. The
    lookup field should follow the pattern of Sheet$fieldName where sheet is the worksheet where the column is
    located and fieldName is the name of the field to pull. The dropDownfkey() function uses the list of
    fields in the workbook (from the schemaFields) to locate the appropriate sheet/column letter to use to build
    the equation.

    Important: the lookup column must be defined before the validation rule gets set on the column. For example, it
    won't work if you are trying to lookup a column (Habitat$geoform) before the habitat sheet is created because
    the fields that belong to that sheet are not yet added to schemaFields.

    :param field: instance of the Field class
    :param allFields: list of all fields in the workbook.
    :return: validator
    """
    fsheet, fkey = field.lookup.split("$")
    eq = dropDownfkey(allFields, fsheet, fkey)
    validator = {'validate': 'list', 'error_type': warnLevel, 'source': f'{eq}'}
    return validator


def validateDate(field=None):
    """
    Creates validation rule to check dates. Dates entered must be greater than 1/1/1900.
    :param field: None needed
    :return: validator
    """
    validator = {'validate': 'date',
                 'criteria': 'greater than',
                 'error_type': warnLevel,
                 'minimum': datetime.date(1, 1, 1)}
    return validator


def validateTime(field=None):
    """
    Creates a validation ruleset to check that times are valid. Times must be between 00:00 and 23:59.
    :param field: None need
    :return: validator
    """
    validator = {'validate': 'time', 'criteria': 'between', 'minimum': datetime.time(0, 0),
                 'error_type': warnLevel,
                 'maximum': datetime.time(23, 59, 59)}
    return validator


def validateGreaterThan(field):
    """
    Validation rule set to check that items entered into a column are greater or equal to the minimum value set
    for the field (field.minValue). Works for both integers and decimals.
    :param field: instance of the Field class
    :return: validator
    """
    validator = {'validate': field.fieldType,
                 'criteria': 'greater than or equal to',
                 'value': field.minValue,
                 'error_type': warnLevel,
                 'error_message': f'{field.fieldType.capitalize()} must be greater than {field.minValue}.'}
    return validator


def validateLessThan(field):
    """
    Validation rule set to check that items entered into a column are less or equal to the maximum value set
    for the field (field.maxValue). Works for both integers and decimals.
    :param field: instance of the Field class
    :return: validator
    """
    validator = {'validate': field.fieldType,
                 'criteria': 'less than or equal to',
                 'value': field.maxValue,
                 'error_type': warnLevel,
                 'error_message': f'{field.fieldType.capitalize()} must be less than {field.maxValue}.'}
    return validator


def validateBetween(field):
    """
    Validation rule set to check that items entered into a column are between the minimum and maximum values for a
    field. Works for both integers and decimals. Min and max bound are inclusive.
    :param field: instance of the Field class
    :return: validator
    """
    validator = {'validate': field.fieldType,
                 'criteria': 'between',
                 'minimum': field.minValue,
                 'maximum': field.maxValue,
                 'error_type': warnLevel,
                 'error_message': f'{field.fieldType.capitalize()} must be '
                                  f'between {field.minValue} and {field.maxValue}.'}
    return validator


def selectValidator(field):
    """
    Selects the correct validator function using the fieldType attribute of the given field. New validators should
    be defined as a function and added as an additional item to conditional in this function.
    :param field: instance of the Field class
    :return:
    """
    if field.fieldType == "string":
        pass
    elif field.fieldType == "list":
        return validateList(field)
    elif field.fieldType == "fkey":
        return validateFkey(field)
    elif field.fieldType == "date":
        return validateDate(field)
    elif field.fieldType == "integer" or field.fieldType == "decimal":
        if isfloat(field.minValue) and not isfloat(field.maxValue):
            return validateGreaterThan(field)
        elif not isfloat(field.minValue) and isfloat(field.maxValue):
            return validateLessThan(field)
        elif isfloat(field.minValue) & isfloat(field.minValue) & (float(field.minValue) < float(field.maxValue)):
            return validateBetween(field)
        else:
            pass
    else:
        raise ValueError(f"Unknown validator.... field type is {field.fieldType}")
    return


def foreignKeyLookup(listofFields, fsheet, fkey):
    """
    Hackish way to return the column letter from a list of fields for each sheet
    :param listofFields: list of all Field classes in workbook
    :param fsheet: the sheet name that will be connected
    :param fkey: the field name that will be connected with the foreign key
    :return: the column letter for the source of the foreign key
    """
    fattrib = [x.fieldName for x in listofFields if x.sheet == fsheet]  # filters field list by selected sheet
    position = fattrib.index(fkey)
    letter = string.ascii_uppercase[position]  # gets the column letter for the position
    return letter


def dropDownfkey(listofFields, fsheet, fkey):
    """
    Builds an excel validation equation for another column in the workbook
    :param listofFields: list of all Field classes in workbook
    :param fsheet: the sheet name that will be connected
    :param fkey: fkey: the field name that will be connected with the foreign key
    :return: excel validation formula
    """
    letter = foreignKeyLookup(listofFields, fsheet, fkey)  # grab the column letter
    # example of the equation that ignores first row =OFFSET(Location!$B:$B, 1, 0, ROWS(Location!$B:$B)-1)
    eq = f'=OFFSET({fsheet}!${letter}:${letter}, 1, 0, ROWS({fsheet}!${letter}:${letter})-1)'
    return eq


def createValidation(tab, col, field):
    """
    Applys the validation rule set to a set number of rows for the selected column (default is the first 20k rows)
    :param tab: the worksheet tab where the column is located
    :param col: the column number for the validation rule (zero indexed)
    :param field: instance of the Field class to build the validation rule set
    :return:
    """
    # define rows to apply validation rules
    row = 0  # start row
    maxValidatorRow = 20000  # max row to apply the validation rule

    validator = selectValidator(field)

    if validator is not None:
        tab.data_validation(row+1, col, maxValidatorRow, col, validator)
    return


def isfloat(value):
    """
    Checks if string can be converted to a flot
    :param value: string to check
    :return: boolean
    """""
    try:
        float(value)
        return True
    except ValueError:
        return False