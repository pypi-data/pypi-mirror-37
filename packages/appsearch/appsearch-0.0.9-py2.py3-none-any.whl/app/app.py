# encoding: utf-8
import os
import re
import sys
import json
import getopt

reload(sys)
sys.setdefaultencoding('utf-8')

try:
    from urllib import parse, request
except ImportError:
    import urllib2
    import urllib
    
def searchApp(platform, query, appName, verbose = False, showAll=False):
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

    isPython2 = (sys.version_info.major == 2)
    if(isPython2):
        reqUrl = '%s%s%s' % (url, '?', urllib.urlencode(request_data))
        req = urllib2.Request(url = reqUrl, headers= headers)
        res = urllib2.urlopen(req).read()
    else:
        reqUrl = '%s%s%s' %(url, '?', parse.urlencode(request_data))
        req = request.Request(url = reqUrl, headers = headers)
        res = request.urlopen(req).read().decode('utf-8')

    requestUrlString = req.get_full_url() if isPython2 else req.full_url    
    if(verbose == True):
        print(requestUrlString) 

    apps = json.loads(res).get('data')

    iphone_app_names = ['美团功能测试', 'imeituan-admittance-test']
    android_app_names_pattern = r'group_.*_meituan_meituaninternaltest'

    def appFilter(app):
        ret = False
        appName = app.get('appName')

        if(platform == 'iphone'):
            ret = appName in iphone_app_names
        else:
            ret = re.match(android_app_names_pattern, appName, re.IGNORECASE)

        return ret


    filteredApps = apps if showAll else filter(appFilter, apps) if isPython2 else list(appFilter, apps)
    if(filteredApps == None or len(filteredApps) == 0):
        print('搜索无结果')
        return

    for app in filteredApps: 
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
        downloadUrl = filePath + '.ipa' if platform == 'iphone' else url
        apptestPage = apptestPageBase % id

        verboseOutput = \
        '''
        %s(%s):

            apptest page: %s

            download url: %s 
        ''' % (appChineseName, version, apptestPage, downloadUrl)

        if(verbose):
            print(verboseOutput)
        else:
            print('%s(%s):  %s' % (appChineseName, version, downloadUrl if platform == 'android' else apptestPage))

def parseArgs(argv):

    try:
        (opts, args) = getopt.getopt(argv,"vtrha", ["--no-filter"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    platform = 'iphone'
    appName = ''
    query = args[0] if len(args) > 0 else None
    verbose = False
    allApp = False

    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt in ("-a"):
            platform = 'android'
        elif opt in ("-v"):
            verbose = True
        elif opt in ("--no-filter"):
            allApp = True

    if(query and len(query) > 0):
        searchApp(platform, query, appName, verbose=verbose, showAll=allApp)

    
def usage():
    usage = '''
Search app package url for JIRA Task, default for iPhone Platform

Usage: appsearch [ -a ] [ -v ] query-content

    -a                  search for android
    -v                  verbose output
    --no-filter         don't filter the results with iMeituan App Test filter

    query-content       can be build number or version number or appName

Example:
    Search iphone iMeituan app with build number:
        
        Exp 1:
            appsearch 13231

        Exp 2: 
            appsearch 13346

    Search android iMeituan app with build number: 

        Exp 1: 
            appsearch -a 34666

        Exp 2: 
            appsearch -a 28777

Report Error:

    Author: joker
    Email: wangzhizhou@meituan.com
    Phone: (+86) 151-0227-2032
    '''
    print(usage)

def search():
    parseArgs(sys.argv[1:])

# For test
if __name__ == '__main__':
    search()
