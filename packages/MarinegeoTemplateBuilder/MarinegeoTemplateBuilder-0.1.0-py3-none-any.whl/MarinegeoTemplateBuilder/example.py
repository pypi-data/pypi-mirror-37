import MarinegeoTemplateBuilder

# Exampe of create an Excel template using the MarinegeoTemplate Builder

from MarinegeoTemplateBuilder import *

metadataValues = {"TemplateVersion": "v0.0.1",
                  "ProtocolVersion": "v0.0.1",
                  "Title": "Test Template"}




main('TestTemplate_v0.0.1.xlsx',
           'attributes_v0.0.1.csv',
           'factor_v0.0.1.csv',
           "Test Template",
           'DEFAULT', protect=True, metadataValues=metadataValues)
