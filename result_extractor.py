from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from pandas import DataFrame
from io import StringIO
from os import getcwd
import sys


def extract_results(roll_no, semester_no):

    driver = webdriver.Firefox(executable_path=getcwd()+'\\geckodriver.exe')
    driver.get('https://makaut.ucanapply.com/smartexam/public/result-details')
    elem = driver.find_element_by_id("username")
    elem.send_keys(roll_no)
    select = Select(driver.find_element_by_id('semester'))
    select.select_by_value('SM' + semester_no)
    elem = driver.find_element_by_class_name('btn.btn-warning')
    elem.click()
    page_source = driver.page_source
    driver.quit()

    if 'Result under process!' not in page_source:
        soup = BeautifulSoup(page_source, "lxml")
        result = soup.findAll('tbody')
        personal_details = []
        for i in result[1].findAll('td'):
            personal_details.append(i.text.strip(' \xa0\n').replace('\xa0', ''))
        score_sheet = []
        for i in result[3].findAll('tr'):
            row = []
            for j in i.findAll('td'):
                row.append(j.text.strip(' \xa0\n').replace('\xa0', ''))
            score_sheet.append(row)
        score_sheet_df = DataFrame(score_sheet[1:], columns=score_sheet[0])
        stats = []
        for i in result[5].findAll('tr')[:-1]:
            stats.append(i.findAll('td')[0].text.strip(' \xa0\n').replace('\xa0', ''))
        mar = []
        for i in result[6].findAll('td'):
            mar.append(i.text.strip(' \xa0\n').replace('\xa0', ''))

        old_stdout = sys.stdout
        text_to_be_written = StringIO()
        sys.stdout = text_to_be_written
        print(*personal_details, sep='\n\n', end='\n\n')
        print(score_sheet_df.to_string(index=False), end='\n\n')
        print(*stats, sep='\n', end='\n\n')
        print(*mar)
        stdout = old_stdout
        
        with open(roll_no+'_'+semester_no+'.txt', 'w') as fp:
            fp.write(text_to_be_written.getvalue())

        return True

    return False


if __name__ == '__main__':

    roll_no = '11600116060'
    semester_no = '06'

    extract_results(roll_no, semester_code)
