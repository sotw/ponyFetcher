# Author Pei-Chen Tsai aka Hammer
# Keep low, if you found this useful. feel free to contact me.
from cStringIO import StringIO
from lxml import etree
from pprint import pprint
import urllib
import urllib2
import sys
import os
import re
import time
from subprocess import Popen
from subprocess import PIPE

global DB_FLT, DB_NOR, DB_ARG, DB_VER #verbose print
global TYPE_P, TYPE_H, TYPE_LI
global ARGUDB #arugment database
global ARGUDB_IDX_T, ARGUDB_IDX_P, ARGUDB_IDX_H, ARGUDB_IDX_LI
global tPage
global TARGET_PASSWORD, TARGET_VIDEO_URL
global password
global TITLE
global outputPath

DB_FLT, DB_NOR, DB_ARG, DB_VER    = range(4)
TYPE_P, TYPE_H, TYPE_LI, TYPE_PRE = range(4)
TARGET_PASSWORD, TARGET_VIDEO_URL = range(2)
ARGUDB        = []
ARGUDB_IDX_T, ARGUDB_IDX_P, ARGUDB_IDX_H, ARGUDB_IDX_LI = range(4)
tPage         = ''
password = []
outputPath = ''

def DB(level,msg):
   if int(level) == int(DB_FLT) :
      print "PID:"+str(os.getpid())+":"+msg

def parseByRe(text):
   ret = []
   #DB(1, repr(text))
   resultList=re.findall('&#23494;&#30908;&#65306;[0-9]+',text)
   #resultList= re.findall(u'\u5bc6\u78bc\uff1a[0-9]+',text)
   for e in resultList:
      DB(1,e)
      #eAry = e.split(u'\uff1a')
      eAry = e.split('&#65306;')
      ret.append(eAry[1])
   return ret

def parseByRe2(text):
   ret = []
   #DB(1, repr(text))
   resultList=re.findall('"no" src="(.+)" width=',text)
   for e in resultList:
      DB(1,"========")
      e = e.split('?')
      DB(1,e[0])
      DB(1,"========")
      ret.append(e[0])
   if len(resultList) == 0:
      resultList=re.findall('marginheight="0" src="(.+)" width=',text)
      for e in resultList:
         DB(1,"********")
         e = e.split('?')
         DB(1,e[0])
         DB(1,"********")
         ret.append(e[0])
   return ret


def parseByLine(text):
   ret = 'none'
   lines = text.split('\n')
   for line in lines:
      DB(1,"LINE:"+line)
      if len(line) > 1:
         #print '#'+line                  
         #print repr(line)
         eAry = line.split(u'\uff1a')
         #print len(eAry)
         if len(eAry) >= 2 :
            #print repr(eAry[0])
            if eAry[0] == u'\u5bc6\u78bc': #password in T-Chinese
               DB(1, 'Found password:'+eAry[1])
               ret = eAry[1]
   return ret

def targetMatch(iList,TARGET):
   DB(1,'targetMatching...')
   target=[]
   
   if TARGET == TARGET_PASSWORD:
      for e in iList:      
         if e.text is not None:                        
            DB(1,e.text)
            #target = parseByLine(e.text)
            target = parseByRe(e.text)
   elif TARGET == TARGET_VIDEO_URL:
      for e in iList:
         if e.get('href') is not None:
            DB(1,e.get('href'))
            try:
               e.get('href').index('http://vlog.xuite.net/play/')
               target.append(e.get('href'))
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
   #etree.strip_tags(tree,'br')
   #etree.strip_tags(tree,'strong')
   #etree.strip_tags(tree,'img')
   etree.strip_tags(tree,'span')
   #etree.strip_tags(tree,'iframe')
   #etree.strip_tags(tree,'code')   
   
   result = etree.tostring(tree.getroot(), pretty_print=True, method="html")
   #DB(1, result)
   #DB(DB_VER, result)
   passwordList = parseByRe(result)
   videoPage = parseByRe2(result)
   targetURL = ""
   lineSum = 0   
   #myList = tree.xpath("//h3[@class='post-title entry-title']") #title
   for iranai in tree.xpath("//div[@class='separator']"):
      DB(1, 'remove 1 separator!')
      iranai.getparent().remove(iranai)
   for iranai in tree.xpath("//div[@class='sitemajiad']"):
      DB(1, 'remove 1 stemajiad!')
      iranai.getparent().remove(iranai)
   for iranai in tree.xpath("//a[@name='more']"):
      DB(1, 'remote 1 a more!')
      iranai.getparent().remove(iranai)
   for iranai in tree.xpath("//iframe"):
      DB(1, 'remote 1 iframe!')
      iranai.getparent().remove(iranai)
   for iranai in tree.xpath("//div[@class='post-body entry-content']/div"):
      DB(1, 'remote 1 div!')
      iranai.getparent().remove(iranai)
   etree.strip_tags(tree,'br')
   myList = tree.xpath("//div[@class='post-body entry-content']")
   global password
   #passwordList = handler_password(myList)
   for pas in passwordList:
     print "Got password:"+pas
     password.append(pas)
   #if password == 'none':
   #   print etree.tostring(tree.getroot(), pretty_print=True, method="html")

   #aHrefList = tree.xpath("//div[@class='post-body entry-content']//a")
   global TITLE
   TITLE = 'none'
   TITLE = tree.xpath("//title")[0].text
   #handler_video(aHrefList)
   #videoPage = handler_video(aHrefList)
   for aPage in videoPage:
      DB(1,"Got video http url:(%s)" %(aPage))
      aPage = aPage.replace('embed','play',1)
      aPage = aPage+"?html5=1" #enable html5
      DB(1,"enable html5:(%s)"%(aPage))
      ret.append(aPage)
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

def prepareXuite(mPage,PASSWORD,TITLE,outputPath):
   iOut =[]
   iOut.append('python')
   iOut.append('xuiteManipulate.py')
   iOut.append(mPage)
   iOut.append(PASSWORD)
   iOut.append(TITLE)
   iOut.append(outputPath)
   iOut.append('0')
   return iOut

def main():
   cd = 3
   sourcePageList = blogspotParser(tPage)
   while len(sourcePageList) == 0 and cd > 0: 
      print "ok, can't find any sourcePage, maybe we can retry "
      time.sleep(1)
      sourcePageList = blogspotParser(tPage)
      cd -= 1
   print "===== START OUTPUT ====="
   cnt = 0
   if len(sourcePageList) == 0:
      f = open('errorReport.txt','a')
      f.write(tPage+'\n')
      f.close()

   for aPage in sourcePageList:
      print aPage+":"+password[cnt]+":"+outputPath
      process = Popen(prepareXuite(aPage,password[cnt],TITLE,outputPath))
      process.wait()
      cnt+=1
   print "===== END OUTPUT ====="

   #data = {'act':'checkPasswd','mediumId':'18132847','passwd':password}
   #f = urllib2.urlopen(
   #      url = sourcePage,
   #      data = urllib.urlencode(data)
   #      )
   #print f.read()

def verify():
   global outputPath
   if len(sys.argv) < 3 or len(sys.argv) > 4 :
      print "command format is: "
      print sys.argv[0]+" <PAGE> <outputPath> <DB>"
      print "--"
      print "you need to input <PAGE> <outputPath>"
      print "DB is option"      
      exit()
   if len(sys.argv) == 4 :
      global DB_FLT
      DB_FLT = int(sys.argv[3])
      outputPath = sys.argv[2]
   print "DB_FLT:"+str(DB_FLT)
   print "outputPath:"+outputPath

if __name__ == '__main__':
   verify()
   #loadArgumentDb()
   assignPageAndOverrideArgu()
   main()
