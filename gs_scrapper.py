# -*- coding: utf-8 -*-
"""
Created on Mon Feb  28 23:15:28 2022
Author: Teenura
"""

from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
import time
import pandas as pd

def get_jobs(keyword, num_jobs, verbose, path):
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''
    
    #Initializing the webdriver
    options = webdriver.ChromeOptions()
    
    #Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    #options.add_argument('headless')
    
    #Change the path to where chromedriver is in your home folder.
    driver = webdriver.Chrome(executable_path=path, options=options)
    driver.set_window_size(1120, 1000)

    url = 'https://www.glassdoor.co.in/Job/india-data-analyst-jobs-SRCH_IL.0,5_IN115_KO6,18.htm'
    driver.get(url)
    jobs = []

    while len(jobs) < num_jobs:  #If true, should be still looking for new jobs.

        #Let the page load. Change this number based on your internet speed.
        #Or, wait until the webpage is loaded, instead of hardcoding it.
        time.sleep(15)

        #Test for the "Sign Up" prompt and get rid of it.
        try:
            driver.find_element_by_css_selector('[class="react-job-listing css-bkasv9 eigr9kq0"]').click()
            print('X1 WORKED')
        except ElementClickInterceptedException:
            print('x1 NOT worked')
            pass

        time.sleep(.1)

        try:
            driver.find_element_by_css_selector('[alt="Close"]').click()  #clicking to the X.
            print('x2 worked')
        except NoSuchElementException:
            print('x2 NOT worked')
            pass

        
        #Going through each job in this page
        job_buttons = driver.find_element_by_xpath("//ul[contains(@class, 'hover p-0  job-search-key')]")  #jl for Job Listing. These are the buttons we're going to click.
        print(job_buttons)
        for job_button in job_buttons.find_elements_by_xpath(".//*"):  

            print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
            if len(jobs) >= num_jobs:
                break

            job_button.click()  #You might 
            time.sleep(6)
            collected_successfully = False
            
            while not collected_successfully:
                try:
                    job_title = driver.find_element_by_xpath('.//div[contains(@class, "title")]').text    
                    location = driver.find_element_by_xpath('.//div[@class="location"]').text
                    job_description = driver.find_element_by_xpath('.//div[@class="jobDescriptionContent desc"]').text
                    collected_successfully = True
                    print('x2 worked')
                except:
                    time.sleep(5)
                    ('x2 NOT worked')

            try:
                salary_estimate = driver.find_element_by_xpath('.//span[@class="gray small salary"]').text
                print('x2 worked')
            except NoSuchElementException:
                salary_estimate = -1 #You need to set a "not found value. It's important."
                ('x2 NOT worked')
            
            try:
                rating = driver.find_element_by_xpath('.//span[@class="rating"]').text
                print('x2 worked')
            except NoSuchElementException:
                rating = -1 #You need to set a "not found value. It's important."
                ('x2 NOT worked')

            #Printing for debugging
            if verbose:
                print("Job Title: {}".format(job_title))
                print("Salary: {}".format(salary_estimate))
                print("Job Description: {}".format(job_description[:500]))
                print("Rating: {}".format(rating))
                print("Location: {}".format(location))

            #Going to the Company tab...
            #clicking on this:
            #<div class="tab" data-tab-type="overview"><span>Company</span></div>
            try:
                driver.find_element_by_xpath('.//div[@class="tab" and @data-tab-type="overview"]').click()
                print('x3 worked')


                try:
                    size = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Size"]//following-sibling::*').text
                    print('x5 worked')
                except NoSuchElementException:
                    size = -1
                    ('x2 NOT worked')

                try:
                    founded = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Founded"]//following-sibling::*').text
                    print('x6 worked')
                except NoSuchElementException:
                    founded = -1
                    ('x2 NOT worked')

                try:
                    type_of_ownership = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Type"]//following-sibling::*').text
                    print('x7 worked')
                except NoSuchElementException:
                    type_of_ownership = -1
                    ('x2 NOT worked')

                try:
                    industry = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Industry"]//following-sibling::*').text
                    print('x8 worked')
                except NoSuchElementException:
                    industry = -1
                    ('x2 NOT worked')

                try:
                    sector = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Sector"]//following-sibling::*').text
                    print('x9 worked')
                except NoSuchElementException:
                    sector = -1
                    ('x2 NOT worked')

                try:
                    revenue = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Revenue"]//following-sibling::*').text
                    print('x10 worked')
                except NoSuchElementException:
                    revenue = -1
                    ('x2 NOT worked')

                try:
                    easyapply = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Easy Apply"]//following-sibling::*').text
                    print('x11 worked')
                except NoSuchElementException:
                    easyapply = -1
                    ('x2 NOT worked')

            except NoSuchElementException:  #Rarely, some job postings do not have the "Company" tab.
                size = -1
                founded = -1
                type_of_ownership = -1
                industry = -1
                sector = -1
                revenue = -1
                ('x2 NOT worked')

                
            if verbose:
                print("Size: {}".format(size))
                print("Founded: {}".format(founded))
                print("Type of Ownership: {}".format(type_of_ownership))
                print("Industry: {}".format(industry))
                print("Sector: {}".format(sector))
                print("Revenue: {}".format(revenue))
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

            jobs.append({"Job Title" : job_title,
            "Salary" : salary_estimate,
            "Job Description" : job_description,
            "Rating" : rating,
            "Location" : location,
            "Size" : size,
            "Founded" : founded,
            "Type of ownership" : type_of_ownership,
            "Industry" : industry,
            "Sector" : sector,
            "Revenue" : revenue,
            "Easy Apply" : easyapply})
            #add job to jobs

        #Clicking on the "next page" button
        try:
            driver.find_element_by_xpath('.//li[@class="next"]//a').click()
            print('x12 worked')
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
            ('x2 NOT worked')
            break

    return pd.DataFrame(jobs)  #This line converts the dictionary object into a pandas DataFrame.

path="D:/DS_PROJECT_GLASSDOOR/Chromedriver_loc/chromedriver"

df=get_jobs('data analyst', 3000, False, path, 20)
df.to_csv('Glassdoor_scrapped_data.csv')