import json
import math
import os
import requests
from typing import List, Optional, Tuple

import matplotlib.pyplot as plt

def get_scores(token: str) -> Tuple[List, List]:
    '''
    Connect to the Oura API to retrieve the metric values at the specified urls.

    Parameters
    ----------
    token : str
        API token.

    Returns
    -------
    metrics : List
        Metrics that have been retrieved.

    scores : List
        Metric values that have been retrieved.
    '''
    def get_data(url: str) -> Optional[int]:
        '''
        Internal function that performs the retrieving of data from the API.

        Parameters
        ----------
        url : str
            Url to connect to.

        Returns
        -------
        score : Optional[int]
            Metric value that has been retrieved or None if no value was retrieved.
        '''
        header = {
            'Authorization': f'Bearer {token}'
        }
        response = requests.request('GET', url, headers=header)
        json_response = json.loads(response.text)   
        try: 
            # Get today's score.
            score = json_response['data'][1]['score']    
        except Exception:
            try:
                # Get yesterday's score.
                score = json_response['data'][0]['score']
            except Exception:
                return None
        
        return score

    base_url = 'https://api.ouraring.com/v2/usercollection'
    urls = {
        'Readiness': f'{base_url}/daily_readiness',
        'Sleep': f'{base_url}/daily_sleep',
        'Activity':  f'{base_url}/daily_activity'
    }

    metrics = list(urls.keys())
    scores = []
    
    for url in urls.values():
        scores.append(get_data(url))

    return metrics, scores

def create_charts(scores: List) -> None:
    '''
    Create and save a figure showing donut charts of the retrieved values.

    Parameters
    ----------
    scores : List
        Metric values that have been retrieved.
    '''
    N_PLOTS = len(scores)
    N_COLS = 3
    N_ROWS = math.ceil(N_PLOTS / N_COLS)

    scores = [score/100 if score is not None else 0 for score in scores]

    _, ax = plt.subplots(N_ROWS, N_COLS)
    ax.flatten()

    for i in range(N_PLOTS):
        ax[i].pie(
                [scores[i]], 
                startangle=90, 
                wedgeprops={'width':0.3}, 
                normalize=False
        )

    plt.savefig('daily_scores.png', transparent=True, bbox_inches='tight')

def print_header(metrics: List, scores: List) -> None:    
    '''
    Prints metrics and their respective values.

    Parameters
    ----------
    metrics : List
        Metrics that have been retrieved.

    scores : List
        Metric values that have been retrieved.
    '''
    terminal_width = os.get_terminal_size()[0]
    n_columns = len(metrics)
    column_width = int(terminal_width / n_columns)

    message = '\n'
    for list in [metrics, scores]:
        for item in list:
            text = f'{item}'.center(column_width)
            message += text

        print(message)
        message = ''


with open('config.json', 'r') as config_file:
    config = json.load(config_file)
    API_KEY = config['API_KEY']

metrics, scores = get_scores(token=API_KEY)
create_charts(scores)
print_header(metrics, scores)