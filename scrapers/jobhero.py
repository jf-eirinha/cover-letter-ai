import pandas as pd
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from absl import flags
from absl import app

options = Options()
options.add_argument('start-maximized')
options.add_argument('disable-infobars')
options.add_argument('--disable-extensions')
options.add_argument('--lang=en-us')

FLAGS = flags.FLAGS
flags.DEFINE_string(
    'exe_path',
    'path/to/chromedriver_win32/chromedriver.exe', 'Path to Chrome Driver.')
flags.DEFINE_string(
    'url',
    'https://www.jobhero.com/sample-cover-letters/', 'URL'
 )

def main(argv):

    driver = webdriver.Chrome(options=options,
                    executable_path=FLAGS.exe_path)

    driver.get(FLAGS.url)

    time.sleep(5)

    def get_jobs():
        job_list = driver.find_elements_by_xpath(
            "//h2[@class='post-title']//a"
            )
        return job_list

    def read_text():

        letter_list = []

        try:
            try:
                text_div = driver.find_element_by_xpath(
                    "//p[contains(text(),'Dear ')]/parent::div | //div[contains(text(),'Dear ')]"
                    )

                letter = text_div.text
                
            except:
                text_div_elements = driver.find_elements_by_xpath(
                    '//article/p | //article/ul'
                )
                letter_start = False
                for element in text_div_elements:
                    str = element.text
                    letter_start = 'Dear ' in str
                    if letter_start:
                        letter_list.append(str)

                letter = ' '.join(letter_list)

            try:
                letter = letter.split(':',1)[1]
            except:
                letter = letter.split(',',1)[1]
            
            try:
                letter = letter.rsplit('Sincerely',1)[0]
            except:
                letter = letter.rsplit('Best Regards',1)[0]

        except:
            letter = 'Failed to download letter'
            download = False
    
        return letter

    job_list = get_jobs()
    letters = []

    for job in range(len(job_list)):
        download = True
        job_list = get_jobs()
        ActionChains(driver).move_to_element(job_list[job]).perform()
        job_list[job].click()
        letter = read_text()
        if download:
            letters.append(letter)
        driver.back()
        time.sleep(0.5)

    letters_df = pd.DataFrame(letters)
    letters_df.to_csv('jobhero.csv', index=False, header=False)

if __name__ == '__main__':
    app.run(main)
