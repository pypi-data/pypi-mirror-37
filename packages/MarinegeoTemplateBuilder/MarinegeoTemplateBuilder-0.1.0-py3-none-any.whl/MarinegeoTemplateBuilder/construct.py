#!/usr/bin/env python3
"""
Uses xlsxwriter to builds sheets from field and vocabulary templatebuilder class instances.
"""

import xlsxwriter
import pkg_resources
from MarinegeoTemplateBuilder import *
from MarinegeoTemplateBuilder.defaults import *
from MarinegeoTemplateBuilder.validators import *
from collections import defaultdict, OrderedDict


def addTabHeaderOnly(workbook, worksheetname, listoffields):
    """
    Generic function to create a new tab, fill out the header and add validation
    :param workbook: current xlsxwriter workbook
    :param worksheetname: name of the new tab
    :param listoffields: list of Field objects for the sheet to use to populate the header and add validation
    :return: worksheet object
    """
    tab = workbook.add_worksheet(worksheetname)  # creates the new worksheet tab
    tab.set_column(0, len(listoffields), colWidthDefault)  # set column widths to project default

    col = 0  # start the column counters

    # loop through each of the fields and write the fieldName in the header
    for s in listoffields:
        tab.write_string(0, col, s.fieldName, workbook.add_format(headerFormat))  # add to header
        s.add2schema()  # add field info for this field to schema list (used to write Schema tab)
        createValidation(tab, col, s)  # creates validation for the column

        # format number if field.formatString is defined
        if s.formatString is not None:
            fmt = workbook.add_format({'num_format': s.formatString})  # create new format class
            tab.set_column(col, col, colWidthDefault, fmt)  # add format to the entire column

        col += 1  # move to next column

    tab.freeze_panes(1, 0)  # freeze the top row

    return tab


def addSheets(workbook, listOfAllfields, tabsDict):
    """
    Loops through the list of Field classes and creates groupings based on the sheets. For each grouping, creates a new
    worksheet tab in the workbook and populates the header with the information form the Field instance.

    Sheets are added to the workbook in the order that they appear in the list of Fields.

    The function pulls the list of sheet names to add from the Field attributes. Then it loops through each target sheet
    name and subsets the field list to only the fields that should be included in the sheet. This subseted list is
    passed to the addTabHeaderOnly function as the listoffields.

    :param workbook: a xlsxwriter workbook object
    :param listOfAllfields: list of fields to create in the workbook (each field should be a Field class instance)
    :param tabsDict: dictionary of the existing worksheet tabs in the workbook
    :return: updated dictionary of the worksheet tabs in the workbook
    """
    # each sheet will need to be added separately so need to separate the list by the field's sheet variable
    # first get a list of unique sheets names from the list while preserving order

    sheets = [x.sheet for x in listOfAllfields]  # get all sheets to create from the list of Field
    sheetsOrdered = list(OrderedDict.fromkeys(sheets))  # unique sheet names while preserving order

    # create new sheets using the addTabHeaderOnly() function in a loop
    for s in sheetsOrdered:
        sub = [x for x in listOfAllfields if x.sheet == s]  # select items in the list that match the sheet name

        # workbook tabs are stored as a data dictionary with the tab name as the key
        tabsDict[s] = addTabHeaderOnly(workbook, s, listoffields=sub)

    return tabsDict


def checkOrCreateWS(workbook, worksheetname):
    """
    Checks to see if a named worksheet exists and then if it doesn't exist it creates it
    :param workbook: a xlsxwriter workbook object
    :param worksheetname:  name of the worksheet to check and/or create
    :return: xlsxwriter worksheet object
    """
    ws = workbook.get_worksheet_by_name(worksheetname)  # function returns the worksheet obj or none if doesn't exist
    if ws is None:
        ws = workbook.add_worksheet(worksheetname)  # add worksheet when it doesn't currently exist
    return ws


def schemaTab(workbook, fieldobjects2add=Field.schemaFields, hide=False):
    """
    Builds the schema tab using the items added to the schemaFields via add2schema() function
    :param workbook: current xlsxwriter object
    :param fieldobjects2add: the list of fields to write to the table
    :param hide: if true hides the tab from the user
    :return:
    """
    # create schema tab if it does not already exist
    ws = checkOrCreateWS(workbook, "Schema")

    header = ["sheet", "fieldName", "fieldDefinition", "fieldType", "formatString", "unit"]

    # Adjust the appearance
    ws.set_column(0, 2, 40)  # sets column width for first three columns
    ws.set_column(3, len(header), colWidthDefault)  # set the rest of the column widths to the default value
    ws.set_default_row(50)  # set the size of the row
    ws.freeze_panes(1, 0)  # freeze the top row to use as a frozen pane

    # write the header in the first row
    for col in range(len(header)):
        ws.write(0, col, header[col], workbook.add_format(headerFormat))

    # start from cells below headers
    row, col = 1, 0

    # loop through the field objects and write each to a row
    for s in fieldobjects2add:
        columns = [s.sheet, s.fieldName, s.fieldDefinition, s.fieldType, s.formatString, s.unit]
        for col in range(len(columns)):
            if columns[col] is not None:
                ws.write(row, col, columns[col], workbook.add_format({'text_wrap': True}))
        row += 1

    # hides the tab when hide is set to True
    if hide:
        ws.hide()
    return ws


def createVocabRange(workbook, vocab_objects=Vocab.vocabFields):
    """
    Builds equations Excel named ranges from the controlled vocabulary (named range will inherit the field name)
    :param workbook: the current xlsxwriter object
    :param vocab_objects: list of vocab controlled terms
    :return:
    """
    # https://stackoverflow.com/questions/6602172/how-to-group-a-list-of-tuples-objects-by-similar-index-attribute-in-python
    groups = defaultdict(list)
    for obj in vocab_objects:
        groups[obj.fieldName].append(obj)

    new_list = groups.values()  # pull the values from the groups to create new list

    start_row = 2  # start position for the first named range

    # loop through each grouping creating a named range
    for grouping in new_list:
        # named range is from the start of the grouping (start_row) to the end of the group (length minus one)
        workbook.define_name(grouping[0].fieldName, f'=Vocab!$B${start_row}:$B${start_row + len(grouping) -1}')
        start_row += len(
            grouping)  # add the length of the group to calculate the start position for the next group
    return


def vocabTab(workbook, vocabobjects2add=Vocab.vocabFields, hide=False):
    """
    Creates and populates the vocabulary tab when there are controlled vocabulary items
    :param workbook: the current xlsxwriter notebook object
    :param vocabobjects2add: the controlled vocabulary items to add and create named ranges
    :param hide: makes the tab hidden from the user
    :return:
    """
    ws = checkOrCreateWS(workbook, "Vocab")  # create vocab tab if it does not already exist
    header = ["fieldName", "code", "definition"]  # manual header items

    # sheet appearance
    ws.set_column(0, len(header), 40)  # Adjust the column width/heights.
    ws.set_column(2, 2, 100)  # Adjust the column width/heights.
    ws.freeze_panes(1, 0)  # freeze the top row

    row, col = 1, 0  # start from cell counter from the row below headers

    # write the cells for the manual header
    for col in range(len(header)):
        ws.write(0, col, header[col], workbook.add_format(headerFormat))

    # loop through the vocabulary objects and write to rows
    for s in vocabobjects2add:
        columns = [s.fieldName, s.code, s.definition]
        for col in range(len(columns)):
            if columns[col] is not None:
                ws.write(row, col, columns[col], workbook.add_format({'text_wrap': True}))
        row += 1

    # create named ranges from the vocab objects
    createVocabRange(workbook, vocabobjects2add)

    # hides the tab when hide is set to True
    if hide:
        ws.hide()

    return ws


def createMetadata(workbook, metadataLists=default_metadata, title="MarineGEO Data Template", imgpath=None, metadataValues=None):
    """
    Creates the metadata tab in the workbook
    :param workbook: the current xlsxwriter workbook object
    :param metadataLists: a list of metadata Field objects to fill.
    :param title: optional - changes the title for the worksheet
    :param imgpath: Optional path to a logo for the top of the sheet. DEFAULT inserts the MarineGEO logo.
    :param metadataValues: default metadata values to populate into the cells
    :return: the metadata tab worksheet object
    """
    tabMetadata = workbook.add_worksheet("Metadata")  # create a new worksheet

    # Adjust the column width/heights.
    tabMetadata.set_column(0, 0, 40)
    tabMetadata.set_column(1, 1, 100)
    tabMetadata.set_default_row(40)


    if imgpath == "DEFAULT":
        # insert the marineGEO branding logo
        filepath = pkg_resources.resource_filename(__name__, "marinegeo_branding.png")
        tabMetadata.insert_image(0, 1, filepath, {'x_scale': 4, 'y_scale': 4})
    elif imgpath is not None:
        # insert the custom logo
        tabMetadata.insert_image(0, 1, imgpath)


    # Write some info for the title
    tabMetadata.write('A3', title, workbook.add_format({'bold': 1, 'font_size': 18}))

    # start from cells below the title
    row, col = 3, 0


    # loop through all the metadata field objects and write name, default values and descriptions
    for metadataobj in metadataLists:

        # custom control of row heights
        if metadataobj.fieldName == "Abstract":
            # overwrite default row height
            tabMetadata.set_row(row, 80)

        if metadataobj.fieldName in ["AdditionalPeople", "DataEntryNotes"]:
            # overwrite default row height
            tabMetadata.set_row(row, 50)


        # write the first column
        tabMetadata.write(row, col, metadataobj.fieldName, workbook.add_format(metadataheaderFormat))


        # write the second colum
        # custom format for the date field
        if metadataobj.fieldName == "DataEntryDate":
            # set format to a date field
            # format number if field.formatString is defined
            if metadataobj.formatString is not None:
                fmt = workbook.add_format({'num_format': metadataobj.formatString, 'text_wrap': 1,
                                           'valign':'top', 'border': 1, 'font_size': 16})  # extend the metadataFormat
                tabMetadata.write_blank(row, col+1, '', fmt)  # add format to the entire column
                tabMetadata.data_validation(row, col+1, row, col+1, {'validate': 'date',
                 'criteria': 'greater than',
                 'minimum': datetime.date(1, 1, 1)})
        else:
            tabMetadata.write(row, col + 1, "", workbook.add_format(metadataFormat))

        # add the comment popup
        tabMetadata.write_comment(row, col+1, metadataobj.fieldDefinition, {'color': '#F3F315', 'font_size': 16})

        # write value if provided
        if metadataobj.fieldName in metadataValues.keys():
            # print(metadataobj.fieldName)
            # print(metadataValues[metadataobj.fieldName])
            tabMetadata.write(row, col + 1, metadataValues[metadataobj.fieldName], workbook.add_format(metadataFormat))

        row += 1  # next row

        # add metadata object to the schema list
        metadataobj.tab = "Metadata"
        metadataobj.add2schema()

    # format the blank cells to have a white background
    format0 = workbook.add_format({'bg_color': 'white'})
    tabMetadata.conditional_format('A1:Z2000', {'type': 'blanks', 'format': format0})

    return tabMetadata


# TODO seed values from a csv
# This likely will be an optional param in main in some fashion
# basically, we'll want to preload existing sites, taxonomic information, etc that previously been collected
#
# some psuedocode...
#
# def seedValue(targetSheet, seedValue):
#
#   find the targetSheet name in the dictionary of sheet tabs
#   then iterate over the seedValues starting at the row below the header?
#
#   this approach doesn't preserve the validation rule.... but does it matter?
#   It will be important that dates/time for example are properly encoded
#
#
#   return
#
#
# Another issue is how to allow the user to pass multiple objects to seed. It would be a common use case in order
# to build an completed example of a workbook template.
#
# Original example using Pandas
# # TODO add doc string
# def seedFromCSV(tab, csvfile, sortColumn = None, skipheader=True):
#     seedDF = pd.read_csv(csvfile) # load data as a pandas dataframe
#     seedDFnoNANs = seedDF.replace(np.nan, '', regex=True) # replaces all NaNs with empty strings
#
#     # sort column(s) alphabetically if provided
#     if sortColumn is not None:
#         seedDFnoNANs = seedDFnoNANs.sort_values(sortColumn).reset_index(drop=True) # reset the index
#
#     # iterate over the rows of the data frame writing the data into the tab
#
#     if skipheader:
#         pass
#     else:
#         tab.write_row(0, 0, list(seedDFnoNANs.columns.values))
#
#     for index, row in seedDFnoNANs.iterrows():
#         tab.write_row(index + 1, 0, row)
#
#     return
#
#
# seed={"Locations": "sites.csv", "Taxon": "fishPreviouslyFound.csv"}
#
# # interate over keys
# for s in seed.keys():
#     seedFromCsv(tabs[s], s.value??, sortColumn, skipheader?) # if items are loaded as a dict then won't be able to have
#     # features that sort or skipheader. Was this the only reason that Pandas is being used? if we can replace empty strings
#     # with null values it might be possible to just use the csv reader package. The advantage is that it would reduce the
#     # depandancy on the pandas external package.

def setTabColor(tabsDict):
    for key, value in tabsDict.items():
        value.set_tab_color(default_color)
    return


def main(output, fields, vocab=None, title="MarineGEO Data Entry Template", branding=None, protect=False, metadataValues=None):
    # creates empty workbook template
    workbook = xlsxwriter.Workbook(output)

    # workbook tabs are stored as a data dictionary with the tab name as the key
    tabs = dict()

    # load the desired fields and factor definitions
    attrib = load.loadfields(fields)

        
    tabs["Metadata"] = createMetadata(workbook, title=title, imgpath=branding, metadataValues=metadataValues)

    tabs = addSheets(workbook, listOfAllfields=attrib, tabsDict=tabs)

    if vocab is not None:
        vocab = load.loadvocab(vocab)
        tabs["Vocabulary"] = vocabTab(workbook, vocabobjects2add=vocab, hide=False)

    tabs["Schema"] = schemaTab(workbook, fieldobjects2add=Field.schemaFields, hide=False)

    if protect:
        if "Schema" in tabs:
            tabs["Schema"].protect()
        if "Vocabulary" in tabs:
            tabs["Vocabulary"].protect()

    setTabColor(tabs)

    workbook.close()

