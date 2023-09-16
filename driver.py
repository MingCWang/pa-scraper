from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def driver_configuaration(download_directory):
    """
    - This function will configure the Chrome WebDriver with the specified options
    - The WebDriver will be configured to download files to the specified directory
    """
    # Create Chrome options
    options = Options()
    # Optional: If running in a sandboxed environment
    options.add_argument("--no-sandbox")
    # Optional: If running in a Docker container
    options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--headless") uncomment this if you don't want the browser to pop up, it will instead run in the background
    prefs = {
        "profile.default_content_settings.popups": 0,
        "download.default_directory": download_directory,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
    }
    options.add_experimental_option("prefs", prefs)

    # Create a new Chrome WebDriver instance with the specified options
    driver = webdriver.Chrome(options=options)
    return driver
