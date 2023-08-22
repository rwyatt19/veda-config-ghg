# Selenium UI Testing

This workflow is for UI testing the GHGC website using selenium. It works by deploying a local version of the site using yarn serve and performing UI checks against that locally hosted site.

# Usage

To use this workflow as part of a larger workflow, first update the ui_data.json file to include the following:

- A list of src links for logos you would like to check exist on the main page
- A list of catalog titles you would like to check exist on the catalogs page (Partial titles are OK)

Add the following to the github environment:
- The password required for sign in to the testing site (if required). Store as a secret with the name UI_PASSWORD

# Output

UI testing passes with a "Validation successful. All elements are present." message if all elements provided in the ui_data.json file are located.

If the test fails a PageValidationError will be triggered with the following returned values:

- Missing logos: A list of any logos that were unable to be located.
- Missing catalogs: A list of any catalogs from the .json file that were not found.
- Logos out of alignment: Indicates that the logos present on the page are out of horizontal alignment.
- Datasets are not appearing on analysis page: Indicates that datasets are not appearing after attempting to draw on the map and request them
- Map datasets are not being generated properly: Indicates that the map datasets appeared but are not being generated correctly after clicking the "Generate" button

In addition an artifact will be included with the run with the html and screenshots of pages that failed ui testing.