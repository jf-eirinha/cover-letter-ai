import pandas as pd
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
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
    'https://www.monster.com/career-advice/article/cover-letters', 'URL'
 )

def main(argv):

    driver = webdriver.Chrome(options=options,
                    executable_path=FLAGS.exe_path)

    driver.get(FLAGS.url)

    time.sleep(5)

    cookies = driver.find_element_by_xpath("//button[@id='widget-popup-close-icon']")
    cookies.click()

    def get_jobs():
        
        job_list = driver.find_elements_by_xpath("//div[@class='niche-content article-top']//ul//li//a")
        return job_list

    def read_text( url ):

        driver.get(url)
        time.sleep(2)
        driver.switch_to.window(driver.window_handles[1])
        
        text_element = driver.find_element_by_xpath('//article')

        letter = text_element.text
        letter = letter.split('Dear', 1)[1]
        letter = letter.split(':',1)[1]
        letter = letter.rsplit('Sincerely',1)[0]
        
        return letter

    job_list = get_jobs()
    letters = []
    default_handle = driver.current_window_handle

    for job in range(len(job_list)):
        
        job_list = get_jobs()
        url = job_list[job].get_attribute('href')
        letter = read_text(url)
        letters.append(letter)
        driver.get(FLAGS.url)
        time.sleep(1)
        driver.switch_to.window(default_handle)

    letters_df = pd.DataFrame(letters)
    letters_df.to_csv('monster.csv', index=False, header=False)

if __name__ == '__main__':
    app.run(main)
