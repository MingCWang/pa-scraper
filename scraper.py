from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

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


def student_emails():
    """This function will read the emails from the emails.txt file and return a list of emails"""
    with open("emails.txt", "r") as f:
        emails = f.readlines()
        emails = [email.strip() for email in emails]
    return emails


def scraper(driver, text_to_find, sleep_time=3):
    """This function is the actual scraper that will scrape the page and download the files"""
    emails = student_emails()
    downloaded_files = 0
    no_submissions = []
    try:
        # wait for the page to load, then locate the class 10A course and click
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//*[contains(text(), '233COSI-10A-2 : Introduction to Problem Solving in Python')]",
                )
            )
        ).click()
        # click on programming assignments

        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//a[.//span[text()='Programming Assignments (PAs)']]")
            )
        ).click()
        # click on the PA

        pa_container = driver.find_element(By.ID, "collapse-1")
        WebDriverWait(pa_container, 30).until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//a[.//span[text()='{text_to_find}']]")
            )
        ).click()
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[contains(text(), 'View all submissions')]")
            )
        ).click()
        # get the number of pages
        page_num = (
            len(
                driver.find_elements(
                    By.XPATH,
                    "//ul[contains(@class, 'mt-1') and contains(@class, 'pagination')]//li",
                )
            )
            - 2
        ) // 2
        for i in range(page_num):
            student_container = driver.find_element(
                By.CSS_SELECTOR,
                ".flexible.table.table-striped.table-hover.generaltable.generalbox tbody",
            )
            students = student_container.find_elements(
                By.CSS_SELECTOR, "tr.unselectedrow"
            )
            for student in students:
                student_email = student.find_element(By.CSS_SELECTOR, ".email").text
                if student_email not in emails:
                    continue
                else:
                    # if the email matches, download the zip file to the specified directory
                    try:
                        WebDriverWait(student, 5).until(
                            EC.element_to_be_clickable(
                                (
                                    By.XPATH,
                                    ".//td[contains(@class, 'c9')]//div[contains(@class, 'fileuploadsubmission')]//a",
                                )
                            )
                        ).click()
                        print(f"Downloading {student_email}'s submission")
                        time.sleep(sleep_time)
                        downloaded_files += 1
                    except Exception as e:
                        print(f"No submission from {student_email}")
                        no_submissions.append(student_email)
            if i != page_num - 1:
                nav = driver.find_elements(
                    By.XPATH,
                    "//nav[contains(@class, 'pagination') and contains(@class, 'pagination-centered') and contains(@class, 'justify-content-center')]",
                )
                nav = nav[1]
                page = WebDriverWait(nav, 10).until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            f"//ul[contains(@class, 'mt-1') and contains(@class, 'pagination')]//li[@data-page-number='{i + 2}']//a",
                        )
                    )
                )
                driver.execute_script("arguments[0].click();", page)

        input(
            "Press Enter to continue after all the files are downloaded to exit the tool..."
        )
        return downloaded_files, len(emails), no_submissions
    except Exception as e:
        print("Error: ", e)
        # print("Please complete the authentication process to proceed")


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

    # scrape the page
    submissions, students, no_submissions_list = scraper(driver, text_to_find)

    no_submissions = students - submissions

    print("\n==========================================\n")
    print(
        f"""Students: {students}
Submissions: {submissions}
No submissions: {no_submissions}
{no_submissions_list}
        """
    )
    print("==========================================\n")


if __name__ == "__main__":
    main()
