import pandas as pd
import os
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from absl import flags
from absl import app
import PyPDF2

options = Options()
options.add_argument('start-maximized')
options.add_argument('disable-infobars')
options.add_argument('--disable-extensions')
options.add_argument('--lang=en-us')

path = r'C:\path\to\pdf'

prefs = {'plugins.always_open_pdf_externally': True,
        'download.default_directory': path,
        'download.prompt_for_download': False,
        'download.directory_upgrade': True,
        'safebrowsing.enabled': False,
        'safebrowsing.disable_download_protection': True}
options.add_experimental_option('prefs', prefs)

FLAGS = flags.FLAGS
flags.DEFINE_string(
    'exe_path',
    'path/to/chromedriver_win32/chromedriver.exe', 'Path to Chrome Driver.')
flags.DEFINE_string(
    'url',
    'https://career.virginia.edu/resumes/writing-cover-letter/cover-letter-sample', 'URL'
 )

def main(argv):

    driver = webdriver.Chrome(options=options,
                    executable_path=FLAGS.exe_path)

    driver.get(FLAGS.url)

    time.sleep(5)

    def get_categories():
        category_list = driver.find_elements_by_xpath(
            "//a[@typeof='skos:Concept']"
            )
        return category_list

    def get_jobs():
        job_list = driver.find_elements_by_xpath(
        "//h2[@class='node-title']//a"
        )
        return job_list

    def enter_pdf():
        pdf_link = driver.find_element_by_xpath("//span[@class='file']//a")
        pdf_link.click()

    def read_text():

        pdf_list = os.listdir(path)
        letters = []

        for pdf in range(len(pdf_list)):

            pdf_path = os.path.join(path, pdf_list[pdf])
            file = open(pdf_path, 'rb')
            file_reader = PyPDF2.PdfFileReader(file)
            page = file_reader.getPage(0)
            letter = (page.extractText())
        
            letters.append(letter)

        return letters

    category_list = get_categories()

    for category in range(len(category_list)):
        
        category_list = get_categories()
        ActionChains(driver).move_to_element(category_list[category]).perform()
        category_list[category].click()
        time.sleep(0.5)
        job_list = get_jobs()

        for job in range(len(job_list)):

            job_list = get_jobs()
            ActionChains(driver).move_to_element(job_list[job]).perform()
            job_list[job].click()            
            enter_pdf()
            driver.back()
            time.sleep(0.5)

        driver.back()
        time.sleep(0.5)

    letters = read_text()
    letters_df = pd.DataFrame(letters)
    letters_df.to_csv('uni_virginia.csv', index=False, header=False)

if __name__ == '__main__':
    app.run(main)
