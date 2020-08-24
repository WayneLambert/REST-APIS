import string

from collections import defaultdict
from typing import Any, List, Tuple

from django.shortcuts import render
from django.views.decorators.cache import cache_page

import requests

from bs4 import BeautifulSoup


def get_area_results(results: dict) -> List[Tuple[Any]]:
    """
    Assembles each of the area's results together into an iterable for
    template rendering.
    """
    area_results = zip(
        results['area_name'],
        results['leave_votes'],
        results['leave_percent'],
        results['remain_votes'],
        results['remain_percent'],
        results['area_votes'],
        results['turnout'],
    )
    results = []
    for area in area_results:
        results.append(area)

    return results


def scrape_content() -> List[List[int]]:
    """
    Scrapes the results of the EU Referendum from the BBC website
    """
    ALPHABET = string.ascii_lowercase
    BASE_URL = 'https://www.bbc.co.uk/news/politics/eu_referendum/results/local/'
    results = defaultdict(list)
    for letter in ALPHABET:
        page_response = requests.get(f"{BASE_URL}{letter}", timeout=5)
        if page_response:
            page_content = BeautifulSoup(page_response.content, "html.parser")
            areas = page_content.find_all('div', attrs={'class': 'eu-ref-result-bar'})
            for area in areas:
                results['area_name'].append(area.find('h3').getText())
                cleaned_leave_votes = int(area.find_all(
                    'div', {'class': 'eu-ref-result-bar__votes'})
                                          [0].string.strip().split('\n')[0].strip().replace(',', ''))
                results['leave_votes'].append(cleaned_leave_votes)
                cleaned_remain_votes = int(area.find_all(
                    'div', {'class': 'eu-ref-result-bar__votes'})
                                           [1].string.strip().split('\n')[0].strip().replace(',', ''))
                results['remain_votes'].append(cleaned_remain_votes)
                area_votes = cleaned_leave_votes + cleaned_remain_votes
                results['area_votes'].append(area_votes)
                results['leave_percent'].append(f"{cleaned_leave_votes / area_votes:.1%}")
                results['remain_percent'].append(f"{cleaned_remain_votes / area_votes:.1%}")
                results['turnout'].append(
                    area.find('div', {'class': 'eu-ref-result-bar__turnout'})
                    .getText().replace('Turnout: ', ''))
        else:
            continue
    return results


def calc_leave_votes(results: list) -> int:
    """
    Calculates the total number of leave votes from the scraped data.
    """
    return sum(result[1] for result in results)


def calc_remain_votes(results: list) -> int:
    """
    Calculates the total number of remain votes from the scraped data.
    """
    return sum(result[3] for result in results)


@cache_page(timeout=None)
def get_referendum_results(request):
    """
    Retrieves the 2016 Brexit Referendum results from the BBC website.
    """
    results = scrape_content()
    results = get_area_results(dict(results))
    leave_votes = calc_leave_votes(results)
    remain_votes = calc_remain_votes(results)
    total_votes = leave_votes + remain_votes
    total_leave_percent = f"{leave_votes / total_votes:.1%}"
    total_remain_percent = f"{remain_votes / total_votes:.1%}"

    context = {
        'results': results,
        'leave_votes': leave_votes,
        'remain_votes': remain_votes,
        'total_votes': total_votes,
        'total_leave_percent': total_leave_percent,
        'total_remain_percent': total_remain_percent,
    }

    return render(request, 'referendum.html', {'context': context})
