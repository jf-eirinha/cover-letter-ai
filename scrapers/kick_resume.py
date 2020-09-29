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
    'https://www.kickresume.com/en/help-center/all-cover-letter-samples/', 'URL'
 )

def main(argv):

    driver = webdriver.Chrome(options=options,
                    executable_path=FLAGS.exe_path)

    driver.get(FLAGS.url)

    time.sleep(5)
    
    accept_cookies =  driver.find_element_by_xpath(
                "//i[@class='ion-checkmark']"
                )
    accept_cookies.click()

    def load_all():

        clickaroo = True

        while(clickaroo):

            try:
                show_more =  driver.find_element_by_xpath(
                    "//a[@class='infinite-more-link']"
                    )
                ActionChains(driver).move_to_element(show_more).perform()
                time.sleep(2)
                
            except:
                clickaroo = False        

    def get_jobs():
        job_list = driver.find_elements_by_xpath(
            "//h3[@class='c-hc-content__sample-title']"
            )
        return job_list

    def read_text():
        frame = driver.find_element_by_xpath(
            "//iframe[@id='hc-preview-iframe']"
            )
        driver.switch_to.frame(frame)
        text_element = driver.find_element_by_xpath(
            "//div[@class='text-area rich-text-area']"
            )
        letter = text_element.text
        return letter

    load_all()
    job_list = get_jobs()
    letters = []

    for job in range(len(job_list)):
        load_all()
        job_list = get_jobs()
        ActionChains(driver).move_to_element(job_list[job]).perform()
        job_list[job].click()
        letter = read_text()
        letters.append(letter)
        driver.back()
        time.sleep(1)

    letters_df = pd.DataFrame(letters)
    letters_df.to_csv('kick_resume.csv', index=False, header=False)

if __name__ == '__main__':
    app.run(main)
