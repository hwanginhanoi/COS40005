import time
from sys import stdout
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from .models import Property, Domain, Cache


def handle(self, *args, **kwargs):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    domain_name = "https://mogi.vn/mua-nha-dat"
    domain, created = Domain.objects.get_or_create(name=domain_name)
    self.crawl_domain(driver, domain, domain_name)

    driver.quit()


def crawl_domain(self, driver, domain, url):
    if Cache.objects.filter(url=url, visited=True).exists():
        return

    driver.get(url)
    time.sleep(2)

    links = driver.find_elements(By.TAG_NAME, "a")
    for link in links:
        href = link.get_attribute("href")
        if href and href.startswith(domain.name):
            try:
                Cache.objects.create(title=domain, url=href)
            except IntegrityError:
                continue

    Cache.objects.filter(url=url).update(visited=True)

    new_links = Cache.objects.filter(title=domain, visited=False)
    for link in new_links:
        self.crawl_domain(driver, domain, link.url)


handle()