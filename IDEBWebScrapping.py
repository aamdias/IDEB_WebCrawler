# Usefull libraries
from selenium import webdriver
from selenium.webdriver.support import ui
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

# Auxiliatory functions
def page_is_loaded(driver):
    return driver.find_element_by_tag_name('body') != None

# Instanciating Selenium Web browser
driver = webdriver.Chrome('/Users/alandias/Files/Spotted/chromedriver')

# Openning 
driver.get('http://ideb.inep.gov.br/resultado/')
wait = ui.WebDriverWait(driver,10)
wait.until(page_is_loaded)

# Switching to iframe tag
frame = driver.find_element_by_tag_name('iframe')
driver.switch_to.frame(frame)

# Getting radio elem
escola_radio_butoon = driver.find_element_by_id('regiaoDecorate:regiaoRadio:3')

# Clicking
escola_radio_butoon.click()

# Wait for loading
time.sleep(2)

# Getting elements of the form

# Filling "UF"
uf = 'SP'
UF_field = driver.find_element_by_id('uf3Decorate:uf3Select')
for option in UF_field.find_elements_by_tag_name('option'):
    if option.text == uf:
        option.click()
        break

# Wait for loading
time.sleep(2)

# Filling "Município"
city = 'SÃO PAULO'
Municipio_field = driver.find_element_by_id('municipio3Decorate:municipio3Select')
for option in Municipio_field.find_elements_by_tag_name('option'):
    if option.text == city:
        option.click()
        break

# Wait for loading
time.sleep(2)

# Filing "Dependência Administrativa"
adm_dep = 'Municipal'
DepAdmin_field = driver.find_element_by_id('redeDependencia2Decorate:redeDependencia2Select')
for option in DepAdmin_field.find_elements_by_tag_name('option'):
    if option.text == adm_dep:
        option.click()
        break

# Filling "Escola"
escola_field = driver.find_element_by_id('escolasDecorate:escolasSelect')
for option in escola_field.find_elements_by_tag_name('option'):
    if option.text == 'Todas':
        option.click() 
        break

# Filling "Série/Ano"
Serie_field = driver.find_element_by_id('serieAnoDecorate:serieAnoSelect')
for option in Serie_field.find_elements_by_tag_name('option'):
    if option.text == 'Todas':
        option.click() 
        break

# Wait for loading
time.sleep(2)

# Finish form. Press "Pesquisar"
search_button = driver.find_element_by_xpath("//span[@id='botoesDecorate']//center//input")
search_button.click()

# Wait for loading
time.sleep(2)

# Go to last page. Filling table from last page to first
fast_foward_button = driver.find_elements_by_class_name('rich-datascr-button')[5] # Getting the last button
fast_foward_button.click()

# Wait for loading
time.sleep(2)

# Getting number of pages
num_pages_elem = driver.find_elements_by_class_name('rich-datascr-act')[0]
num_pages = int(num_pages_elem.text)
print('Found ', num_pages, 'pages!')

# Going back to first page
back_foward_button = driver.find_elements_by_class_name('rich-datascr-button')[0]
back_foward_button.click()

# Wait for loading
time.sleep(2)

# Setting up data scructure to store data
df_columns = ['escola','2005_obs','2007_obs','2009_obs',
              '2011_obs','2013_obs','2015_obs','2017_obs',
              '2007_proj','2009_proj','2011_proj','2013_proj',
              '2015_proj','2017_proj','2019_proj','2021_proj']
df = pd.DataFrame(columns=df_columns)

# Starting the loop to get all data
for page in range(1,num_pages+1):
    print('Iterating in page number ', page)

    # Iteracting through each table rows
    table_rows = driver.find_elements_by_class_name('rich-table-row')
    for i,tr in enumerate(table_rows):
        values_to_add = {}
        for j,elem in enumerate(tr.find_elements_by_class_name('rich-table-cell')):
            values_to_add[df_columns[j]] = elem.text
        row_to_add = pd.Series(values_to_add,name=i)
        df = df.append(row_to_add)

    # Finding the next page element, in case we're not in the final page
    if page != num_pages:
        next_page = page + 1
        inactive_elems = driver.find_elements_by_class_name('rich-datascr-inact')
        for elem in inactive_elems:
            if elem.text == next_page:
                elem.click()
                break

        # Wait for loading
        time.sleep(2)
    else:
        print('Parsed all data!')

# Adding columns representing uf, city and adm_dep of the data collected
df['uf'] = uf
df['municipio'] = city
df['dependencia_adm'] = adm_dep
df['anos_escolares'] = 'FUND I'

# Final status of the DataFrame
df.to_csv('dados_crawler_ideb.csv',index=False)





