from MarinegeoTemplateBuilder.classes import Field

# default styles and formats
default_color = '#97C8EB'

headerFormat = {'bold': 1, 'bg_color': default_color, 'center_across': 1}
metadataheaderFormat = {'bold': 1, 'bg_color': default_color, 'text_wrap': 1,
                        'valign': 'vcenter', 'border': 1, 'font_size': 16}
metadataFormat = {'text_wrap': 1, 'valign':'vcenter', 'border': 1, 'font_size': 16, 'text_wrap': 1}
selectorFormat = {'bold': 1, 'bg_color': '#ccd9ff', 'center_across': 1}

# warning level for validation
warnLevel = 'warning'  # options ['stop', 'warning', 'information']

# default column width
colWidthDefault = 18

# default metadata fields
default_metadata = [
    Field(sheet="Metadata",
              fieldName='Title',
              fieldDefinition='Brief unique name describing location, type of data collected and dates'),
    Field(sheet="Metadata",
              fieldName='Abstract',
              fieldDefinition='Short description that contains details about what, why, how, when, and where '
                              'the data was collected'),
    Field(sheet="Metadata",
              fieldName='ContactPerson',
              fieldDefinition='Full name of data set creator (First Last). One person only.'),
    Field(sheet="Metadata",
              fieldName='EmailAddress',
              fieldDefinition='Email address for data set creator'),
    Field(sheet="Metadata",
              fieldName='People',
              fieldDefinition='Full names of all people that collected data. Separate multiple names with semicolons ('
                              'ie Person One; Person Two; Person Three)'),
    Field(sheet="Metadata",
              fieldName='DataEntryBy',
              fieldDefinition='Full name of person(s) entering data. Separate multiple names with semicolons.'),
    Field(sheet="Metadata",
              fieldName='DataEntryDate',
              fieldDefinition='Date the data was entered to this form. If data was entered over multiple days, please'
                              ' report the last date.',
              fieldType='date',
              formatString='YYYY-MM-DD'),
    Field(sheet="Metadata",
              fieldName='Notes',
              fieldDefinition='General notes about the project'),
    Field(sheet="Metadata",
              fieldName='ProtocolVersion',
              fieldDefinition='Protocol version number if applicable'),
    Field(sheet="Metadata",
              fieldName='TemplateVersion',
              fieldDefinition='Data template spreadsheet version')
]