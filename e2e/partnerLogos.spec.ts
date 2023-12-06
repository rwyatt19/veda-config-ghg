import { test, expect } from './pages/basePage';

test('load collaborator logos in main content of /home route', async ({
  page,
  homePage,
  logos,
 }) => {
  await page.goto('/')
  await expect(homePage.mainContent, `home page should load`).toBeVisible();

  for (const logo of logos) {
    const img = homePage.mainContent.getByAltText(`${logo} logo`);
    // images are lazy loaded. kick off loading
    await img.scrollIntoViewIfNeeded();
    await expect(img).toBeVisible();
};
});

    test('load collaborator logos in footer', async ({
      page,
      footerComponent,
      logos,
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
    logos,
   }) => {
    await page.goto('/about')
    for (const logo of logos) {
      const img = aboutPage.mainContent.getByAltText(`${logo} logo`);
      // images are lazy loaded. kick off loading
      await img.scrollIntoViewIfNeeded();
      await expect(img).toBeVisible();
  };
});