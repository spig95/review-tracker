from django.urls import path
from scrape_app import views


urlpatterns = [
    path('', views.scraping_index_page, name='index'),
    path('index', views.scraping_index_page, name='index'),  # Check if this is canonical:)
    path('scrape/<str:scraper_name>', views.scrape, name="scrape"),
    path('api/get_scrape_task_results', views.get_scrape_task_results, name="get_scrape_task_results"),
    path('api/stop_scraping_and_get_partial_results',
         views.stop_scraping_and_get_partial_results,
         name="stop_scraping_and_get_partial_results")
]