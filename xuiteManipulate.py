# Author Pei-Chen Tsai aka Hammer
# Keep low, if you found this useful. feel free to contact me.
from cStringIO import StringIO
from lxml import etree
from pprint import pprint
import urllib
import urllib2
import sys
import os
import json
import re
from subprocess import Popen
from subprocess import PIPE

global DB_FLT, DB_NOR, DB_ARG, DB_VER #verbose print
global TYPE_P, TYPE_H, TYPE_LI
global ARGUDB #arugment database
global ARGUDB_IDX_T, ARGUDB_IDX_P, ARGUDB_IDX_H, ARGUDB_IDX_LI
global tPage
global TARGET_PASSWORD, TARGET_VIDEO_URL
global PASSWD
global PARSE_STATEI,PASRSE_STATEII, PARSE_STATEIII
global fileTitle
global outputPath

fileTitle = 'none'
DB_FLT, DB_NOR, DB_ARG, DB_VER    = range(4)
TYPE_P, TYPE_H, TYPE_LI, TYPE_PRE = range(4)
TARGET_PASSWORD, TARGET_VIDEO_URL = range(2)
PARSE_STATEI,PARSE_STATEII = range(2)
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

   if TARGET == TARGET_VIDEO_URL:
      for e in iList:
         if e.text is not None:
            #DB(1,e.text)
            lines = e.text.split('\n')
            for line in lines:
               #print line
               line = line.rstrip(' ')
               line = line.lstrip(' ')
               #print line
               iEntrys = line.split(' ')
               #print len(iEntrys)
               if len(iEntrys) >= 4:                  
                  if iEntrys[1] == 'srcUrl':
                     target = iEntrys[3]
                     target = target.rstrip(';\r')
                     print repr(target)
   return target

def handler_passI(iList):      
   DB(1,'ENTER handler_passI')
   ret = 0
   cnt = len(iList)
   DB(1, 'There are '+str(cnt)+' interesting stuff found')
   ret = targetMatch(iList,TARGET_VIDEO_URL)
   DB(1, 'LEAVE handler_passI')
   return ret

def handler_passII(iList):
   ret = 0
   cnt = len(iList)
   DB(1, 'There are '+str(cnt)+' interesting stuff found')
   for entry in iList:
      if entry.get('data-mediaid') != None:
        ret = iList[0].get('data-mediaid')
   return ret

def prepareCurlPara(url,outputName):
   iOutput = []
   iOutput.append('curl')
   iOutput.append('-L')
   iOutput.append(url)
   iOutput.append('-o')
   iOutput.append(outputPath+'/'+outputName)
   return iOutput

def jsonExtractor(tPage):
   DB(1,'tPage='+tPage)
   ret = ['none','none']
   #resp = urllib2.urlopen(tPage)
   #if resp.code == 200 :
   #   data = resp.read()
   #   resp.close()
   #elif resp.code == 404 :
   #   print "page do not exist"
   #   exit()
   #else :
   #   print "can not open page"
   #   exit()
   req = urllib2.Request(tPage, None)
   opener = urllib2.build_opener()
   f = opener.open(req)
   paraBag = json.load(f)

   for mEntry in paraBag['media']:
      if type(paraBag['media'][mEntry]) == unicode :
        DB(1, mEntry+":"+paraBag['media'][mEntry])
      elif type(paraBag['media'][mEntry]) == bool :
         if paraBag['media'][mEntry] == True :
            DB(1, mEntry+":true")
         else:
            DB(1, mEntry+":false")
   

   location = 'none'
   global fileTitle 
   if paraBag['media']['html5HQUrl'] != '':
      location = paraBag['media']['html5HQUrl']
   elif paraBag['media']['html5Url'] != '':
      location = paraBag['media']['html5Url']

   if fileTitle != 'none':
      fileTitle = fileTitle.replace(' ','')
      retSet = re.findall('](.+)',fileTitle)
      if len(retSet) != 0 :
         fileTitle = retSet[0]
   elif paraBag['media']['TITLE'] != None:
      print paraBag['media']['TITLE']
      fileTitle = paraBag['media']['TITLE']
   
   #wholeFileName = fileTitle+"."+paraBag['media']['SRC_TYPE'].encode("UTF-8")
   wholeFileName = paraBag['media']['TITLE']+".mp4"
   #[]== orz.. I hate string encode coversion
   #print wholeFileName
   #wholeFileName = wholeFileName.encode('UTF-8')
   return [location, wholeFileName]

def xuiteParser(tPage, PARSE_STATE): 
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
   #etree.strip_tags(tree,'span')
   #etree.strip_tags(tree,'code')   
   
   #result = etree.tostring(tree.getroot(), pretty_print=True, method="html")
   #DB(1, result)
   #DB(DB_VER, result)

   targetURL = ""
   if(PARSE_STATE == PARSE_STATEI):
      myList = tree.xpath("//div[@id='single-video']/script")
      ret=handler_passI(myList) 
   elif(PARSE_STATE == PARSE_STATEII):
      myList = tree.xpath("//div[@id='play-hiddendata']")
      ret=handler_passII(myList)
   return ret

def assignPageAndOverrideArgu():
   DB(DB_ARG,'ENTER overrideArgu')
   global tPage
   tPage = sys.argv[1];
   #DB(DB_ARG,'target is:'+tPage)
   DB(DB_ARG,'LEAVE overrideArgu')

def loadArgumentDb():
   DB(1,'ENTER loadArgumentDb')
   if os.path.isfile('./.argumentDataBase') is True:
      f = open('.argumentDataBase','r')
      if f is not None:
         for line in f :
            if line != '\n' and line[0] != '#':
               line = line.rstrip('\n')
               global ARGUDB
               ARGUDB.append(line)
         f.close()
   else:
      DB(1,'override file is not exist')
   DB(1,'LEAVE loadArgumentDb')

def isInsideDownloadedList(filename):
   for entry in ARGUDB :
      DB(1. entry)
      if entry == filename :
         return True
   return False

def main():
   #sourcePage = xuiteParser(tPage,PARSE_STATEI)
   #print sourcePage
   mId = xuiteParser(tPage, PARSE_STATEII)
   print mId
   finalTarget = ''
   finalTarget,title = jsonExtractor('http://vlog.xuite.net/_ajax/default/media/ajax?act=checkPasswd&mediumId='+mId+'&passwd='+PASSWD)
   print title
   print finalTarget
   if finalTarget == '':
      f = open('errorReport.txt','a')
      f.write('xuiteErr:'+tPage+" "+PASSWD+"\n")
      f.close()
   #print 'why stop?'
   if isInsideDownloadedList(title) == False :
      print 'new one, go downloading...'
      process = Popen(prepareCurlPara(finalTarget,title))
      process.wait()
      f = open('.argumentDataBase','a')
      f.write(title+"\n")
      f.close()
   else :
      print 'old one, skip'

def verify():
   global DB_FLT
   global PASSWD
   global fileTitle
   global outputPath
   outputPath = ''
   if len(sys.argv) < 5 or len(sys.argv) > 6 :
      print "command format is: "
      print sys.argv[0]+" <PAGE> <PASSWD> <fileTitle> <OUTPUTPATH> <DB>"
      print "--"
      print "You need to input <PAGE>"
      print "PASSWD is option"      
      exit()
   if len(sys.argv) == 6 :      
      DB_FLT = int(sys.argv[5])
      PASSWD = sys.argv[2]
      fileTitle = sys.argv[3]
      outputPath = sys.argv[4]
   elif len(sys.argv) == 5:         
      DB_FLT = int(sys.argv[4])
      fileTitle = sys.argv[2]
      outputPath = sys.argv[3]
   print "DB_FLT:"+str(DB_FLT)
   print "fileTitle:"+fileTitle
   print "outputPath:"+outputPath

if __name__ == '__main__':
   verify()
   loadArgumentDb()
   assignPageAndOverrideArgu()
   main()
