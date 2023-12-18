from selenium import webdriver
from selenium.common.exceptions import JavascriptException

from time import sleep, time
import random, pickle, config, math

TAB_NUM = 1  # tab number when a new search is opened
SEARCH_WINS = 0  # number of search wins achieved


class SB:
    """The SB object logs into Swagbucks and helps you automate poll answers and search wins."""

    def __init__(self, email: str, password: str,
                 driver: webdriver.Chrome = None):
        """Logs into Swagbucks with your email and password from config.py using Selenium.

        Parameters:
            email (str): Your login email in config.py for your Swagbucks account.
            password (str): Your login password in config.py for your Swagbucks account.
            driver: An optional pre-existing WebDriver instance.
        """
        if driver is None:
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            self.driver = webdriver.Chrome(options=options)
        else:
            self.driver = driver

        # Rest of your __init__ method...
        self.email = email
        self.password = password

    def poll(self):
        """Randomly selects a poll answer and submits your answer to earn 1 SB."""
        driver = self.driver
        driver.maximize_window()
        driver.get('https://www.swagbucks.com/polls')
        sleep(5)
        # complete the poll
        try:
            driver.execute_script(f"document.querySelectorAll('td.pollCheckbox')[{random.randint(0,1)}].click();")
            sleep(3)
            driver.execute_script("document.getElementById('btnVote').click()")
            print('Submitted answer for poll')
        except JavascriptException:
            print('Poll already completed')
        finally:
            sleep(5)

    def open_link_new_tab(self, url: str):
        """Opens URL in a new tab in chrome."""
        global TAB_NUM
        driver = self.driver
        driver.execute_script(f"window.open('{url}', 'Tab {TAB_NUM}')")
        # switch active window to the new tab
        driver.switch_to.window(driver.window_handles[TAB_NUM])
        TAB_NUM += 1

    def search(self):
        """Automates your searches and claims your search wins."""
        global SEARCH_WINS
        driver = self.driver
        driver.maximize_window()
        links = ['https://www.swagbucks.com/g/l/xcq6yq',
                 'https://www.swagbucks.com/g/l/6vyye1',
                 'https://www.swagbucks.com/g/l/p3btd7',
                 'https://www.swagbucks.com/g/l/1j26i4']

        # two search wins
        print(f'Begin search win #{SEARCH_WINS+1}')
        for url in (x for _ in range(10) for x in links):
            # end search if bot achieved two search wins
            if SEARCH_WINS == 2:
                break
            else:
                self.open_link_new_tab(url)
                sleep(16)
                # claims sb for search win (captcha?)
                self.claimSB()

    def tearDown(self):
        """Stops your Chrome session."""
        print('Finished running bot')
        self.driver.quit()

    def claimSB(self):
        """Submits form to claim SB."""
        global SEARCH_WINS
        driver = self.driver
        try:
            driver.execute_script("document.getElementById('claimSearchWinForm').submit()")
            sleep(10)
            print('Claimed SB')
            sleep(10)
            print(f'End search win #{SEARCH_WINS+1}')
            SEARCH_WINS += 1
            if SEARCH_WINS != 2:
                print(f'Begin search win #{SEARCH_WINS+1}')
        except JavascriptException:
            pass


def main():
    """Main function"""
    start = time()
    swag = SB(config.EMAIL, config.PASSWORD)
    swag.poll()
    swag.search()
    swag.tearDown()
    print(f'Bot ran for: {math.floor(int(time() - start) / 60)} minutes and {int(time() - start) % 60} seconds.')


if __name__ == '__main__':
    main()
