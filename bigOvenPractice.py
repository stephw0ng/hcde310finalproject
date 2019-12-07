import urllib.parse, urllib.request, urllib.error, json

#application ID: 5df38ba5
#application key:30589e1f9f7a3953ed9b6ec2e893495e
edamambaseurl = "https://api.edamam.com/search"
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


# Method to get JSON from API
def getRecipes(q, params={}):
    params['app_key'] = app_key
    params['app_id'] = application_id
    params['q'] = q
    url = edamambaseurl + "?" + urllib.parse.urlencode(params)
    print(url)
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




# Grab the big JSON file of all the recipes
allRecipes = getRecipes("chicken", params={'health':'vegetarian''balanced'})

# Get only the list of recipes
allRecipes = allRecipes['hits']

# Put all of the recipes into Class Objects of Recipes
# into a list that will be passed to the HTML file
#listDictRecipes = [Recipe(x['recipe']) for x in allRecipes]

# Sorted the recipes in the list of Recipe objects
#sortedDictRecipes=sorted(listDictRecipes, key=lambda obj: obj.time)

print('testing sorted...')



# for obj in listRecipesObjects:
#     print("Photo: %s \nTitle: %s \nTime it takes: %s \nNumber of ingredients: %s \nNumber of people it serves: %s"%(obj.image, obj.title, obj.time, obj.numIngredients, obj.servesPeople))




