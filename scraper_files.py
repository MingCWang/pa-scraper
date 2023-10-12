from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import asyncio


def student_emails():
    """This function will read the emails from the emails.txt file and return a list of emails"""
    with open("emails.txt", "r") as f:
        emails = f.readlines()
        emails = [email.strip() for email in emails]
    return emails


def get_student_files(page_num, driver, emails, sleep_time=0):
    """This function will download the files students who were assigned to the grader"""
    no_submissions = []
    downloaded_files = 0
    late_submission = []

    for i in range(page_num):
        student_container = driver.find_element(
            By.CSS_SELECTOR,
            ".flexible.table.table-striped.table-hover.generaltable.generalbox tbody",
        )
        students = student_container.find_elements(By.CSS_SELECTOR, "tr.unselectedrow")
        for student in students:
            student_email = student.find_element(By.CSS_SELECTOR, ".email").text
            if student_email not in emails:
                continue
            else:
                # if the email matches, download the zip file to the specified directory

                try:
                    WebDriverWait(student, 2).until(
                        EC.element_to_be_clickable(
                            (
                                By.XPATH,
                                ".//td[contains(@class, 'c9')]//div[contains(@class, 'fileuploadsubmission')]//a",
                            )
                        )
                    ).click()

                    print(f"Downloading {student_email}'s submission")
                    try:
                        element = WebDriverWait(student, 2).until(
                            EC.element_to_be_clickable(
                                (
                                    By.XPATH,
                                    ".//td[contains(@class, 'c4')]//div[contains(@class, 'latesubmission')]",
                                )
                            )
                        )
                        late = element.text
                        late_submission.append(f"{student_email}: {late}")
                    except:
                        pass
                    print(f"Downloading {student_email}'s submission")
                    # time.sleep(sleep_time)
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
            page = WebDriverWait(nav, 5).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        f"//ul[contains(@class, 'mt-1') and contains(@class, 'pagination')]//li[@data-page-number='{i + 2}']//a",
                    )
                )
            )
            driver.execute_script("arguments[0].click();", page)
    return downloaded_files, no_submissions, late_submission


async def scraper(driver, text_to_find, course, sleep_time=0):
    """This function is the actual scraper that will scrape the page and download the files"""
    emails = student_emails()
    try:
        # wait for the page to load, then locate the class 10A course and click
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    f"//*[contains(text(), '{course}')]",
                )
            )
        ).click()
        # click on programming assignments

        # WebDriverWait(driver, 30).until(
        #     EC.element_to_be_clickable(
        #         (By.XPATH, f"//a[.//span[text()='Programming Assignments (PAs)']]")
        #     )
        # ).click()
        # click on the PA

        # pa_container = driver.find_element(By.ID, "collapse-1")
        # WebDriverWait(pa_container, 30).until(
        #     EC.element_to_be_clickable(
        #         (By.XPATH, f"//a[.//span[text()='{text_to_find}']]")
        #     )
        # ).click()

        input("Press Enter to continue after you have clicked on the PA...")

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

        downloaded_files, no_submissions, late_submissions = get_student_files(
            page_num, driver, emails, sleep_time
        )

        input(
            "Press Enter to continue after all the files are downloaded to exit the tool..."
        )

        return downloaded_files, len(emails), no_submissions, late_submissions
    except Exception as e:
        print("Error: ", e)
