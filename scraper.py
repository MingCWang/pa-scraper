from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from driver import driver_configuaration
from scraper_files import scraper
import time
import os


def authenticate(driver, username, password):
    """This function will fill out the authentication form with the given username and password"""
    try:
        form = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "f"))
        )
        username_input = form.find_element(By.NAME, "j_username")
        password_input = form.find_element(By.NAME, "j_password")
        username_input.send_keys(username)
        password_input.send_keys(password)
        driver.find_element(
            By.XPATH,
            '//div[@class="form-element-wrapper form-group form-group pull-right hidden-xs"]//button[@type="submit"]',
        ).click()
        print("Check your phone for DUO authentication. ")
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.ID, "trust-browser-button"))
        ).click()
    except Exception as e:
        print(e)


def main():
    # Specify the download directory
    download_directory = os.environ.get("DOWNLOAD_DIR")
    # Specify the programming assignmnt name
    text_to_find = os.environ.get("PA_NAME")
    # Get the value of an environment variable
    password = os.environ.get("PWD")
    username = os.environ.get("UNAME")

    driver = driver_configuaration(download_directory)
    driver.get("https://moodle2.brandeis.edu/my/")

    # fill out auth form
    authenticate(driver, username, password)
    start_time = time.time()
    # scrape the page
    submissions, students, no_submissions_list = scraper(driver, text_to_find)

    no_submissions = students - submissions
    end_time = time.time()
    duration = round(end_time - start_time, 1)
    print("\n==========================================\n")
    print(
        f"""Duration: {duration} seconds
Students: {students}
Submissions: {submissions}
No submission: {no_submissions}
No submission emails:
{no_submissions_list}
        """
    )
    print("==========================================\n")


if __name__ == "__main__":
    main()
