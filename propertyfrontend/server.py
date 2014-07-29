from propertyfrontend import app

from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import abort

from healthcheck import HealthCheck

import requests

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

@app.template_filter()
def currency(value):
    """Format a comma separated  currency to 2 decimal places."""
    return "{:,.2f}".format(float(value))

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
    return render_template('view_property.html', title=json,
      service_frontend_url = service_frontend_url)

@app.route('/search')
def search():
    return redirect(url_for('index'))

@app.route('/search/results', methods=['POST'])
def search_results():
    query = request.form['search']
    search_api_url = "%s/%s" % (search_api, 'search')
    search_url = "%s?query=%s" % (search_api_url, query)
    app.logger.info("URL requested %s" % search_url)
    response = get_or_log_error(search_url)
    json = response.json()
    app.logger.info("Found for the following: %s" % json)
    return render_template('search_results.html', results=json['results'])

@app.errorhandler(404)
def page_not_found(err):
    return render_template('404.html'), 404

@app.errorhandler(500)
def error(err):
    return render_template('500.html'), 500

# could go further and create a catch all that ensures we
# return nicer page than default for *any* errors?

@app.after_request
def after_request(response):
    response.headers.add('Content-Security-Policy', "default-src 'self' 'unsafe-inline' data:") # can we get some guidance on this?
    response.headers.add('X-Frame-Options', 'deny')
    response.headers.add('X-Content-Type-Options', 'nosniff')
    response.headers.add('X-XSS-Protection', '1; mode=block')
    return response
