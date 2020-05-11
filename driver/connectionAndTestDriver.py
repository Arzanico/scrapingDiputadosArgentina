from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait

# driver.navigate("file:///race_condition.html")

driver = webdriver.Chrome('./chromedriver')  # Optional argument, if not specified will search path.

myurl = "https://votaciones.hcdn.gob.ar"


driver.get(myurl)
# time.sleep(5) # Let the user actually see something!
# Elemento formulario de busqueda
form = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element_by_tag_name('form'))
buton = form.find_element_by_tag_name('button')
buton.click()


time.sleep(5) # Let the user actually see something!
driver.quit()