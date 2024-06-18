from celery import shared_task
from .models import Property, Domain

@shared_task
def insert_data_to_db(data):
    for items in data:
        domain, created = Domain.objects.get_or_create(title=items['domain'])
        property_data = Property(
            domain=domain,
            title=items['title'],
            address=items['address'],
            price=items['price'],
            area=items['area'],
            floor=items['floor'],
            bedroom=items['bedroom'],
            toilet=items['toilet'],
            publish_date=items['publish_date'],
            contact=items['contact'],
            description=items['description']
        )
        property_data.save()

def crawl_data():
    print()
