# Playwright E2E Testing

This testing suite is for End to End testing the GHGC website via the UI using Playwright. It works by deploying a local version of the site using yarn serve and performing UI checks against that locally hosted site.

## Directory Structure

The end to end tests are organized in the `/e2e` directory. The tests have been written following a [Page Object Model](https://martinfowler.com/bliki/PageObject.html) pattern.
Supporting files within the repo are in the following structure:

```text
/e2e
   │
   │─── README.md
   │─── playwright.config.ts - imports our global setup, defines preferred browsers, & number of retries
   │─── testFixture.ts - contains all project specific test data such as expected logos and catalogs
   │─── uiDataTypes.d.ts - contains typings for items in the testFixture.ts file
   └─── /pages
   │      └─── basePage.ts - imports all seeded data and PageObjects into our `test` object.
   │      │
   │      └─── [PAGENAME]Page.ts - The page objects. UI elements interacted with on a page are defined once to keep tests DRY and minimize test changes if layout changes.
   └─── tests - our actual tests
```

## Usage

Test data for this suite is handled in a fixture located in e2e/testFixture.ts  To use this suite after updating, first update the fixture file to include the following:

- A list of partner logos you would like to check render correctly
- A list of catalog titles you would like to check exist on the catalogs page (Partial titles are OK)

## Updating Tests

If the layout of a page changes, then the tests may no longer be able to interact with locators. These locators are defined in the Page Objects defined in `/e2e/pages`. The Playwright framewok provides multiple ways to choose elements to interact with.  The recomended ones are defined in the [Playwright documentation](https://playwright.dev/docs/locators#quick-guide).

Any new pages will need to have new page objects created and then imported into the `basePage.ts` file following th format of existing pages.  This allows all tests to reference the page.

## Output

Playwright will generate an html report with test results.  This report will show all tests that were run, and will allow a user to view the results of any failed tests.

In addition an artifact will be included with the run with a trace including network calls and screenshots of the failed test run.

