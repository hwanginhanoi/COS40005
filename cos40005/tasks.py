from celery import shared_task
from .models import Property, Domain, Cache
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

options = Options()
options.headless = True  # Enable headless mode
options.add_argument("--window-size=1920,1200")  # Set the window size

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
def crawl_urls_to_cache(data):
    domains = Domain.objects.values('domain', 'title', 'pagination')
    for domain in domains:
        base_url = domain['domain'] + domain['pagination']
        page = 1
        urls = []

        while True:
            try:
                pagination_url = f'{base_url}?cp={page}'

                driver.get(pagination_url)

                next_page_button = driver.find_element(By.CSS_SELECTOR, '.pagination__next a')
                if not next_page_button.is_enabled():
                    break

                page += 1
            except (TimeoutException, NoSuchElementException) as e:
                print(f'Error on page {page} for {domain.title}: {e}')
                break  # Exit loop on error

            finally:
                driver.quit()  # Close the browser after each loop





def crawl_data():
    print()
