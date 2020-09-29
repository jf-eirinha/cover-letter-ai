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
    'https://www.thebalancecareers.com/best-cover-letters-a-z-list-of-examples-2060172', 'URL'
 )

def main(argv):

    driver = webdriver.Chrome(options=options,
                    executable_path=FLAGS.exe_path)

    driver.get(FLAGS.url)

    time.sleep(5)

    cookies = driver.find_element_by_xpath(
                "//button[@id='gdpr-notification-banner__btn-close_1-0']"
                )
    cookies.click()

    def load_all():
        time.sleep(1)

        try:
            creading = driver.find_element_by_xpath(
            "//span[@class='btn-title']"
            )
            creading.click()
        except:
            pass

    def get_jobs():
        job_list = driver.find_elements_by_xpath(
            "//ul//li//a[@data-component='link']"
            )
        return job_list

    def read_text():
        text_element = driver.find_element_by_xpath(
            "//div[@id='mntl-sc-block-callout-body_1-0']"
            )
        letter = text_element.text
        return letter

    load_all()
    job_list = get_jobs()
    del job_list[-1]
    letters = []

    for job in range(len(job_list)):
        load_all()
        job_list = get_jobs()
        del job_list[-1]
        job_list[job].click()
        letter = read_text()
        letters.append(letter)
        driver.back()
        time.sleep(1)

    letters_df = pd.DataFrame(letters)
    letters_df.to_csv('thebalancecareers.csv', index=False, header=False)

if __name__ == '__main__':
    app.run(main)
