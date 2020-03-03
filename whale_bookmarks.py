# Copyright (c) 2020 Heepie <gheepie@gmail.com>
#
# MIT Licence. See http://opensource.org/licenses/MIT
# Created on 2020-02-22

import json
import os
import sys
from collections import namedtuple
from pprint import pprint

inputPath = os.getenv('whale_path')
defaultPath = '~/Library/Application Support/Naver/Whale/Profile 1/bookmarks'

if inputPath:
	WhaleBookMarkPath = os.path.expanduser(inputPath)
else:
	WhaleBookMarkPath = os.path.expanduser(defaultPath)

Bookmark = namedtuple('Bookmark', 'name url')

bookMarkList = []
def searchItem(targetJson):
    if('children' in targetJson):
        searchItem(targetJson['children'])
    else:
        for item in targetJson:
            if ('children' in item):
                searchItem(item['children'])
            else:
                bookMarkList.append(Bookmark(item['name'],item['url']))

class Parser():
   def __init__(self):
       self.bookMarkList = []

   @classmethod
   def parseForJson(self, file):
       if (os.path.exists(file) == False):
           print('There is no json file')
           return

       with open(file) as json_file:
           json_data = json.load(json_file)
           root = json_data["roots"]
           bookMarkRoot = root["bookmark_bar"]
           targetRoot = bookMarkRoot["children"]

           searchItem(targetRoot)

class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)

def main():
   Parser.parseForJson(WhaleBookMarkPath)
   json.dump(dict(items=mapToAlfredJson()), sys.stdout, indent=2, sort_keys=True, cls=EnhancedJSONEncoder)
   return 0

def mapToAlfredJson():
    alfredJsonList = []
    for item in bookMarkList:
        alfredJsonList.append(dict(
            title=item.name,
            subtitle=item.url,
            arg=item.url,
            uid=item.url,
            valid=True,
        ))
    return alfredJsonList

if __name__ == "__main__":
    code = main()
    sys.exit(code)
