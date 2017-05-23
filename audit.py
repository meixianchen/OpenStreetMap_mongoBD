"""
Author: Meixian Chen
"""

import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json


# check if the postcode and country code is vaild
def postcode_and_country(file_in):
    postcode_set = set()
    country_set = set()
    for _, element in ET.iterparse(file_in):
        if element.tag == "tag":
            if element.get('k') == "addr:postcode":
                postcode_set.add(element.get('v'))
            if element.get('k') == "addr:country":
                country_set.add(element.get('v'))
    print "The country code of Switzerland is CH."
    print "The country codes we found from the sample includes:"
    print country_set

    print "\nWe focus on Cantone Zurich, whose postcode should be like 8XXX."
    print "The postcode we found from the sample:"
    print postcode_set
    print "(We should eliminate the tag with postcode 5XXX)"



# check the Name tag
#
# name tag of different languages: <tag k="name:de" v="Kleinikon"/>
# different key for "name": 'alt_name', 'old_name', "name_old","official_name"...
# source of name: <tag k="name:source" v="OGD-stzh_stadtplan"/> <tag k="name:source" v="knowledge"/>
# botanical name:  <tag k="name:botanical" v="Tilia cordata"/>

def name_language(file_in):
    name_tag = re.compile(r'name:([a-z]|_)*$')
    languages = {}
    name_type = set()
    for i, element in ET.iterparse(file_in):
        if element.tag == "tag":
            if re.match(name_tag,element.get('k')):
                l = element.get('k').split(":")[1]
                if l not in languages:
                    languages[l] = 0
                languages[l] +=1
            if "name" in element.get('k') and ":" not in element.get('k'):
                name_type.add(element.get('k'))
        if len(languages)>150:
            break
    print "Switzerland has four official languages, "
    print "and many people from different countries living in Zurich."
    print "The name tags from the data are many different language:"
    print languages

    print "\nThe most frequent are: de (German), gsd (Swiss German)."
    print "Beside, \"source\", \"left\" and \"botanical\" should be treated different from the language tag in data cleaning."

    print "\nThere are different ways to call the tag name, which should also be uniformed:"
    print name_type



# check recycling tag
# <tag k="recycling:paper" v="no"/>
#<tag k="recycling:clothes" v="yes"/>
def recycling(file_in):
    recycling_type = set()
    recycling_good = set()
    recycling_possibility = set()
    for i, element in ET.iterparse(file_in):
        if element.tag == "tag":
            k = element.get('k')
            if "recycling" in k:
                if ":" in k:
                    recycling_good.add(k.split(":")[1])
                    recycling_possibility.add(element.get('v'))
                else:
                    recycling_type.add(k +": "+ element.get('v'))
    print "Different places for recyclying:"
    print recycling_type
    print "\nRecyclying objects:"
    print recycling_good
    print "\nPossibility of recyclying"
    print recycling_possibility
    print "(There is no \"unknown\" values)"



if __name__ == "__main__":
    #postcode_and_country("../data/sample10.osm")
    name_language("../data/zurich_switzerland.osm")
    #traffic("../data/zurich_switzerland.osm")
    #recycling("../data/sample10.osm")
