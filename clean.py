
"""
Author: Meixian Chen
"""



import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json



lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

# creating info
CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

# Reshape the element in a more logical (json) format
def shape_element(element):
    node = {}
    if element.tag == "node" or element.tag == "way" :
        # reshape node type
        node['type'] = element.tag
        for term in element.iter():
            if term.tag =="node":
                # store creasting infor in node[created] dictionary
                node['created']={}
                if 'lon' in term.attrib.keys():
                    node['pos'] = [0,0]
                for key in term.attrib.keys():
                    if key in CREATED:
                        node['created'][key] = term.attrib[key]
                    # rewrite latitude and longitude in position
                    elif key == 'lat':
                        node['pos'][0] = float(term.attrib[key])
                    elif key == 'lon':
                        node['pos'][1] = float(term.attrib[key])
                    else: node[key] = term.attrib[key]

            if term.tag == 'nd':
                # put reference nodes into a list
                if 'node_refs' not in node:
                    node['node_refs'] = []
                node['node_refs'].append(term.get('ref'))


            # the main part, reshape the tag node
            if term.tag == 'tag':

                k = term.get('k')
                if k is None:
                    continue

                # first clean the tags of which we found problem in audit.py
                # address info
                if k.startswith("addr") and re.match(lower_colon,k):
                    ks = k.split(":")
                    if ks[0] == "addr":
                        ks[0] = "address"
                    if ks[1] == "postcode" and not term.get('v').startswith('8'):
                        # eliminate node which is not in cantone zurich
                        return None
                    if not ks[0] in node:
                        node[ks[0]] = {}
                    elif not isinstance(node[ks[0]],dict):
                        # if ks[0] is already in node but it is a dict
                        # convert it to dict
                        tmp = node[ks[0]]
                        node[ks[0]] ={"default":tmp}
                    if (not ks[1] in node[ks[0]]) and isinstance(node[ks[0]], dict):
                        # store key-value pair
                        node[ks[0]][ks[1]]=term.get('v')

                # name info
                elif k.startswith("name") and re.match(lower_colon,k):
                    # multipul name tag in different languages (name could be the same)
                    #<tag k="name:de" v="Kleinikon"/>
                    #<tag k="name:eg" v="Kleinikon"/>
                    #<tag k="name:cn" v="something"/>
                    # => name: set([Kleinikon, something])
                    ks = k.split(":")
                    # deal with name:botanical, name:source, name:left
                    if ks[1] in ["botanical","source","left"]:
                        node[ks[1]] = term.get('v')
                    else:
                        if ks[0] not in node:
                            node[ks[0]] = []
                        elif not isinstance(node[ks[0]],list):
                            # if there is already a name tag field, convert it to a list
                            tmp = node[ks[0]]
                            node[ks[0]] =[tmp]
                        if term.get('v') not in node[ks[0]]:
                            node[ks[0]].append(term.get('v'))

                #name info
                elif "name" in k and re.match(lower,k) and "_" in k:
                    # convert 'alt_name', 'old_name', "name_old","official_name" ...
                    # into a name list
                    if "name" not in node:
                        node["name"] = term.get('v')
                    elif not isinstance(node['name'],list):
                        tmp = node['name']
                        node['name'] = [tmp]
                    if term.get('v') not in node['name']:
                        node['name'].append(term.get('v'))

                 # # check recycling tag
                 # <tag k="recycling:paper" v="no"/>
                 #<tag k="recycling:clothes" v="yes"/>
                 #<tag k="recycling:cans" v="yes"/>
                 # -> recycling:[clothes,cans]
                elif k.startswith("recycling") and re.match(lower_colon,k):
                    ks = k.split(":")
                    if ks[0] not in node:
                        node[ks[0]] = []
                    elif not isinstance(node[ks[0]],list):
                             # if there is already a name tag field, convert it to a list
                        tmp = node[ks[0]]
                        node[ks[0]] =[tmp]
                    if ks[1] not in node[ks[0]] and term.get('v')=="yes":
                        node[ks[0]].append(ks[1])

                # other k value:
                elif re.match(lower,k):
                    node[k] = term.get('v')
                elif re.match(lower_colon,k):
                    ks = k.split(":")
                    if not ks[0] in node:
                        node[ks[0]]={}
                    elif not isinstance(node[ks[0]],dict):
                        tmp = node[ks[0]]
                        node[ks[0]] = {tmp:tmp}
                    if (not ks[1] in node[ks[0]]) and isinstance(node[ks[0]], dict) :
                        node[ks[0]][ks[1]]=term.get('v')


        return node
    else:
        return None


def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "../data/clean.json"
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data




if __name__ == "__main__":
    process_map('../data/zurich_switzerland.osm', True)
