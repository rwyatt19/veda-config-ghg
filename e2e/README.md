# Playwright E2E Testing

This testing suite is for End to End testing the GHGC website via the UI using Playwright. It works by deploying a local version of the site using yarn serve and performing UI checks against that locally hosted site.

## Usage

Test data for this suite is handled in a fixture located in e2e/testFixture.ts  To use this suite after updating, first update the fixture file to include the following:

- A list of partner logos you would like to check render correctly
- A list of catalog titles you would like to check exist on the catalogs page (Partial titles are OK)

## Output

Playwright will generate an html report with test results.  This report will show all tests that were run, and will allow a user to view the results of any failed tests.

In addition an artifact will be included with the run with a trace including network calls and screenshots of the failed test run.
