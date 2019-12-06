import urllib.parse, urllib.request, urllib.error, json

#application ID: 5df38ba5
#application key:30589e1f9f7a3953ed9b6ec2e893495e
baseurl = "https://api.edamam.com/search"
app_key = "30589e1f9f7a3953ed9b6ec2e893495e"
application_id = "5df38ba5"

def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)

def safeGet(url):
    try:
        return urllib.request.urlopen(url)
    except urllib.error.HTTPError as e:
        print("The server couldn't fulfill the request.")
        print("Error code: ", e.code)
    except urllib.error.URLError as e:
        print("We failed to reach a server")
        print("Reason: ", e.reason)
    return None

def getRecipes(q, params={}):
    params['app_key'] = app_key
    params['app_id'] = application_id
    params['q'] = q
    url = baseurl + "?" + urllib.parse.urlencode(params)
    safeurl = safeGet(url)
    if safeurl is None:
        return None
    return json.load(safeurl)



recipes = getRecipes("fried rice")
recipes = recipes['hits'][1]['recipe']




class Recipe():
    def __init__(self, recipeDict):
        self.title = recipeDict['label']
        self.image = recipeDict['image']
        self.link = recipeDict['url']
        self.numIngredients = len(recipeDict['ingredients'])
        self.servesPeople = recipeDict['yield']

r1 = Recipe(recipes)
print(r1.title)
print(r1.image)
print(r1.link)
print(r1.numIngredients)
print(r1.servesPeople)



