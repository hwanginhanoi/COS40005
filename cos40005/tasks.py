from celery import shared_task


@shared_task
def crawl_data():
    print()
