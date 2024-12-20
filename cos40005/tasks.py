from urllib.parse import urljoin

from celery import shared_task, group
from django.db import transaction

from .models import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import redis
import json
import requests

from .utils import get_chrome_driver

r = redis.Redis(host='localhost', port=6379)


@shared_task
def crawl_domain():
    domain = Domain.objects.get(enable=True)
    # print(domains)
    # for domain in domains:
    try:
        cache = Cache.objects.get(url=domain.domain)
        cache.domain = domain
        cache.status = False
        cache.visited = False
        cache.save()
    except Cache.DoesNotExist:
        Cache.objects.create(domain=domain, url=domain.domain, status=False, visited=False)

    not_visited = Cache.objects.filter(visited=False)
    if not_visited and len(not_visited) > 0:
        driver = get_chrome_driver()
        for cache in not_visited:
            try:
                driver.get(cache.url)
                time.sleep(2)
                links = driver.find_elements(By.TAG_NAME, "a")
                for link in links:
                    href = link.get_attribute("href")
                    if href and (href.startswith(cache.domain.domain) or href.startswith('/')):
                        try:
                            new_cache = Cache(domain=cache.domain, url=href, status=False, visited=False)
                            new_cache.save()
                        except Exception as e:
                            print(f"Error saving cache for {href}: {e}. Cache might be existed in the database")
                cache.visited = True
                cache.save()
            except Exception as ex:
                print(f"Error processing {cache.url}: {ex}")
                cache.visited = True
                cache.save()
                continue
        driver.quit()
        print("Task completed")


@shared_task
def crawl_domain_mogi_hn():
    domain = Domain.objects.get(name="mogi")

    url_template = "https://mogi.vn/ha-noi/mua-nha-dat?cp={page}"
    base_url = "https://mogi.vn"

    driver = get_chrome_driver()
    page = 5800 #thay start number cua m vao day
    while True:
        print("Current page number: ", page)
        if page > 5804: #lay start_page + 1k, thay vao day
            break
        url = url_template.format(page=page)

        driver.get(url)

        driver.implicitly_wait(10)

        link_elements = driver.find_elements(By.CSS_SELECTOR, "a.link-overlay")

        for link_element in link_elements:
            href = link_element.get_attribute("href")
            if href and (href.startswith(base_url) or href.startswith('/')):
                full_url = urljoin(base_url, href)
                try:
                    new_cache = Cache(domain=domain, url=full_url, status=False, visited=True)
                    new_cache.save()
                except Exception as e:
                    print(f"Error saving cache for {href}: {e}. Cache might be existed in the database")
        page += 1


    driver.quit()


@shared_task
def crawl_domain_mogi_hcm():
    domain = Domain.objects.get(name="mogi")

    url_template = "https://mogi.vn/ha-noi/mua-nha-dat?cp={page}"
    base_url = "https://mogi.vn"

    driver = get_chrome_driver()
    page = 10000
    while True:
        url = url_template.format(page=page)

        driver.get(url)

        driver.implicitly_wait(10)

        link_elements = driver.find_elements(By.CSS_SELECTOR, "a.link-overlay")

        for link_element in link_elements:
            href = link_element.get_attribute("href")
            if href and (href.startswith(base_url) or href.startswith('/')):
                full_url = urljoin(base_url, href)
                try:
                    new_cache = Cache(domain=domain, url=full_url, status=False, visited=True)
                    new_cache.save()
                    print(f"Saved cache for {full_url}")
                except Exception as e:
                    print(f"Error saving cache for {href}: {e}. Cache might be existed in the database")
        page += 1

    driver.quit()

#
# @shared_task
# def crawl_property(domain_names):
#     domain_names = domain_names.split(',')
#     for domain_name in domain_names:
#         domain = Domain.objects.get(name=domain_name)
#
#         total_caches = Cache.objects.filter(domain=domain, status=False).count()
#         middle_index = total_caches // 2  # Integer division to get the middle index
#         # Get records from middle to end using offset
#         caches = Cache.objects.filter(domain=domain, status=False)[:200]
#
#         title_type = domain.title_type
#         title_property = domain.title_property
#
#         address_type = domain.address_type
#         address_property = domain.address_property
#
#         price_type = domain.price_type
#         price_property = domain.price_property
#
#         area_type = domain.area_type
#         area_property = domain.area_property
#
#         floor_type = domain.floor_type
#         floor_property = domain.floor_property
#
#         bedroom_type = domain.bedroom_type
#         bedroom_property = domain.bedroom_property
#
#         toilet_type = domain.toilet_type
#         toilet_property = domain.toilet_property
#
#         contact_type = domain.contact_type
#         contact_property = domain.contact_property
#
#         description_type = domain.description_type
#         description_property = domain.description_property
#
#         if caches and len(caches) > 0:
#             options = Options()
#             options.add_argument("--start-maximized")
#             options.add_argument("--no-sandbox")
#             options.add_argument("--disable-dev-shm-usage")
#             options.add_argument("--headless")
#             options.add_argument('--ignore-certificate-errors')
#             options.add_argument('--ignore-ssl-errors')
#             options.add_experimental_option("excludeSwitches", ["enable-automation"])
#             options.add_experimental_option('useAutomationExtension', False)
#             driver = get_chrome_driver()
#             for cache in caches:
#                 driver.get(cache.url)
#                 title = None
#                 address = None
#                 price = None
#                 area = None
#                 floor = None
#                 bedroom = None
#                 toilet = None
#                 publish_date = None
#                 contact = None
#                 description = None
#
#                 if title_type and title_property:
#                     try:
#                         title = driver.find_element(title_type, title_property).text
#                     except:
#                         pass
#                 if address_type and address_property:
#                     try:
#                         address = driver.find_element(address_type, address_property).text
#                     except:
#                         pass
#                 if price_type and price_property:
#                     try:
#                         price = driver.find_element(price_type, price_property).text
#                     except:
#                         pass
#                 if area_type and area_property:
#                     try:
#                         area = driver.find_element(area_type, area_property).text
#                     except:
#                         pass
#                 if floor_type and floor_property:
#                     try:
#                         floor = driver.find_element(floor_type, floor_property).text
#                     except:
#                         pass
#                 if bedroom_type and bedroom_property:
#                     try:
#                         bedroom = driver.find_element(bedroom_type, bedroom_property).text
#                     except:
#                         pass
#                 if toilet_type and toilet_property:
#                     try:
#                         toilet = driver.find_element(toilet_type, toilet_property).text
#                     except:
#                         pass
#                 if publish_date and publish_date:
#                     try:
#                         publish_date = driver.find_element(publish_date, publish_date).text
#                     except:
#                         pass
#                 if contact_type and contact_property:
#                     try:
#                         contact = driver.find_element(contact_type, contact_property).text
#                     except:
#                         pass
#                 if description_type and description_property:
#                     try:
#                         description = driver.find_element(description_type, description_property).text
#                     except:
#                         pass
#                 try:
#                     print(title,address,price)
#                     if title:
#                         property = Property(domain=domain, title=title, address=address, price=price, area=area, floor=floor,
#                                             bedroom=bedroom, toilet=toilet, publish_date=publish_date, contact=contact,
#                                             description=description)
#
#                         property.save()
#                         last = Property.objects.last()
#                         if last.id and last.description:
#                             toExtract = {
#                                 'id': last.id,
#                                 'description': last.description
#                             }
#                             r.rpush('extract_queue', json.dumps(toExtract))
#                     cache.status = True
#                     cache.save()
#                 except Exception as e:
#                     print(e)
#
#             driver.quit()

NUMBER_OF_THREADS = 3 # Neu tren windows thi chinh len (5), macos chinh xuong (2)
@shared_task
def crawl_property(domain_names):
    domain_names = domain_names.split(',')

    for domain_name in domain_names:
        domain = Domain.objects.get(name=domain_name)
        total_caches = Cache.objects.filter(domain=domain, status=False).count()

        if total_caches > 0:
            caches = list(Cache.objects.filter(domain=domain, status=False)[:35000])
            part_size = len(caches) // NUMBER_OF_THREADS  # Divide caches into 5 parts
            tasks = []
            # Dispatch each part to a separate subtask
            for i in range(NUMBER_OF_THREADS):
                start_index = i * part_size
                end_index = (i + 1) * part_size if i < (NUMBER_OF_THREADS - 1) else len(caches)
                cache_part = caches[start_index:end_index]
                print(len(cache_part))
                # crawl_property_subtask.delay(domain, cache_part)
                cache_ids = []
                for cache in cache_part:
                    cache_ids.append(cache.id)
                tasks.append(crawl_property_subtask.s(domain_name, cache_ids))

            group(tasks).apply_async()

@shared_task
def crawl_property_subtask(domain_name, cache_ids):
    domain = Domain.objects.get(name=domain_name)
    caches = Cache.objects.filter(id__in=cache_ids)

# Fetch property attributes from domain object
    title_type = domain.title_type
    title_property = domain.title_property

    address_type = domain.address_type
    address_property = domain.address_property

    price_type = domain.price_type
    price_property = domain.price_property

    area_type = domain.area_type
    area_property = domain.area_property

    floor_type = domain.floor_type
    floor_property = domain.floor_property

    bedroom_type = domain.bedroom_type
    bedroom_property = domain.bedroom_property

    toilet_type = domain.toilet_type
    toilet_property = domain.toilet_property

    contact_type = domain.contact_type
    contact_property = domain.contact_property

    description_type = domain.description_type
    description_property = domain.description_property

    if caches and len(caches) > 0:
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--headless")
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        driver = get_chrome_driver()

        for cache in caches:
            driver.get(cache.url)
            title, address, price, area, floor, bedroom, toilet, publish_date, contact, description = (None,) * 10

            if title_type and title_property:
                try:
                    title = driver.find_element(title_type, title_property).text
                except:
                    pass
            if address_type and address_property:
                try:
                    address = driver.find_element(address_type, address_property).text
                except:
                    pass
            if price_type and price_property:
                try:
                    price = driver.find_element(price_type, price_property).text
                except:
                    pass
            if area_type and area_property:
                try:
                    area = driver.find_element(area_type, area_property).text
                except:
                    pass
            if floor_type and floor_property:
                try:
                    floor = driver.find_element(floor_type, floor_property).text
                except:
                    pass
            if bedroom_type and bedroom_property:
                try:
                    bedroom = driver.find_element(bedroom_type, bedroom_property).text
                except:
                    pass
            if toilet_type and toilet_property:
                try:
                    toilet = driver.find_element(toilet_type, toilet_property).text
                except:
                    pass
            if publish_date and publish_date:
                try:
                    publish_date = driver.find_element(publish_date, publish_date).text
                except:
                    pass
            if contact_type and contact_property:
                try:
                    contact = driver.find_element(contact_type, contact_property).text
                except:
                    pass
            if description_type and description_property:
                try:
                    description = driver.find_element(description_type, description_property).text
                except:
                    pass
            try:
                print(title, address, price)
                if title:
                    property = Property(domain=domain, title=title, address=address, price=price, area=area, floor=floor,
                                        bedroom=bedroom, toilet=toilet, publish_date=publish_date, contact=contact,
                                        description=description)

                    property.save()
                    last = Property.objects.last()
                    if last.id and last.description:
                        toExtract = {
                            'id': last.id,
                            'description': last.description
                        }
                        r.rpush('extract_queue', json.dumps(toExtract))
                cache.status = True
                cache.save()
            except Exception as e:
                print(e)

        driver.quit()


# Define the list of available ports
PORTS = [9966, 9967, 9968, 9969, 9970]

@shared_task
def process_single_port(port, toExtract):
    try:
        # Make API request to the specified port
        res = requests.get(f'http://localhost:{port}?raw_data=' + toExtract['description'])
        res = res.json()

        # Fetch the property from the database
        property = Property.objects.get(id=toExtract['id'])
        print(f"Processing on port {port}: Property ID: {property.id}")
        print(f"Address: {property.address}")
        print(f"Area: {property.area} sq ft (or m²)")  # Adjust unit based on your location
        print(f"Floor: {property.floor}")
        print(f"Bedrooms: {property.bedroom}")
        print(f"Contact: {property.contact}")
        print(f"Bathrooms: {property.toilet} (assuming 'toilet' refers to bathrooms)")
        print(f"Price: ${property.price}")  # Adjust currency symbol if needed

        # Update property details based on the extracted data
        try:
            if not property.address and res['address']['result']:
                property.address = res['address']['result']
            if not property.area and res['real_area']['result']:
                property.area = res['real_area']['result']
            if not property.floor and res['number_of_floors']['result']:
                property.floor = res['number_of_floors']['result']
            if not property.bedroom and res['number_of_bedrooms']['result']:
                property.bedroom = res['number_of_bedrooms']['result']
            if not property.contact and res['contact_number']['result']:
                property.contact = res['contact_number']['result']
            if not property.toilet and res['number_of_toilets']['result']:
                property.toilet = res['number_of_toilets']['result']
            if not property.price and res['price']['result']:
                property.price = res['price']['result']
            if not property.publish_date and res['publish_date']['result']:
                property.publish_date = res['publish_date']['result']
        except Exception as e:
            print('Form not correct', e)
        print("--------------------------------done")
        print(f"Property ID: {property.id}")
        print(f"Address: {property.address}")
        print(f"Area: {property.area} sq ft (or m²)")  # Adjust unit based on your location
        print(f"Floor: {property.floor}")
        print(f"Bedrooms: {property.bedroom}")
        print(f"Contact: {property.contact}")
        print(f"Bathrooms: {property.toilet} (assuming 'toilet' refers to bathrooms)")
        print(f"Price: ${property.price}")  # Adjust currency symbol if needed
        # Save the updated property details
        property.save()

        print(f"Property ID: {property.id} processing completed on port {port}.")

    except Exception as ex:
        print(f'Extract failed on port {port}', ex)


@shared_task
def call_api_extract():
    try:
        # Pop 5 items from the Redis queue
        items_to_extract = []
        for _ in range(5):
            toExtract = r.lpop('extract_queue')
            if not toExtract:
                print("No more items left in the queue. Stopping task.")
                break
            toExtract = json.loads(toExtract)
            items_to_extract.append(toExtract)

        # If no items were extracted, stop the task
        if not items_to_extract:
            print("No items to process.")
            return

        # Assign each item to a different port
        tasks = []
        for index, toExtract in enumerate(items_to_extract):
            port = PORTS[index % len(PORTS)]  # Cycle through the ports
            tasks.append(process_single_port.s(port, toExtract))

        # Execute all tasks concurrently
        group(tasks).apply_async()

    except Exception as ex:
        print('Main extract task failed', ex)