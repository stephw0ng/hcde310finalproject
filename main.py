#import urllib, json, urllib2
#import jinja2, os, logging,
import urllib.request, urllib.error, urllib.parse, json, webbrowser, webapp2


class MainHandler(webapp2.RequestHandler):
    def get(self):
        vals = {}
        searchterm = self.request.get('search_term')
        go = self.request.get('btn search')
        logging.info(searchterm)
        logging.info(go)
        if searchterm:
            # if form filled in, get results using this data
            food_filters = self.request.get_all('food_filter')
            logging.info(food_filter)
            # GET RECIPES USING FILTERS

            article_filters = self.request.get_all('news_filter')
            logging.info(news_filter)
            # GET ARTICLES USING FILTERS

            # UPDATE PAGE
            # template = JINJA_ENVIRONMENT.get_template('greetresponse.html')
            # self.response.write(template.render(vals))
        else:
            # if no search term, then show the form again with a correction to the user
            # note: this prompt still needs to be added to the HTML
            vals['prompt'] = "How can I greet you if you don't enter a name?"
            template = JINJA_ENVIRONMENT.get_template('greetform.html')
            self.response.write(template.render(vals))


# JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
#     extensions=['jinja2.ext.autoescape'], autoescape=True)
#
# def test():
#     print("hi")