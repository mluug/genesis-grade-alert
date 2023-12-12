from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import user_defined


def grades_extracted_reformat(grades):
    lines = grades.strip().split('\n')

    formatted_result = []
    for i in range(0, len(lines), 4):
        course = lines[i + 2].strip()
        grade = lines[i].strip()
        formatted_result.append(f'{course}, {grade}')

    return formatted_result


def crawl_grades():
    driver = webdriver.Chrome()

    driver.get('https://parents.mtps.com:443/moorestown/')

    username_field = driver.find_element(By.ID, 'j_username')
    password_field = driver.find_element(By.ID, 'j_password')

    username_field.send_keys(user_defined.username())
    password_field.send_keys(user_defined.password())

    password_field.send_keys(Keys.RETURN)

    # WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//p[@class="sectionTitle"]')))

    # hamburger = driver.find_element(By.XPATH, '//div[@id="hamburgerIcon"]')
    # hamburger.click()

    # gradebook = driver.find_element(By.XPATH, '//div[contains(text(),"Gradebook")]')
    # gradebook.click()

    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.itemContainer')))
    grade_container = driver.find_element(By.CSS_SELECTOR, '.itemContainer')

    grades = grade_container.text

    driver.quit()

    return grades
