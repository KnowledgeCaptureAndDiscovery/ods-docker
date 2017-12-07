import csv
import codecs
import cStringIO
import json
import requests

api_url = "http://organicdatacuration.org/enigma/api.php"
facts_url = api_url + "?action=wtfacts&operation=show&format=json&title="

query_url = api_url + "?action=query&"
categories_url = query_url + "list=allcategories&aclimit=500&format=json"
instances_url = query_url + "list=categorymembers&cmlimit=500&format=json&cmtitle="

session = requests.Session()
wgCore = "(L)"

# Collect facts recursively starting from a title
allfacts = {}


class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


def collectFacts(title, recurse=False):
    if title in allfacts:
        return allfacts[title]
    facts = {}
    # print("Collecting facts for {}".format(title))
    allfacts[title] = {}
    tfacts = session.get(facts_url + title).json()['wtfacts']['facts']
    for prop, fact in tfacts.items():
        if prop == "subobjects":
            continue
        propname = prop.replace(" " + wgCore, "")
        values = []
        valtype = None
        for value in fact['values']:
            valtype = value['type']
            if recurse and valtype == "WikiPage":
                collectFacts(value['val'])
            values.append(value['val'])
        facts[propname] = values
    allfacts[title] = facts
    return facts


def getCategoryProperties(category):
    properties = []
    cfacts = session.get(facts_url + "Category:" +
                         category).json()['wtfacts']['facts']
    if "Has property" in cfacts:
        for value in cfacts["Has property"]['values']:
            prop = value['val'].replace("Property:", "")
            propname = prop.replace("_" + wgCore, "")
            properties.append(propname)
    return sorted(properties)


def writeCollectionFile(category):
    category = category.replace(" ", "_")
    catname = category.replace("_" + wgCore, "")
    catfile = catname.lower() + ".csv"

    catprops = getCategoryProperties(category)
    if catprops:
        print("=============================")
        print("CATEGORY: " + catname)

        catprops.insert(0, catname)

        with open('csv/' + catfile, 'wb') as csvfile:
            csvwriter = UnicodeWriter(csvfile)
            csvwriter.writerow(catprops)

            for memberinfo in session.get(instances_url + "Category:" + category).json()['query']['categorymembers']:
                pagename = memberinfo['title']
                pfacts = collectFacts(pagename)
                row = [pagename]
                if pfacts is not None:
                    print("------------------")
                    print("PAGE: " + pagename)
                    for prop in catprops[1:]:
                        value = ";".join(pfacts.get(prop, []))
                        row.append(value)
                csvwriter.writerow(row)


# Collect all relevant categories and instances in the wiki
def collectCategories():
    for catinfo in session.get(categories_url).json()['query']['allcategories']:
        cat = catinfo["*"]
        if cat.endswith(wgCore):
            writeCollectionFile(cat)

collectCategories()
# collectFacts('SZCorticol')
# collectFacts('SZNegativeSymptoms')
# collectFacts('SZPositiveSymptoms')
# print(facts)
