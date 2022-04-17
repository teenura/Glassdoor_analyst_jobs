# Glassdoor_analyst_jobs

EDA Tableau Story: https://public.tableau.com/shared/GGXPHBP5N?:display_count=n&:origin=viz_share_link

Data analyst jobs for various locations in India has been scrapped using a selenium x-path based web scrapper from Glassdoor. 
This code is contained in the file gs_scrapper.py. 
The base code is taken from https://github.com/arapfaik/scraping-glassdoor-selenium and modified to allow scrapping from a modified Glassdoor webpage

Data_cleaning.py is used for:
1. parsing Salary to get upper and lower bounds
2. calculating age of the company
3. cleaning size and revenue data
4. parsing job description for skills required
5. vleaning location data
6. parsing job title to find categories and seniority
7. imputing missing salary values(independent variable) using average upper and lower salary over Location, Revenue, Size

Model_gs.py is used for:
1. Replacing all missing values of dpendent variables using mode of that variable
2. running linear regression to get a root mean square error of the order 10^29
3. regularising linear regression by lasso and varying weights of regularisation to get best rms error of      1.93
4. using Random Forest to get rms error of 1.95 and tuning hyperparameters using GridSearchCV to get best fit and lowest rms error of 1.90
5. storing the model using pickle
