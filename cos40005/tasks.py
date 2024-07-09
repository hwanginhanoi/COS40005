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
def crawl_domain():
    driver = webdriver.Chrome()
    domain = None
    domains = Domain.objects.all()
    if len(domains) > 0:
        domain = domains[0]
    else:
        domain = Domain(name = 'Mogi', domain = "https://mogi.vn/")
        domain.save()

    url = domain.domain

    not_visited = Cache.objects.filter(visited=False)

    if not_visited and len(not_visited) > 0:
        not_visited = not_visited[0]

        try:
            crawl_content(domain, not_visited.url)
        except Exception as e:
            print(e)

        not_visited.visited = True
        not_visited.save()
    else:
        options = Options()
        options.headless = True  # Enable headless mode
        options.add_argument("--window-size=1920,1200")  # Set the window size
        if Cache.objects.filter(url=url, visited=False).exists():
            return
        driver.get(url)
        time.sleep(2)

        links = driver.find_elements(By.TAG_NAME, "a")
        for link in links:
            href = link.get_attribute("href")
            if href and href.startswith(url):
                try:
                    print(href)
                    cache = Cache(domain = domain, url = href)
                    cache.save()
                except Exception as e:
                    print(e)

        driver.quit()

def crawl_content(domain, url):
    driver = webdriver.Chrome()
    options = Options()
    options.headless = True  # Enable headless mode
    options.add_argument("--window-size=1920,1200")  # Set the window size
    driver.get(url)
    time.sleep(2)

    title= ''
    address = ''
    price = ''
    area = ''
    floor = ''
    bedroom = ''
    toilet = ''
    publish_date = ''
    contact = ''
    description = ''

    # if domain.title_type and domain.title_property:
    try:
        title = driver.find_element('css selector', '.main-info .title h1')
        if title:
            title = title.text
    except:
        pass
    try:
        address = driver.find_element('css selector', '.main-info .address')
        if address:
            address = address.text
    except:
        pass
    try:
        price = driver.find_element('css selector', '.main-info .price')
        if price:
            price = price.text
    except:
        pass
    try:
        area = driver.find_element('xpath', './/*[contains(concat(" ",normalize-space(@class)," ")," info-attr ")][contains(concat(" ",normalize-space(@class)," ")," clearfix ")]/span[contains(normalize-space(),"Diện tích đất")]/following-sibling::span')
        if area:
            area = area.text
    except:
        pass
    # floor = driver.find_element('css selector', '.main-info .title h1').text
    try:
        bedroom = driver.find_element('css selector', './/*[contains(concat(" ",normalize-space(@class)," ")," info-attr ")][contains(concat(" ",normalize-space(@class)," ")," clearfix ")]/span[contains(normalize-space(),"Phòng ngủ")]/following-sibling::span')
        if bedroom:
            bedroom = bedroom.text
    except:
        pass
    try:
        toilet = driver.find_element('css selector', './/*[contains(concat(" ",normalize-space(@class)," ")," info-attr ")][contains(concat(" ",normalize-space(@class)," ")," clearfix ")]/span[contains(normalize-space(),"Nhà tắm")]/following-sibling::span')
        if toilet:
            toilet = toilet.text
    except:
        pass
    # publish_date = driver.find_element('css selector', '.main-info .title h1').text
    try:
        show = driver.find_element('css selector', '.showphonetext')
        if show:
            show.click()
    except:
        pass
    try:
        contact = driver.find_element('css selector', '.showphonetext ~ span')
        if contact:
            contact = contact.text
    except:
        pass
    try:
        description = driver.find_element('css selector', '.info-content-body')
        if description:
            description = description.text
    except:
        pass

    if title:
        property = Property(domain=domain, title=title, address=address, price=price, area=area, floor=floor, bedroom=bedroom, toilet=toilet, publish_date=publish_date, contact=contact, description=description)
        property.save()

    links = driver.find_elements(By.TAG_NAME, "a")
    for link in links:
        href = link.get_attribute("href")
        if href and href.startswith(domain.domain):
            try:
                print(href)
                cache = Cache(domain=domain, url=href)
                cache.save()
            except Exception as e:
                print(e)

    driver.quit()





