from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

options = Options()
options.headless = True  # Enable headless mode
options.add_argument("--window-size=1920,1200")  # Set the window size


driver.get("https://batdongsan.com.vn/cho-thue-van-phong-duong-nguyen-du-phuong-nguyen-du/chinh-chu-cho-san-85-dt-tu-50-100-200m2-noi-that-pccc-pr40028370")



title = driver.find_element(By.CLASS_NAME, 'js__pr-title')
address = driver.find_element(By.CLASS_NAME, 'js__pr-address')
items = driver.find_elements(By.CLASS_NAME, 're__pr-short-info-item')

print(title.text)
print(address.text)
for item in items:
    value_element = item.find_element(By.CLASS_NAME, 'value')
    print(value_element.text)


driver.quit()


