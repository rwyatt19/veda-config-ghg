import { test, expect } from '../pages/basePage';
const logos = JSON.parse(require('fs').readFileSync('e2e/testData.json', 'utf8'))['logos'];


test('load collaborator logos in header content of /home route', async ({
  page,
  homePage,
 }) => {
  await page.goto('/')
  await expect(homePage.mainContent, `home page should load`).toBeVisible();

  for (const logo of logos) {
    const img = homePage.headingContainer.getByAltText(`${logo} logo`);
    // images are lazy loaded. kick off loading
    await img.scrollIntoViewIfNeeded();
    await expect(img).toBeVisible();
};
});

    test('load collaborator logos in footer', async ({
      page,
      footerComponent,
     }) => {
      await page.goto('/')
      await expect(footerComponent.footer, `footer should load`).toBeVisible();

      for (const logo of logos) {
        const img = footerComponent.partners.getByAltText(`${logo} logo`);
        // images are lazy loaded. kick off loading
        await img.scrollIntoViewIfNeeded();
        await expect(img).toBeVisible();
    };
  });

  test('load collaborator logos in /about route', async ({
    page,
    aboutPage,
   }) => {
    await page.goto('/about')
    for (const logo of logos) {
      const img = aboutPage.mainContent.getByAltText(`${logo} logo`);
      // images are lazy loaded. kick off loading
      await img.scrollIntoViewIfNeeded();
      await expect(img).toBeVisible();
  };
});