
# Copernicus Essential Climate Variables for assessing climate variability

This tool allows you to retrieve Copernicus **Essential Climate Variables** for assessing climate variability from the [Copernicus Climate Data Store](https://cds.climate.copernicus.eu/#!/home).

Copernicus ECV for assessing climate variability is available from the Copernicus portal at https://cds.climate.copernicus.eu/cdsapp#!/dataset/ecv-for-climate-change?tab=overview

To be able to retrieve data, you would need to register and get your [CDS API key](https://cds.climate.copernicus.eu/api-how-to).

The CDS API Key needs to be:
  - located in a file called `.cdsapirc`in the HOME area 
    (as defined the `HOME` environment variable).
  - or passed in an enviroment variable called `GALAXY_COPERNICUS_CDSAPIRC_KEY`. 
    When passed in `GALAXY_COPERNICUS_CDSAPIRC_KEY`, make sure the key does not
    contain the string `key: ` but the key itself only (starting with a number).
    The file `.cdsapirc` will then be created and placed in the HOME area (using
    HOME environment variable).
  - or use `GALAXY_COPERNICUS_CDSAPIRC_KEY_FILE` to specify where your key is stored
    on your system.
