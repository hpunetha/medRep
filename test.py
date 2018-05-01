import pywikibot

import mwparserfromhell


enwp = pywikibot.Site('en', 'wikipedia')
page = pywikibot.Page(enwp, 'Common cold')
wikitext = page.get()
wikicode = mwparserfromhell.parse(wikitext)
# templates = wikicode.filter_templates()
# print(templates)
print(wikicode)
# for a in templates:
#     print(a)

import requests

url1 = "https://en.wikipedia.org/wiki/Common_cold"

r =requests.get(url1)