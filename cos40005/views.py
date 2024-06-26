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
price = driver.find_element(By.XPATH, './/*[contains(concat(" ",normalize-space(@class)," ")," re__pr-short-info-item ")]/span[contains(normalize-space(),"Mức giá")]/following-sibling::span')
area = driver.find_element(By.XPATH, './/*[contains(concat(" ",normalize-space(@class)," ")," re__pr-short-info-item ")]/span[contains(normalize-space(),"Diện tích")]/following-sibling::span')

print("title: ", title.text)
print("address: ", address.text)
print("price: ", price.text)
print("area: ", area.text)


driver.quit()


