import os

from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import abort
from healthcheck import HealthCheck
import requests

from propertyfrontend import app

search_api = app.config['SEARCH_API']
HealthCheck(app, '/health')

def get_or_log_error(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response
    except requests.exceptions.HTTPError as e:
        app.logger.error("HTTP Error %s", e)
        abort(response.status_code)
    except requests.exceptions.ConnectionError as e:
        app.logger.error("Error %s", e)
        abort(500)


@app.route('/')
def index():
    return render_template('search.html')


@app.route('/property/<title_number>')
def property_by_title_number(title_number):
    title_url = "%s/%s/%s" % (search_api, 'titles', title_number)
    app.logger.info("Requesting title url : %s" % title_url)
    response = get_or_log_error(title_url)
    json = response.json()
    app.logger.info("Found the following title: %s" % json)
    service_frontend_url = '%s/%s' % (app.config['SERVICE_FRONTEND_URL'], 'property')
    return render_template(
        'view_property.html',
        title=json,
        apiKey=os.environ['OS_API_KEY'],
        service_frontend_url=service_frontend_url)


@app.route('/search')
def search():
    return redirect(url_for('index'))

@app.route('/search/results', methods=['GET'])
def search_results():
    query = request.args['search']
    search_api_url = "%s/%s" % (search_api, 'search')
    search_url = "%s?query=%s" % (search_api_url, query)
    app.logger.info("URL requested %s" % search_url)
    response = get_or_log_error(search_url)
    result_json = response.json()
    app.logger.info("Found for the following %s result: %s"
      % (len(result_json['results']), result_json))
    one_result = len(result_json['results']) == 1

    return render_template(
        'search_results.html',
        results=result_json['results'],
        query=query,
        apiKey=os.environ['OS_API_KEY']
    )
