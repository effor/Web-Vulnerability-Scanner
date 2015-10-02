#----------------Google search query info------------------#
# spaces are converted to +
# query is given by ?q=query
# page is given by the index of the first search result,
# i.e. &start=20
# sample query: http://www.google.se/search?q=cp+nice&start=20
#----------------------------------------------------------#
from Search import Search
from Proxy import Proxy
import urllib.request
import urllib.parse
import re
import bcolors
import time
import random
import data

# The following class will handle the google searches and the
# google url scraping. It should be able to conduct multiple searches
# and return the links without issue.
class Google(Search) :
        
    #Conducts the main search
    def conduct_search(self, query, pages) :
        query = query.replace(" ", "+")
        if (self.useproxy) :
            super(Google, self).update_proxy(True)
        if (self.verbose) :
            bcolors.printBold("Conducting google search...")
        page = 0
        while (page < pages) :
            # wait between 0 and self.sleep seconds
            time.sleep(random.randrange(self.sleep))
            try :
                self._get_page(query, page)
            except Exception as e:
                super(Google,self).fatal_exception(e)
            page += 1
        if (self.verbose) :
            super(Google, self).print_urls()
            
    def _get_page(self, query, page) :
        n = 1 # the nr of the link scraped
        # Acquire url from data and get the html tree for the page
        url = data.get_google_pageURL(query, page)
        if (self.useproxy) :
            self.proxyhandler.validate_proxy()
        tree = super(Google, self).get_html(url)
        
        while (True) :
            url = self._get_url(tree, n)
            n += 1
            if (url == [] or url == "[]") : break
            # Here we append the urls
            self.urls.append(url)
        
    def _get_url(self, tree, nr) :
        url = tree.xpath(data.get_google_xpath(nr))
        url = str(url)
        url = urllib.parse.unquote(url)
        url = self._strip_url(url)
        return url
    
    # Strips the url gathered by the scraper.
    # This is necessary since each url is a request
    # to google.
    def _strip_url(self, link) :
        regex = '(?=&sa=).+'
        url = ''.join(link)
        url = url.replace("['/url?q=", "")
        url = re.sub(regex, '', url)
        if (self.verbose) :
            bcolors.printGreen("[+]Extracted url: " + url)
        return url
    
    def get_urls(self) :
        return self.urls
    def reset_urls(self) :
        self.urls = []
        
if __name__ == '__main__' :
    print("Running test...")
    g = Google(True, 10, True)
    g.conduct_search("Agent Orange", 20)
    print(str(g.get_urls()))