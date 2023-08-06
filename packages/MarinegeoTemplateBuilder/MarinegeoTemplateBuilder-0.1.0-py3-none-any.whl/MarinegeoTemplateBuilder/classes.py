#!/usr/bin/env python3
"""
Template Builder Python Classes
"""

class Field:
    """
    Fields are the columns that are added to the workbook. Each field must have a destination (sheet), header
    name (fieldName), description (fieldDefinition) and the attribute type defined (fieldType).

    The allowed fieldType options are:
        string - general format cells with no restrictions.
        date - Excel date format with validation. Dates and times must have the formatString defined.
        list - Validation from another column in the spreadsheet. Source must be defined in the lookup variable.
        integer - validation of integers only. Maybe constrained using minValue and maxValue.
        decimal - validation of numbers. May be constrained using minValue and maxValue.

    Dates and times field types should have the date format defined as the formatString. Some examples include
    YYYY-MM-DD for dates and HH:MM for hours/minutes. See Excel Format Cells dialogue for help.

    List items should be loaded as Vocab instances.

    Integers and decimals fields can be limited to a certain range using the min and max values. The min and max values
    are inclusive.

    """
    # list of all the fields to write to the schema tab
    schemaFields = []

    def __init__(self, sheet, fieldName, fieldDefinition, fieldType="string", formatString=None,
                 lookup=None, unit=None, minValue=None, maxValue=None):
        self.sheet = sheet
        self.fieldName = fieldName
        self.fieldDefinition = fieldDefinition
        self.formatString = formatString
        self.lookup = lookup
        self.unit = unit
        self.fieldType = fieldType
        self.minValue = minValue
        self.maxValue = maxValue

    # function to add items to the working schemaFields list
    def add2schema(self):
        Field.schemaFields.append(self)

    @property
    def fieldtype(self):
        return self._fieldType

    # limits fieldType to predefined options only
    @fieldtype.setter
    def fieldtype(self, value):
        acceptableTypes = ['string', 'date', 'list', 'integer', 'decimal']
        if value not in acceptableTypes:
            raise ValueError(f"Unknown fieldType: {value}. Valid fieldType include {acceptableTypes}")
        self._fieldType = value


class Vocab:
    """
    Controlled vocabulary for fields. The controlled vocabulary is used for populating validation drop down menus.

    Each vocabulary term must have the destination field (fieldName) and the term/code itself (code). It is also
    best practice to include a definition for each code.
    """

    # list of all the Vocab terms to write to the vocab tab
    vocabFields = []

    def __init__(self, fieldName, code, definition):
        self.fieldName = fieldName
        self.code = code
        self.definition = definition

    def __repr__(self):
        return f'(name: {self.fieldName}, code: {self.code}, def: {self.definition})'

    def add2vocab(self):
        Vocab.vocabFields.append(self)

