from celery import shared_task
from .models import Property, Domain, Cache
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time


@shared_task
def crawl_domain():
    domains = Domain.objects.all()
    for domain in domains:
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
        driver = webdriver.Chrome()
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--headless=new")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        for cache in not_visited:
            try:
                driver.get(cache.url)
                time.sleep(2)
                links = driver.find_elements(By.TAG_NAME, "a")
                for link in links:
                    href = link.get_attribute("href")
                    if href and href.startswith(cache.domain.domain):
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
def crawl_property(domain_name):
    domain = Domain.objects.get(name=domain_name)
    caches = Cache.objects.filter(domain=domain, status=False)

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

    toilet_type = domain.tolet_type
    toilet_property = domain.tolet_property

    contact_type = domain.contact_type
    contact_property = domain.contact_property

    description_type = domain.description_type
    description_property = domain.description_property

    if caches and len(caches) > 0:
        driver = webdriver.Chrome()
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--headless=new")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        for cache in caches:
            title = None
            address = None
            price = None
            area = None
            floor = None
            bedroom = None
            toilet = None
            publish_date = None
            contact = None
            description = None

            if title_type and title_property:
                try:
                    title = driver.find_element(title_type, title_property)
                except:
                    pass
            if address_type and address_property:
                try:
                    address = driver.find_element(address_type, address_property)
                except:
                    pass
            if price_type and price_property:
                try:
                    price = driver.find_element(price_type, price_property)
                except:
                    pass
            if area_type and area_property:
                try:
                    area = driver.find_element(area_type, area_property)
                except:
                    pass
            if floor_type and floor_property:
                try:
                    floor = driver.find_element(floor_type, floor_property)
                except:
                    pass
            if bedroom_type and bedroom_property:
                try:
                    bedroom = driver.find_element(bedroom_type, bedroom_property)
                except:
                    pass
            if toilet_type and toilet_property:
                try:
                    toilet = driver.find_element(toilet_type, toilet_property)
                except:
                    pass
            if publish_date and publish_date:
                try:
                    publish_date = driver.find_element(publish_date, publish_date)
                except:
                    pass
            if contact_type and contact_property:
                try:
                    contact = driver.find_element(contact_type, contact_property)
                except:
                    pass
            if description_type and description_property:
                try:
                    description = driver.find_element(description_type, description_property)
                except:
                    pass

            property = Property(domain=domain, title=title, address=address, price=price, area=area, floor=floor,
                                bedroom=bedroom, toilet=toilet, publish_date=publish_date, contact=contact,
                                description=description)
            property.save()
            cache.visited = True
            cache.save()

        driver.quit()

