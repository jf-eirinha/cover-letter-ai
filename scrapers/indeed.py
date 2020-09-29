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
    'https://www.indeed.com/career-advice/cover-letter-samples', 'URL'
 )

def main(argv):

    driver = webdriver.Chrome(options=options,
                    executable_path=FLAGS.exe_path)

    driver.get(FLAGS.url)

    time.sleep(5)

    try:
        cookies = driver.find_element_by_xpath("//button[@class='tos-Button tos-Button-white']")
        cookies.click()
    except:
        pass
    
    def get_jobs():
        job_list = driver.find_elements_by_xpath("//a[@class='CoverLetter__GrayButton-ctLiBu kuIkJp']")
        return job_list

    def read_text():
        paragraphs = driver.find_elements_by_xpath('//div//p')
        for i in range(len(paragraphs)):
            p_text = paragraphs[i].text
            if p_text.startswith('Dear') or p_text.startswith ('To Whom It May Concern'):
                index_start = i
                del paragraphs[:i]
                break

        full_text_list = []
        for i in range(len(paragraphs)):
            p_text = paragraphs[i].text
            full_text_list.append(p_text)

        letter = ' '.join(full_text_list)

        try:
            letter = letter.split(':',1)[1]
        except:
            letter = letter.split(',',1)[1]
        
        try:
            letter = letter.rsplit('Sincerely',1)[0]
        except:
            letter = letter.rsplit('Best Regards',1)[0]

        return letter

    job_list = get_jobs()
    letters = []

    for job in range(len(job_list)):
        job_list = get_jobs()
        ActionChains(driver).move_to_element(job_list[job]).perform()
        job_list[job].click()
        letter = read_text()
        letters.append(letter)
        driver.back()
        time.sleep(1)

    letters_df = pd.DataFrame(letters)
    letters_df.to_csv('indeed.csv', index=False, header=False)

if __name__ == '__main__':
    app.run(main)
