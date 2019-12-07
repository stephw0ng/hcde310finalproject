import json, urllib2, urllib
import jinja2, os, logging, webapp2

def safeGet(url):
    try:
        return urllib2.urlopen(url)
    except urllib2.HTTPError as e:
        logging.error("The server couldn't fulfill the request.")
        logging.error("Error code: ", e.code)
    except urllib2.URLError as e:
        logging.error("We failed to reach a server")
        logging.error("Reason: ", e.reason)
    return None

### EDAMAM CODE ###
edamambaseurl = "https://api.edamam.com/search"
app_key = "30589e1f9f7a3953ed9b6ec2e893495e"
application_id = "5df38ba5"

# Method to get JSON from API
def getRecipes(q, params={}):
    params['app_key'] = app_key
    params['app_id'] = application_id
    params['q'] = q
    url = edamambaseurl + "?" + urllib.parse.urlencode(params)
    safeurl = safeGet(url)
    if safeurl is None:
        return None
    return json.load(safeurl)

# Class for a Recipe
class Recipe():
    def __init__(self, recipeDict):
        self.title = recipeDict['label']
        self.image = recipeDict['image']
        self.time = recipeDict['totalTime']
        self.link = recipeDict['url']
        self.numIngredients = len(recipeDict['ingredients'])
        self.servesPeople = recipeDict['yield']

### NYT CODE ###
api_key = "VnAC49a37JJMyA6aPbvMGymXVJbeIb4t"
NYTbaseurl = "http://api.nytimes.com/svc/"

# gets JSON from API
def articleSearch(searchwords, params={}):
    params['api-key'] = api_key
    params['fq'] = "news_desk:(\"Food\" \"Business\" \"World\" \"Dining\" \"Environment\" \"Health\") AND " + searchwords

    url = NYTbaseurl + "search/v2/articlesearch.json?" + urllib.parse.urlencode(params)
    safeurl = safeGet(url)
    if safeurl is None:
        return None
    return json.load(safeurl)

# turn each article dict into an Article class
class Article:
   def __init__(self, articledict):
       self.headline = articledict['headline']['main']
       self.summary = articledict['snippet']
       author = articledict['byline']['person'][0]
       self.author = author['firstname'] + " " + author['lastname']
       keywords = []
       for x in dict['keywords']:
           keywords.append(x['value'])
       self.keywordslist = keywords

# returns dict with sort param if user chooses a sort option
def articleSort(filterlist):
    if len(filterlist) > 0:
        return {'sort':filterlist[0]}
    else:
        return {}

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'], autoescape=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        vals = {}
        searchterm = self.request.get('search_term')
        go = self.request.get('searchbutton')
        logging.info(searchterm)
        logging.info(go)
        if searchterm:
            # if form filled in, get results using this data
            food_filters = self.request.get_all('food_filter')
            logging.info(food_filters)
            # GET RECIPES USING FILTERS

            article_filters = self.request.get_all('news_filter')
            vals['filter'] = article_filters[0]
            # GET ARTICLES USING FILTERS
            #articleSearch(searchterm, params=articleSort(article_filters))
            template = JINJA_ENVIRONMENT.get_template('template.html')
            self.response.write(template.render(vals))

            # UPDATE PAGE
            # template = JINJA_ENVIRONMENT.get_template('greetresponse.html')
            # self.response.write(template.render(vals))
        else:
            # if no search term, then show the form again with a correction to the user
            # note: this prompt still needs to be added to the HTML
            vals['prompt'] = "How can I greet you if you don't enter a name?"
            template = JINJA_ENVIRONMENT.get_template('template.html')
            self.response.write(template.render(vals))

application = webapp2.WSGIApplication([('/.*', MainHandler)],
                                      debug=True)