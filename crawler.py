#!/usr/bin/env python

import coloredlogs, logging
logger = logging.getLogger(__name__)
coloredlogs.install(logger=logger,
                    level='INFO',
                    fmt='%(asctime)s %(hostname)s %(name)s[%(process)d] %(levelname)s %(message)s')

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from pdb import set_trace as bp ##for testing
from selenium.common.exceptions import NoSuchElementException        

import re
import time
import csv
import os
import click
import sys
import csv

def check_exists_by_xpath(driver, xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True


def magic(str):
    i = str.find('$')
    j = str.find('USD')
    return str[i+1:j-1]


def do_stuff(driver, url):
    # On the city page
    logger.info('On the city page')
    driver.get(url)
    logger.info('City page opened!')
    time.sleep(5)
    element=driver.find_element_by_xpath('//*[@id="post"]')
    logger.info('Captured id=post element!')
    # Click on create post
    logger.info('Clicking on create post!')
    element.click()   
    logger.info('Clicked on create post!')
    time.sleep(3)

    logger.info('Getting first radio!')
    element = driver.find_elements_by_css_selector("input[type='radio']")[0]
    logger.info('Got first radio!')
    time.sleep(1)
    # Click on the first radio input
    logger.info('Clicking on first radio!')
    element.click()
    logger.info('Clicked on first radio!')

    while(True):
        logger.info('Checking for post page!')
        if check_exists_by_xpath(driver, ".//span[contains(text(), 'posting title')]"):
            logger.warn('Post page exists!')
            return ""
        logger.info('This is not a post page!')
        logger.info('Checking for price!')
        if check_exists_by_xpath(driver, '//span[@id="priceCalc"]'):
            logger.info('Price found!')
            text=driver.find_element_by_xpath('//span[@id="priceCalc"]').text
            print(text)
            time.sleep(1)
            return text
        else:
            logger.info('Price not found!')
            logger.info('Checking for radio existence!')
            if check_exists_by_xpath(driver, "//input[@type='radio']"):
                logger.info('Radio exists!')
                element = driver.find_elements_by_css_selector("input[type='radio']")[0]
                time.sleep(1)
                element.click()
                time.sleep(1)
            elif check_exists_by_xpath(driver, "//input[@type='checkbox']"):
                logger.info('Radio doesnt exists!')
                logger.info('Checking for checkboxes!')
                logger.info('')
                element = driver.find_elements_by_css_selector("input[type='checkbox']")[0]
                time.sleep(1)
                element.click()
                time.sleep(1)
                button = driver.find_elements_by_css_selector("input[type='submit']")[0]
                logger.info('Checkbox submitted!')
                time.sleep(1)
                button.click()
                time.sleep(1)


@click.command()
@click.option('--driver', '-d', 'driver_', required=True, type=click.Path(exists=True))
def run(driver_):
    """Simple spider to view emails."""

    # url="https://columbusga.craigslist.org/"
    # front="https://www.craigslist.org/about/sites"

    logger.info('Web Driver: %s.',os.path.expanduser(driver_))
    chrome_options = Options()
    # Uncomment line below if you dont want a window of chrome pop up.
    # chrome_options.add_argument('headless')
    driver = webdriver.Chrome(executable_path=os.path.realpath(driver_), chrome_options=chrome_options)

    with open('input_cities.txt', 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        writeFile = open('output.txt', 'w')
        writer = csv.writer(writeFile)
        for row in csv_reader:
            logger.warn(f'Processing {line_count + 1} line.')
            text = do_stuff(driver, row[0])
            price = "0.00"
            if text != "":
                price = magic(text)
            writer.writerow([row[0], price])
            writeFile.flush()
            logger.info(f'Iteration successfully finished for {line_count + 1} line.')
            line_count += 1
        logger.info(f'Processed {line_count} lines.')
        sys.exit()

if __name__ == "__main__":
    run()

