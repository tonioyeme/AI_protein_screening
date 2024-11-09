from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

# Initialize the WebDriver
driver = webdriver.Chrome(options=chrome_options)

# Interact with the page
driver.get("https://alphafoldserver.com")

# Set the directory containing the JSON files
input_folder = "/Users/toni/alpha_fold/batch_input"
files = [f for f in os.listdir(input_folder) if f.endswith('.json')]
wait = WebDriverWait(driver, 5)

for file_name in files:
    # Click on the "Upload JSON" button to open the dialog
    upload_json_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "upload-json-button")]')))
    upload_json_btn.click()

    # Locate the hidden file input and upload the file directly
    file_path = os.path.join(input_folder, file_name)
    file_input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@type="file" and @accept="application/JSON"]')))
    file_input.send_keys(file_path)  # This uploads the file without needing the OS file dialog

    # Click on the "Submit Job as Draft" button in the popup window
    submit_draft_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@class="confirm mdc-button mdc-button--unelevated mat-mdc-unelevated-button mat-primary mat-mdc-button-base dmat-mdc-button"]')))
    submit_draft_btn.click()

    time.sleep(2)  # Ensure each file has enough time to submit

# Close the browser after the loop
driver.quit()
