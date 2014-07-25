from property_frontend import app
from flask import render_template, request, redirect, url_for
import requests

@app.template_filter()
def currency(value):
    """Format a comma separated  currency to 2 decimal places."""
    return "{:,.2f}".format(float(value))

@app.route('/')
def index():
     return render_template('search.html')

@app.route('/property/<title_number>')
def property(title_number):

    title_url = "%s/%s/%s" % (app.config['SEARCH_API'], 'titles', title_number)
    app.logger.info("Requesting title url : %s" % title_url)

    #TODO - put more/better error handling around request
    response = requests.get(title_url)
    app.logger.info("Status code %s" % response.status_code)
    if response.status_code == 404:
            return render_template('404.html'), 404
    else:
        title_json = response.json()

        app.logger.info("Found the following title: %s" % title_json)
        return render_template('view_property.html',
                title_number = title_json['title_number'],
                house_number = title_json['house_number'],
                road = title_json['road'],
                town = title_json['town'],
                postcode = title_json['postcode'],
                price_paid = title_json['price_paid'])

# Note -Does elasticsearch return empty json array
# for now results? If so I don't think maybe just show
# results page with no results message not 404?
@app.route('/search/')
def search():
    return redirect(url_for('index'))

@app.route('/search/results/')
def search_results():
    query = request.args.get('search', '')
    search_api_url = "%s/%s" % (app.config['SEARCH_API'], 'search')
    search_url = search_api_url + "?query=" + query

    app.logger.info("URL requested %s" % search_url)
    r = requests.get(search_url)
    json = r.json()
    app.logger.info("Found for the following: %s" % json)
    if json:
        return render_template('search_results.html', results = json['results'])
    else:
        return render_template('404.html'), 404

@app.after_request
def after_request(response):
    response.headers.add('Content-Security-Policy', "default-src 'self' 'unsafe-inline' data:") # can we get some guidance on this?
    response.headers.add('X-Frame-Options', 'deny')
    response.headers.add('X-Content-Type-Options', 'nosniff')
    response.headers.add('X-XSS-Protection', '1; mode=block')
    return response
