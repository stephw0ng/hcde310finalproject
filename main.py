import json, urllib2, urllib
import jinja2, os, logging, webapp2
from datetime import datetime


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
app_key = "YOUR APP KEY HERE
application_id = "YOUR APPLICATION ID HERE"


# Method to get JSON from API
def getRecipes(q, filters, params={}):
    params['app_key'] = app_key
    params['app_id'] = application_id
    params['q'] = q
    url = edamambaseurl + "?" + urllib.urlencode(params) + "&" + recipesWithFilters(filters)
    safeurl = safeGet(url)
    if safeurl is None:
        return None
    return json.load(safeurl)


# Class for a Recipe
class Recipe():
    def __init__(self, recipeDict):
        self.title = recipeDict['label']
        self.image = recipeDict['image']
        time = recipeDict['totalTime']
        self.time = time
        if time == 0.0:
            self.timeString = "Time is not given"
        else:
            self.timeString = str(int(time)) + " minutes"
        self.link = recipeDict['url']
        self.numIngredients = len(recipeDict['ingredients'])
        self.servesPeople = int(recipeDict['yield'])


### NYT CODE ###
api_key = "YOUR API KEY HERE"
NYTbaseurl = "http://api.nytimes.com/svc/"


# gets JSON from API
def articleSearch(searchwords, params={}):
    params['api-key'] = api_key
    params['fq'] = "news_desk:(\"Food\" \"Business\" \"World\" \"Dining\" \"Environment\" " \
                   "\"Health\" \"Home\") " \
                   "AND " + searchwords

    url = NYTbaseurl + "search/v2/articlesearch.json?" + urllib.urlencode(params)
    safeurl = safeGet(url)
    if safeurl is None:
        return None
    return json.load(safeurl)


# turn each article dict into an Article class
class Article:
    def __init__(self, articledict):
        self.headline = articledict['headline']['main']
        self.summary = articledict['snippet']
        self.url = articledict['web_url']
        self.date = datetime.strptime(articledict['pub_date'], '%Y-%m-%dT%H:%M:%S+%f').strftime('%B %d, %Y')

        if len(articledict['byline']['person']) != 0:
            author = articledict['byline']['person'][0]
            self.author = ""
            if author['firstname'] is not None:
                self.author += author['firstname'] + " "
            if author['lastname'] is not None:
                self.author += author['lastname']
        else:
            self.author = "No author"

        keywords = []
        for x in articledict['keywords']:
            keywords.append(x['value'])
        self.keywordslist = keywords


# returns dict with params for filtering recipes
def recipesWithFilters(filterlist):
    str = ""
    listlen = len(filterlist)
    if listlen > 0:
        for filter in filterlist[:listlen - 1]:
            str += "health=" + filter + "&"
        str += "health=" + filterlist[listlen - 1]
    return str

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
                                       extensions=['jinja2.ext.autoescape'], autoescape=True)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        vals = {}
        # Get users search term
        searchterm = self.request.get('search_term')
        go = self.request.get('searchbutton')
        logging.info(searchterm)
        logging.info(go)

        # Check if user inputed a search term
        if searchterm:
            # If form filled in, get results using this data
            # Get the food filters
            food_filters = self.request.get_all('food_filter')
            logging.info(food_filters)
            # Get the number of results to show from user
            num_results = self.request.get('num_results')
            pages = (int(num_results) / 10)

            # Get recipes using filters
            allRecipes = getRecipes(searchterm, food_filters, params={'to': num_results})['hits']
            # Put the recipes into Recipe objects
            listDictRecipes = [Recipe(x['recipe']) for x in allRecipes]
            # Sort Recipe objects by user input (either by number of people the recipe serves
            # or by the number of ingredients
            sortInput = self.request.get('food_sort')
            if sortInput == 'servings':
                sortedDictRecipes = sorted(listDictRecipes, key=lambda obj: obj.servesPeople, reverse=True)
            elif(sortInput == 'number of ingredients'):
                sortedDictRecipes = sorted(listDictRecipes, key=lambda obj: obj.numIngredients)


            # Takes input for how the articles should be sorted
            news_sort = self.request.get('news_sort')

            # Creates a list of Article objects with the requested number of results
            allArticles = []
            for p in range(pages):
                searchdict = articleSearch(searchterm, params={'sort':news_sort, 'page':p})
                listArticles = searchdict['response']['docs']
                articlesObjectList = [Article(article) for article in listArticles]
                allArticles.extend(articlesObjectList)

            # Pass values to the HTML template
            vals['searchterm'] = searchterm
            vals['numresults'] = num_results
            vals['recipefilters'] = food_filters
            vals['recipesort'] = sortInput
            vals['recipes'] = sortedDictRecipes
            vals['newssort'] = news_sort
            vals['articles'] = allArticles

            template = JINJA_ENVIRONMENT.get_template('template.html')
            self.response.write(template.render(vals))
        # If no search term, display blank template
        else:
            template = JINJA_ENVIRONMENT.get_template('template.html')
            self.response.write(template.render(vals))


application = webapp2.WSGIApplication([('/.*', MainHandler)],
                                      debug=True)