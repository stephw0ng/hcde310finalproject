import urllib.parse, urllib.request, urllib.error, json

api_key = "VnAC49a37JJMyA6aPbvMGymXVJbeIb4t"
baseurl = "http://api.nytimes.com/svc/"

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

def getMostViewed(period, params={}):
   params['api-key'] = api_key
   params['period'] = period
   url = baseurl + "mostpopular/v2/viewed/%s"%period +".json?" + urllib.parse.urlencode(params)
   safeurl = safeGet(url)
   if safeurl is None:
       return None
   return json.load(safeurl)

def articleSearch(searchwords, sort="relevance", params={}):
   params['api-key'] = api_key
   params['sort'] = sort
   #params['fq'] = "news_desk:(\"food\") AND subject:(\"" + searchwords + "\")"
   params['fq'] = "news_desk:(\"Food\" \"Business\" \"World\" \"Dining\" \"Environment\" \"Health\") AND " + searchwords

   url = baseurl + "search/v2/articlesearch.json?" + urllib.parse.urlencode(params)
   safeurl = safeGet(url)
   if safeurl is None:
       return None
   return json.load(safeurl)


class Article:
  def __init__(self, articledict):
      self.headline = articledict['headline']['main']
      self.summary = articledict['snippet']
      self.url = articlesDict['web_url']

      if len(articledict['byline']['person']) != 0:
       author = articledict['byline']['person'][0]
       self.author = author['firstname'] + " " + author['lastname']
      else:
       self.author = "No author"

      keywords = []
      for x in articledict['keywords']:
          keywords.append(x['value'])
      self.keywordslist = keywords




# Get the JSON from the API
searchdict = articleSearch("chicken teriyaki")
# Get the list of articlds
listArticles = searchdict['response']['docs']
# Put the articles into Article classes
articlesDict = [Article(article) for article in listArticles]



# mostviewed = getMostViewed(1)
# print(pretty(mostviewed))
# sections = []
# sortedlist = sorted(mostviewed['results'], key=lambda x: x['views'], reverse=True)
# for articledict in sortedlist:
#     sections.append((articledict['section'], articledict['views']))
# print(sections)



# articlesummaries = []
# keywords = []
# for dict in searchdict['response']['docs']:
#     keywords = []
#     for x in dict['keywords']:
#         keywords.append(x['value'])
#     title = dict['headline']['main']
#     snippet = dict['snippet']
#     articlesummaries.append({'title': title, 'keywords':keywords, 'snippet':snippet})
#

# for dict in articlesummaries:
#     print(dict['title'])
#     print(dict['snippet'])
#     print(dict['keywords'][:4])
#     print("\n")
