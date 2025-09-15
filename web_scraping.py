import requests 
import pandas as pd
import re 
from bs4 import BeautifulSoup

# Step 1: Website you are getting the data from.
url = "https://web.archive.org/web/20230902185326/https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29"
# Step 2: Make the get request to the website, use the .text to extract the content page.
page_content = requests.get(url).text
# Step 3 Create a soup Element using the BeautifulSoup Class
soup = BeautifulSoup(page_content,'html.parser')
# Step 4 Find the target table using soup object and pass the value as string: 'table' and class_ 'table class if case it has one'
target_table = soup.find('table', class_='wikitable')


# Step 4 If you table has any colspan 2, this will cause data inconsistency, so delete the class from the entire table.
for td_tag in target_table.find_all('td'): # Combining two columns happens in the table data(td), Create a for loop that finds all the td tags.
    for child_tag in td_tag.find_all('sup'): # Going through every td_tag en 
        child_tag.decompose() # Remove from the tree the descendent childre of the tag.
target_table.prettify() # We use prettify 

target_table_tbody = target_table.find('tbody')  # Working only with the table body
data = [] # variable when the row information will be saved.
for row in target_table_tbody.find_all('tr'): # this loop is to go over every row.
    row_data = [] # Temporary variable that will save the current value.
    for cell in row.find_all(['td']): # Going over each cell in each row
        colspan = int(cell.get('colspan',1)) # get colspan value, if not specified 
        row_data.append(cell.get_text(strip=True))# add the value of each cell to the row
        for _ in range(colspan - 1): # going over every value that has colspan
           row_data.append('') # assigning empty value
    data.append(row_data)

data_cleaned = []
for row in data:
    clean_data_row = []
    for cell in row:
        if cell != '—':
            clean_data_row.append(cell)
        else:
            clean_data_row.append('')
    data_cleaned.append(clean_data_row)

filterList = list(filter(None,data_cleaned))
header =['Country/Terretory','UN Region','Estimate1','Year1','Estimate2','Year2','Estimate3','Year3']

df = pd.DataFrame(filterList,columns=header)
print(df)
df.to_csv('./Countries.csv')
