# Author Pei-Chen Tsai aka Hammer
# Keep low, if you found this useful. feel free to contact me.
from cStringIO import StringIO
from lxml import etree
from pprint import pprint
import urllib
import urllib2
import sys
import os
from subprocess import Popen
from subprocess import PIPE

global DB_FLT, DB_NOR, DB_ARG, DB_VER #verbose print
global TYPE_P, TYPE_H, TYPE_LI
global ARGUDB #arugment database
global ARGUDB_IDX_T, ARGUDB_IDX_P, ARGUDB_IDX_H, ARGUDB_IDX_LI
global TARGET_PASSWORD, TARGET_VIDEO_URL
global password
global doIt
global newerPage
global outputPath

oututPath = ''
doIt = 1
newerPage = ''
DB_FLT, DB_NOR, DB_ARG, DB_VER    = range(4)
TYPE_P, TYPE_H, TYPE_LI, TYPE_PRE = range(4)
TARGET_PASSWORD, TARGET_VIDEO_URL = range(2)
ARGUDB        = []
ARGUDB_IDX_T, ARGUDB_IDX_P, ARGUDB_IDX_H, ARGUDB_IDX_LI = range(4)

def DB(level,msg):
   if int(level) == int(DB_FLT) :
      print msg

def parseByLine(text):
   ret = 'none'
   lines = text.split('\n')
   for line in lines:
      print "LINE:"+line
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
   target = []
   doAgain = 0
   if TARGET == TARGET_PASSWORD:
      for e in iList:      
         if e.text is not None:                        
            #DB(1,e.text)
            target = parseByLine(e.text)
   elif TARGET == TARGET_VIDEO_URL:
      for e in iList:
         if e.text is not None:            
            if e.get('href') is not None:
               DB(1,e.get('href'))
               doAgain = 0
               try:
                  e.get('href').index('http://hdx3.blogspot.tw')
                  target.append([e.text,e.get('href')])
               except ValueError:
                  DB(1,"I am not interesting in this url..try another one")                  
                  doAgain = 1
            if doAgain == 1 :
               if e.get('href') is not None:
                  try:
                     e.get('href').index('http://hornydragon.blogspot.tw')
                     target.append([e.text,e.get('href')])
                  except ValueError:
                     DB(1, "still can't find interesting stuff")
                  
               
   return target

def handler_list(iList):      
   DB(1,'ENTER handler_video')
   cnt = len(iList)
   DB(1, 'There are '+str(cnt)+' interesting stuff found')
   ret = targetMatch(iList,TARGET_VIDEO_URL)
   DB(1, '%d found ' %(len(ret)))
   for entry in ret:
      print entry[0]+':'+entry[1]
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
   ret = []
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
   #etree.strip_tags(tree,'')
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
   myList = tree.xpath("//div[@class='blog-posts hfeed']//a")
   ret = handler_list(myList)   
   myList2 = tree.xpath("//a[@class='blog-pager-newer-link']")
   global doIt
   global newerPage
   if len(myList2) > 0 :
      print "newer index page found!"
      for e in myList2:
         if e.get('href') != None:
            print e.get('href')
            newerPage = e.get('href')
   else :
      doIt = 0 
   
   return ret

def assignPageAndOverrideArgu():
   DB(DB_ARG,'ENTER overrideArgu')
   global newerPage
   newerPage = sys.argv[1];
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

def prepareSinglePony(page,outputPath):
   iOut =[]
   iOut.append('python')
   iOut.append('ponyFetcher.py')
   iOut.append(page)
   iOut.append(outputPath)
   iOut.append('0')
   return iOut

def main():
   while doIt == 1 :
      myList = blogspotParser(newerPage)
      for e in myList:
         print e
         process = Popen(prepareSinglePony(e[1],outputPath))
         process.wait()
         #raw_input()

   #data = {'act':'checkPasswd','mediumId':'18132847','passwd':password}
   #f = urllib2.urlopen(
   #      url = sourcePage,
   #      data = urllib.urlencode(data)
   #      )
   #print f.read()

def verify():
   if len(sys.argv) < 3 or len(sys.argv) > 4 :
      print "command format is: "
      print sys.argv[0]+" <ANIMA_NAME> <outputPath> <DB>"
      print "--"
      print "you need to input <ANIMANNAME> <outputPath>"
      print "ANIMANAME now is provided by perform0.sh"
      print "DB is option"      
      exit()
   if len(sys.argv) == 4 :
      global DB_FLT
      global outputPath
      DB_FLT = int(sys.argv[3])
      outputPath = sys.argv[2]

if __name__ == '__main__':
   verify()
   #loadArgumentDb()
   assignPageAndOverrideArgu()
   main()
