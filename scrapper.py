import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def initialize(id, password, url):
    options = Options()
    options.add_argument('--headless=new')
    driver = webdriver.Chrome(options=options)

    driver.get(url)

    main_button = driver.find_elements(By.CSS_SELECTOR, 'a[role="button"]')[2]
    main_button.click()

    # filling login information, id-password
    driver.find_element(By.ID, 'tridField') .send_keys(id)
    driver.find_element(By.ID, 'egpField') .send_keys(password)

    # click button
    login_button = driver.find_element(By.CSS_SELECTOR, 'button[class="btn btn-send"]')
    login_button.click()
    
    # set grades page
    grades_url = url + 'not-gor'
    driver.get(grades_url)
    time.sleep(5)

    grade_table = driver.find_element(By.CSS_SELECTOR, 'div[data-ng-if="noteData"]')
    grade_columns = grade_table.find_element(By.CLASS_NAME, 'row').text.split('\n')[1:-2]
   
    course_table = []
    courses = grade_table.find_elements(By.CSS_SELECTOR, 'div[data-ng-repeat="tnotlarNote in birim.tnotlarNotes"]')
    
    for course in courses:
        values = course.find_elements(By.CSS_SELECTOR, 'p[class="ng-binding ng-scope"]')
        
        row = [value.text for value in values[1:-1]]
        course_table.append(row)

    return driver, course_table, grade_columns

def check(driver, course_table, grade_columns):
    driver.refresh()
    time.sleep(5)

    message = ""
    status = False

    grade_table = driver.find_element(By.CSS_SELECTOR, 'div[data-ng-if="noteData"]')
    courses = grade_table.find_elements(By.CSS_SELECTOR, 'div[data-ng-repeat="tnotlarNote in birim.tnotlarNotes"]')
    

    for i in range(len(courses)):
        values = courses[i].find_elements(By.CSS_SELECTOR, 'p[class="ng-binding ng-scope"]')
        row = [value.text for value in values[1:-1]]
        
        for j in range(len(row)):
            if course_table[i][j] != row[j]:
                course_table[i][j] = row[j]
                status = True

                message += f"{row[0]}\n\n"
                for k in range(1, len(row)):
                    if row[k] != "--" and row[k] != "":
                        message += f"{grade_columns[k]}: {row[k]}\n"
                message += "--------------------------\n\n"
    
    return message, status, course_table
