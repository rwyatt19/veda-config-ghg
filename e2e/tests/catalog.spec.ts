import { test, expect } from '../pages/basePage';

test('load catalogs on /data-catalog route', async ({
  page,
  catalogPage,
  catalogs,
 }) => {
  await page.goto('/data-catalog');
  await expect(catalogPage.header, `catalog page should load`).toHaveText(/data catalog/i);

  for (const item of catalogs) {
    const catalogCard = catalogPage.mainContent.getByRole('article') .filter({ hasText: item});
    await expect(catalogCard, `${item} catalog card should load`).toBeVisible();
  };
});


test('clicking catalog cards routes to dataset details page', async ({
  page,
  catalogPage,
  catalogs,
  datasetPage,
 }) => {

  // this test takes longer due to all of the page loads
  test.setTimeout(180000);
  for (const item of catalogs) {
    await page.goto('/data-catalog');
    await expect(catalogPage.header, `catalog page should load`).toHaveText(/data catalog/i);

    await catalogPage.mainContent.getByRole('article') .filter({ hasText: item}).click();
    await expect(datasetPage.header.filter({ hasText: item}), `${item} page should load`).toBeVisible();
  };
});