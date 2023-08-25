import json
import os
import statistics
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
# options.add_experimental_option("detach", True)
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
driver.set_window_size(1920, 1080)
driver.implicitly_wait(3)

with open('ui_data.json') as json_file:
    data = json.load(json_file)

class PageValidationException(Exception):
    def __init__(self, custom_message=None):
        self.custom_message = custom_message

    def __str__(self):
        message = "UI validation failed:\n"

        if self.custom_message:
            message += self.custom_message + "\n"
        return message

def wait_for_clickable(element):
    return WebDriverWait(driver, 10).until(EC.element_to_be_clickable(element))

def password_input():
    try:
        password_input = driver.find_element(By.XPATH, '//input[@name="password"]')
        password_input.send_keys(ui_password)
        password_input.send_keys(Keys.ENTER)
    except NoSuchElementException as e:
        pass

def save_page(filename):
    output_dir = os.environ["OUTPUT_DIR"]
    os.makedirs(output_dir, exist_ok=True)

    html_path = os.path.join(output_dir, f"{filename}.html")
    html_source = driver.page_source
    with open(html_path, "w", encoding="utf-8") as file:
        file.write(html_source)

    screenshot_path = os.path.join(output_dir,f"{filename}_screenshot.png")
    original_size = driver.get_window_size()
    height = driver.execute_script("return document.body.parentNode.scrollHeight")
    driver.set_window_size(original_size['width'], height)
    url = driver.current_url
    driver.get(url)
    time.sleep(3)
    driver.save_screenshot(screenshot_path)

def logo_validation(dashboard_base_url):
    driver.get(dashboard_base_url)
    if ui_password:
        password_input()
    logo_src_list = data["logos"]
    missing_logos = []
    y_coordinates = []
    for src in logo_src_list:
        image_elements = driver.find_elements(By.XPATH, f"//img[contains(@src, '{src}')]")
        if not image_elements:
            missing_logos.append(src)
            encountered_errors.append(f"Missing logo: {src}")
            save_page("missing-logos")
        else:
            for image_element in image_elements:
                image_element_y = image_element.location['y']
                y_coordinates.append(image_element_y)
    mean_y = statistics.mean(y_coordinates)
    absolute_deviations = [abs(y - mean_y) for y in y_coordinates]
    mad = statistics.mean(absolute_deviations)
    if mad > 13:
        encountered_errors.append("Logos are out of alignment.")
        save_page("misaligned-logos")

def catalog_verification(dashboard_base_url):
    driver.get(f"{dashboard_base_url}/data-catalog")
    if ui_password:
        password_input()
    catalog_list = data["catalogs"]
    missing_catalogs = []
    for catalog in catalog_list:
        try:
            driver.find_element(By.XPATH, f'//h3[contains(text(), "{catalog}")]')
        except NoSuchElementException:
            missing_catalogs.append(catalog)
            encountered_errors.append(f"Missing catalog: {catalog}")
            save_page("missing-catalogs")

def dataset_verification(dashboard_base_url):
    driver.get(f"{dashboard_base_url}/analysis")
    if ui_password:
        password_input()
    map_canvas = driver.find_element(By.XPATH, '//canvas[@class="mapboxgl-canvas"]')
    corner_coordinates = [
        (-20, 20),
        (60, 20),
        (60, 60),
        (-20, 60)
    ]
    # time.sleep(3)
    actions = ActionChains(driver)
    wait_for_clickable(map_canvas)
    for x, y in corner_coordinates:
        actions.move_to_element_with_offset(map_canvas, x, y).click().perform()
    map_canvas.send_keys(Keys.ENTER)
    time.sleep(3)
    action_button = driver.find_element(By.XPATH, '//span[contains(text(), "Actions")]/following::button[contains(@class, "StyledButton")]')
    driver.execute_script("arguments[0].click();", action_button)
    driver.find_element(By.XPATH, '//li//button[contains(text(), "Last 10 years")]').click()
    while True:  # This creates an infinite loop that will keep trying until the condition is met
        try:
            data_set = driver.find_element(By.XPATH, '//*[contains(@class, "checkable__FormCheckableText")]')
            wait_for_clickable(data_set)
            driver.execute_script("arguments[0].scrollIntoView();", data_set)
            data_set.click()

            clicked_button = None
            try:
                clicked_button = driver.find_element(By.XPATH, '//a[contains(@variation, "achromic-outline")]')
            except NoSuchElementException:
                pass

            if clicked_button:
                break  # Exit the loop if the condition is met
        except NoSuchElementException:
            encountered_errors.append("Datasets are not appearing on the analysis page")
        save_page("missing-datasets")
    # time.sleep(3)
    generate_button = driver.find_element(By.XPATH, '//a[contains(@class, "Button__StyledButton") and contains(text(), "Generate")]')
    wait_for_clickable(generate_button)
    generate_button.click()
    try:
        WebDriverWait(driver, 30).until(
            EC.invisibility_of_element_located((By.XPATH, '//p[contains(text(), "loading") or contains(text(), "loaded")]'))
)
    except TimeoutException:
        save_page("missing-map-datasets")
        encountered_errors.append("Map datasets are not being generated properly")

# Retry loop
max_retries = 1
dashboard_base_url = os.getenv("DASHBOARD_BASE_URL").rstrip('/')
ui_password = os.getenv("PASSWORD")

for retry in range(max_retries):
    encountered_errors = []
    try:
        logo_validation(dashboard_base_url)
        catalog_verification(dashboard_base_url)
        dataset_verification(dashboard_base_url)
        if encountered_errors:
            error_message = "\n".join(encountered_errors)
            raise PageValidationException(custom_message=error_message)
        else:
            print("Validation successful!!! All elements found.")
            break
    except PageValidationException as e:
        if retry < max_retries - 1:
            continue
        else:
            raise e
