#!/usr/bin/env python3
import sys
import json
from urllib import parse,request
import os
import getopt

def searchApp(platform, query, appName, verbose = False):
    request_data = {
        'platform': platform,
        'query': query,
        'appName': appName
    }

    headers = {
        'Content-Type': 'application/json',
        'Accept' : '*/*',
        'Accept-Language': 'zh-cn'
    }

    url = 'http://apptest.sankuai.com/api/v2/searchPackage'
    apptestPageBase = 'https://apptest.sankuai.com/page/app/detail/%d'

    req = request.Request(url = '%s%s%s' %(url, '?', parse.urlencode(request_data)), headers = headers)
    res = request.urlopen(req).read().decode('utf-8')
    apps = json.loads(res).get('data')
    
    if(verbose):
        print(req.full_url)

    if(apps == None or len(apps) == 0):
        print("搜索无结果")
        return

    for app in apps: 
        id = app.get('id')
        url = app.get('url')
        appChineseName = app.get('appChineseName')
        iconUrl = app.get('iconUrl')
        version = app.get('version')
        createTime = app.get('createTime')
        branchId = app.get('branchID')
        groupId = app.get('groupId')
        branchName = app.get('branchName')

        (filePath, ext) = os.path.splitext(url)
        downloadUrl = filePath + '.ipa'
        apptestPage = apptestPageBase % id

        outputFormat = \
        '''
        %s(%s):

            apptest page: %s

            download url: %s 
        ''' % (appChineseName, version, apptestPage, downloadUrl)

        print(outputFormat)


def parseArgs(argv):

    try:
        opts, args = getopt.getopt(argv,"trha:q:", ["--appName=","--query="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    platform = 'iphone'
    appName = ''
    query = None
    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt in ("-t", "--test"):
            appName = '美团功能测试'
        elif opt in ("-r", "--release"):
            appName = 'imeituan-admittance-test'
        elif opt in ("-q", "--query"):
            query = arg
            print(arg)
        elif opt in ("-a", "--appName"):
            appName = arg

    if(len(opts) == 0):
        if(len(argv) > 0):
            query = argv[0]

    if(query):
        searchApp(platform, query, appName)
    
def usage():
    print('Usage: appsearch [ -r | -t | -h ] -q <query content> [ -a <appName> ]')


def search():
    parseArgs(sys.argv[1:])

# For test
if __name__ == '__main__':
    search()