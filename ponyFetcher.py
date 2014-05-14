# Author Pei-Chen Tsai aka Hammer
# Ok, the line break position is impossible to 100% accurate currently, so just tune global parameter for your own purpose
from cStringIO import StringIO
from lxml import etree
from pprint import pprint
import urllib
import urllib2
import sys
import os

global DB_FLT, DB_NOR, DB_ARG, DB_VER #verbose print
global TYPE_P, TYPE_H, TYPE_LI
global ARGUDB #arugment database
global ARGUDB_IDX_T, ARGUDB_IDX_P, ARGUDB_IDX_H, ARGUDB_IDX_LI
global tPage
global TARGET_PASSWORD, TARGET_VIDEO_URL
global password

DB_FLT, DB_NOR, DB_ARG, DB_VER    = range(4)
TYPE_P, TYPE_H, TYPE_LI, TYPE_PRE = range(4)
TARGET_PASSWORD, TARGET_VIDEO_URL = range(2)
ARGUDB        = []
ARGUDB_IDX_T, ARGUDB_IDX_P, ARGUDB_IDX_H, ARGUDB_IDX_LI = range(4)
tPage         = ''

def DB(level,msg):
   if int(level) == int(DB_FLT) :
      print msg

def parseByLine(text):
   ret = 'none'
   lines = text.split('\n')
   for line in lines:
      if len(line) > 1:
         #print '#'+line                  
         #print repr(line)
         eAry = line.split(u'\uff1a');
         #print len(eAry)
         if len(eAry) >= 2 :
            #print repr(eAry[0])
            if eAry[0] == u'\u5bc6\u78bc': #password in T-Chinese
               print 'Found password:'+eAry[1]
               ret = eAry[1]
   return ret

def targetMatch(iList,TARGET):
   DB(1,'targetMatching...')
   target='none'
   
   if TARGET == TARGET_PASSWORD:
      for e in iList:      
         if e.text is not None:                        
            #DB(1,e.text)
            target = parseByLine(e.text)
   elif TARGET == TARGET_VIDEO_URL:
      for e in iList:
         if e.get('href') is not None:
            DB(1,e.get('href'))
            try:
               e.get('href').index('http://vlog.xuite.net/play/')
               target=e.get('href')
            except ValueError:
               DB(1,"I am not interesting in this url")
   return target

def handler_video(iList):      
   DB(1,'ENTER handler_video')
   cnt = len(iList)
   DB(1, 'There are '+str(cnt)+' interesting stuff found')
   ret = targetMatch(iList,TARGET_VIDEO_URL)
   DB(1, 'LEAVE handler_video')
   return ret

def handler_password(iList):      
   DB(1,'ENTER handler_password')
   cnt = len(iList)
   DB(1, 'There are '+str(cnt)+' interesting stuff found')
   ret = targetMatch(iList,TARGET_PASSWORD)
   DB(1, 'LEAVE handler_password')
   return ret

def blogspotParser(tPage):
   ret = 'none'
   DB(1,'tPage='+tPage)
   resp = urllib2.urlopen(tPage)
   if resp.code == 200 :
      data = resp.read()
      resp.close()
   elif resp.code == 404 :
      print "page do not exist"
      exit()
   else :
      print "can not open page"
      exit()
   parser = etree.HTMLParser()
   tree = etree.parse(StringIO(data), parser)
   #etree.strip_tags(tree,'br')
   #etree.strip_tags(tree,'strong')
   #etree.strip_tags(tree,'img')
   etree.strip_tags(tree,'span')
   #etree.strip_tags(tree,'code')   
   
   #result = etree.tostring(tree.getroot(), pretty_print=True, method="html")
   #DB(1, result)
   #DB(DB_VER, result)

   targetURL = ""
   lineSum = 0   
   #myList = tree.xpath("//h3[@class='post-title entry-title']") #title
   for iranai in tree.xpath("//div[@class='separator']"):
      #print '1 remove separator!'
      iranai.getparent().remove(iranai)
   etree.strip_tags(tree,'br')
   myList = tree.xpath("//div[@class='post-body entry-content']")
   global password
   password = handler_password(myList)   
   print "Got password:"+password

   aHrefList = tree.xpath("//div[@class='post-body entry-content']//a")
   videoPage = handler_video(aHrefList)
   print "Got video http url:(%s)" %(videoPage)
   videoPage = videoPage+"?html5=1" #enable html5
   print "enable html5:(%s)"%(videoPage)
   ret = videoPage
   return ret

def assignPageAndOverrideArgu():
   DB(DB_ARG,'ENTER overrideArgu')
   global tPage
   tPage = sys.argv[1];
   #DB(DB_ARG,'target is:'+tPage)
   DB(DB_ARG,'LEAVE overrideArgu')

def loadArgumentDb():
   DB(DB_ARG,'ENTER loadArgumentDb')
   if os.path.isfile('./argumentDataBase') is True:
      f = open('argumentDataBase','r')
      if f is not None:
         for line in f :
            if line != '\n' and line[0] != '#':
               line = line.rstrip('\n')
               global ARGUDB
               ARGUDB.append(line)
         f.close()
   else:
      DB(DB_ARG,'override file is not exist')
   DB(DB_ARG,'LEAVE loadArgumentDb')

def main():
   sourcePage = blogspotParser(tPage)
   data = {'act':'checkPasswd','mediumId':'18132847','passwd':password}
   f = urllib2.urlopen(
         url = sourcePage,
         data = urllib.urlencode(data)
         )
   print f.read()

def verify():
   if len(sys.argv) < 2 or len(sys.argv) > 3 :
      print "command format is: "
      print sys.argv[0]+" <PAGE> <DB>"
      print "--"
      print "you need to input <PAGE>"
      print "DB is option"      
      exit()
   if len(sys.argv) == 3 :
      global DB_FLT
      DB_FLT = int(sys.argv[2])

if __name__ == '__main__':
   verify()
   #loadArgumentDb()
   assignPageAndOverrideArgu()
   main()
