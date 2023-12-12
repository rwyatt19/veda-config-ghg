import { test, expect } from '../pages/basePage';

const catalogs = JSON.parse(require('fs').readFileSync('e2e/testData.json', 'utf8'))['catalogs'];

test('load catalogs on /data-catalog route', async ({
  page,
  catalogPage,
 }) => {
  await page.goto('/data-catalog');
  await expect(catalogPage.header, `catalog page should load`).toHaveText(/data catalog/i);

  for (const item of catalogs) {
    const catalogCard = catalogPage.mainContent.getByRole('article') .filter({ hasText: item});
    await expect(catalogCard, `${item} catalog card should load`).toBeVisible();
  };
});


test.describe('catalog card routing', () => {
 for (const item of catalogs) {
  test(`${item} routes to dataset details page`, async({
    page,
    catalogPage,
    datasetPage,
  }) => {
    await page.goto('/data-catalog');
    await expect(catalogPage.header, `catalog page should load`).toHaveText(/data catalog/i);

    await catalogPage.mainContent.getByRole('article') .filter({ hasText: item}).click();
    await expect(datasetPage.header.filter({ hasText: item}), `${item} page should load`).toBeVisible();
  })
 }

});