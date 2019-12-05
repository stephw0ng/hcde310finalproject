#import urllib, json, urllib2
#import jinja2, os, logging,
import urllib.request, urllib.error, urllib.parse, json, webbrowser



JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'], autoescape=True)

def test():
    print("hi")