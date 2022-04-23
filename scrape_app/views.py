from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

from review_tracker import celery_app
from scrape_app.forms.scraper_type import ScraperForm
from scrape_app.forms.url_and_params import URLAndParamsForm
from scrape_app.tasks import scrape_task
from scrape_app.utility.logger import log
from scrape_app.utility.plot import get_html_plot
from scrape_app.utility.web_utils import get_soup


def scraping_index_page(request):
    """Page that selects the scraper to be used using a ScraperForm"""
    if request.method == 'POST':
        form = ScraperForm(request.POST)
        if form.is_valid():
            scraper_name = form.cleaned_data["scraper_name"]
            return redirect("scrape", scraper_name=scraper_name)
    else:
        form = ScraperForm()

    return render(request, 'index.html', {'form': form})


def scrape(request, scraper_name: str):
    """View to select restaurant url + other scraper params"""
    log.debug(f"scraper_name: {scraper_name}")

    params_form = URLAndParamsForm(scraper_name=scraper_name)
    running_task_id = None

    if request.method == 'POST':
        if "start_scrape_task" in request.POST:
            params_form = URLAndParamsForm(request.POST, scraper_name=scraper_name)
            log.debug(f"params_form: {params_form}")
            if params_form.is_valid():
                scrape_task_kwargs = {
                    "scraper_name": params_form.get_scraper_name(),
                    "url": params_form.get_url_to_scrape(),
                    "params_dict": params_form.get_scraper_params_dict(),
                }
                res = scrape_task.apply_async(args=(), kwargs=scrape_task_kwargs)
                running_task_id = res.id
                log.debug(f"Celery task launched. ID {running_task_id}")
            else:
                # Todo: do something nicer here
                return HttpResponse("Invalid form")

    args_dict = {
        'form': params_form,
        'scraper_name': scraper_name,
        'running_task_id': running_task_id,
    }
    return render(request, 'scrape.html', args_dict)


def get_scrape_task_results(request):
    """View used in Ajax calls to get results of running scrape task"""
    # Is this correct? Shall we just raise an error if the request does not have the tid?
    running_task_id = None
    if request.method == 'GET':
        running_task_id = request.GET.get("running_task_id", None)

    if running_task_id is None:
        # Todo: do something nicer here
        return HttpResponse(f"Got a wrong request. Expecting a GET request with a running task id. Got {request}")

    return get_json_response_with_task_results(running_task_id)


def stop_scraping_and_get_partial_results(request):
    """Kill the task with the id specified in the request and returns the results obtained so far."""
    if request.method == 'GET':
        task_to_kill = request.GET.get("task_to_kill")
    else:
        return HttpResponse(f"Unexpected request, use a POST to kill a task. Got {request}")

    ret = get_json_response_with_task_results(task_to_kill)

    log.debug(f"Killing task {task_to_kill}")
    res = scrape_task.AsyncResult(task_to_kill, app=celery_app)
    res.revoke(terminate=True)
    log.debug("Returning")
    return ret


def get_json_response_with_task_results(running_task_id):
    task = scrape_task.AsyncResult(running_task_id)
    log.debug(f"running_task_id: {running_task_id}")

    if task.state == "SUCCESS":
        aggregated_results = task.get()
    elif task.state == "PROGRESS":
        aggregated_results = task.info
    else:
        # Unknown state
        aggregated_results = {}

    info_str = aggregated_results.get("info_str", f"No info on current task yet. Task in '{task.state}' state.")
    timestamps = aggregated_results.get("timestamps", [])
    ratings = aggregated_results.get("ratings", [])
    done = aggregated_results.get("done", False)

    graph = get_html_plot(timestamps, ratings, with_slider=done)

    ret = {
        "running_task_id": running_task_id,
        "is_result_final": done,
        "info_str": info_str,
        "graph": graph
        }

    return JsonResponse(ret)
