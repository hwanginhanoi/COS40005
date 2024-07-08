from celery import shared_task
from .models import Property, Domain, Cache
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse, urljoin
import time

driver = webdriver.Chrome()

options = Options()
options.headless = True  # Enable headless mode
options.add_argument("--window-size=1920,1200")  # Set the window size

url = 'https://mogi.vn/'

@shared_task
def insert_data_to_db(data):
    print(data)
    domain, created = Domain.objects.get_or_create(title=data['domain'])
    property_data = Property(
        domain=domain,
        title=data['title'],
        address=data['address'],
        price=data['price'],
        area=data['area'],
        floor=data['floor'],
        bedroom=data['bedroom'],
        toilet=data['toilet'],
        publish_date=data['publish_date'],
        contact=data['contact'],
        description=data['description']
    )
    property_data.save()

@shared_task
def crawl_domain(driver, url):
    # domain, created = Domain.objects.get_or_create(name=domain_name)
    if Cache.objects.filter(url=url, visited=True).exists():
        return

    driver.get(url)
    time.sleep(2)

    links = driver.find_elements(By.TAG_NAME, "a")
    for link in links:
        href = link.get_attribute("href")
        if href and href.startswith(url):
            try:
                Cache.objects.create(title='Mogi', url=href)
            except Exception as e:
                continue

    Cache.objects.filter(url=url).update(visited=True)

    new_links = Cache.objects.filter(title=domain, visited=False)
    for link in new_links:
        crawl_domain(driver, domain, link.url)

crawl_domain(driver, domain, domain_name)

driver.quit()

