import pandas as pd
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
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
    'https://resumegenius.com/cover-letter-examples', 'URL'
 )

def main(argv):

    driver = webdriver.Chrome(options=options,
                    executable_path=FLAGS.exe_path)

    driver.get(FLAGS.url)

    time.sleep(5)

    def get_jobs():
        job_list = driver.find_elements_by_xpath(
            "//section[@class='examples-section examples-section-categories']//div[@class='entry-content']//a"
            )
        return job_list

    def read_text():
        text_element = driver.find_element_by_xpath(
            "//div[@class='entry-content example-section-content-inner']"
            )
        letter = text_element.text

        letter = letter.split('Dear',1)[1]

        try:
            letter = letter.split('],',1)[1]
        except:
            try:
                letter = letter.split('),',1)[1]
            except:
                download = False
        
        try:
            letter = letter.rsplit('Sincerely',1)[0]
        except:
            letter = letter.rsplit('Best Regards',1)[0]


        return letter

    job_list = get_jobs()
    letters = []

    for job in range(len(job_list)):
        download = True
        job_list = get_jobs()
        job_list[job].click()
        letter = read_text()
        if download:
            letters.append(letter)
        driver.back()
        time.sleep(1)

    letters_df = pd.DataFrame(letters)
    letters_df.to_csv('resume_genius.csv', index=False, header=False)

if __name__ == '__main__':
    app.run(main)
