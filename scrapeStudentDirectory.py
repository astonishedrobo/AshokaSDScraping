from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import time
import pwinput
import pandas as pd



def login(driver):
    inpEmail = input("Enter your email: ")
    email = driver.find_element(By.XPATH, "//*[@id='identifierId']")
    email.send_keys(inpEmail)
    nextButton = driver.find_element(By.XPATH, "//*[@id='identifierNext']/div/button")
    nextButton.click()
    if (driver.page_source.find("Enter your password")):
        print("Found your Google Account")
        inpPassword = pwinput.pwinput("Enter your password: ")
        password = driver.find_element(By.XPATH, "//*[@id='password']/div[1]/div/div[1]/input")
        WebDriverWait(driver, 10).until(lambda p: password.is_displayed())
        password.send_keys(inpPassword)
        nextButton = driver.find_element(By.CSS_SELECTOR, "#passwordNext > div > button")
        WebDriverWait(driver, 10).until(lambda p: nextButton.is_displayed())
        nextButton.click()


def searchDegreeSession(driver):
    degreeProgram = driver.find_element(By.CLASS_NAME, "select2-choice")
    degreeProgram.click()
    select = Select(driver.find_element(By.XPATH, "//*[@id='ddlDegreeProgramme']"))
    chosenProgram = "UG"
    chosenProgram = input("1.ASP\n2.UG\nEnter the degree program (default=UG): ")
    select.select_by_visible_text(chosenProgram)
    time.sleep(1)
    degreeSession = driver.find_element(By.ID, "s2id_ddlSession")
    degreeSession.click()
    writeYear = driver.find_element(By.ID, "s2id_autogen48_search")
    Chosenyear = input("Enter the year: ")
    writeYear.send_keys(Chosenyear)
    writeYear.send_keys(Keys.ENTER)
    driver.find_element(By.ID, "btnGet").click()

def captureData(driver, studentDF = pd.DataFrame()):
    dataBlocks = driver.find_elements(By.CLASS_NAME, "thumbnail")
    print("Total Student: ", len(dataBlocks))
    print("Scraping data...")
    for i in range(len(dataBlocks)):
        image = dataBlocks[i].find_element(By.TAG_NAME, "img")
        imageSrc = image.get_attribute("src")
        name = dataBlocks[i].find_element(By.TAG_NAME, "p").text
        name = name.splitlines()
        
        #save data to dataframe
        student = {"Name": name[1], "Ashoka ID": name[0], "Image": imageSrc}
        studentDF = pd.concat([studentDF, pd.DataFrame(student, index=[0])], ignore_index=True)
    
    #save data to excel
    studentDF.to_excel("studentData.xlsx", sheet_name= "studentDB", index=False)
    print("Data saved to studentData.xlsx")
    
    return studentDF



def main():
    driver = webdriver.Chrome()
    driver.get("https://ams.ashoka.edu.in/Contents/StudentDashboard.aspx")
    if (driver.page_source.find("Sign in")):
        login(driver)
    
    time.sleep(10)
    driver.get("https://ams.ashoka.edu.in/Contents/Masters/ViewstudentDirectory.aspx")
    searchDegreeSession(driver)
    time.sleep(5)
    studentDF = captureData(driver)
    time.sleep(10)
    driver.quit()

if __name__ == "__main__":
    main()