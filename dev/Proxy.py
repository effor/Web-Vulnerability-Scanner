from lxml import html
import get_proxy
import urllib.request
import urllib.parse
import urllib.error
import data
import sys
import os
import bcolors

class Proxy() :
    def __init__(self, verbose = False) :
        self.blacklist = []
        self.currentHttpProxy = None
        self.currentHttpsProxy = None
        self.verbose = verbose
        self.myip = self.get_ip()
    
    def print_state(self) :
        bcolors.printBold("****Printing object state****")
        bcolors.printBold("PROXIES:\n")
        print("http: " + str(self.currentHttpProxy) + ", https: " + str(self.currentHttpsProxy))
        bcolors.printBold("Settings:\n")
        print("Your ip: " + str(self.myip))
        bcolors.printBold("Blacklist:\n")
        print(str(self.blacklist))
    
    #Private function
    #Pings a host to ensure it is alive
    def _ping(self, hostname) :
        response = os.system(data.pingWINDOWS + hostname + " > null")
        #Returns non-zero value if connection fails!
        if response == 0 :
            print(hostname)
            return True
        else :
            return False

    #Private function
    #Returns true if proxy is valid,
    #else returns false
    def _validate(self, proxy, https=None, google=None):
        #Socks proxy validation
        if (https == None and google == None) :
            if (str(proxy[2]) in data.validCountries and self._ping(str(proxy[0]))) :
                return True
            
        #HTTP proxy validation (checks google and https conditions)
        elif ((not https and proxy[6] == 'no') or (https and proxy[6] == 'yes')) :
            if ((not google and proxy[5] == 'no') or (google and proxy[5] == 'yes') or (google == None)) :
                if (str(proxy[2]) in data.validCountries and self._ping(str(proxy[0]))) :
                    return True
        return False
    
    #Public method
    #Acquires and installs a http and https proxy
    def proxify(self, https = True, google = True) :
        proxy = self.get_http_proxy(1, False, google)
        proxyhttps = None
        if (https == True) :
            proxyhttps = self.get_http_proxy(1, True, google)
            proxyhttps = self.format_proxies(proxyhttps)[0]
        proxy = self.format_proxies(proxy)[0]
        self.install_proxy(proxy, proxyhttps)   
    
    def blacklist_current_proxy(self, https = True) :
        if (not self.currentHttpProxy == None) :
            self.blacklist_proxy(self.currentHttpProxy)
        if (not self.currentHttpsProxy == None and https) :
            self.blacklist_proxy(self.currentHttpsProxy)
    
    #Public function
    #blacklists a given proxy
    def blacklist_proxy(proxy) :
        if (not proxy == None) :
            self.blacklist.append(proxy)

    #Private function
    #Returns the tree of the proxy url
    #Always resets the proxy to get the new
    def _get_tree(self, url, reset=True) :
        if (reset) :
            proxy_handler = urllib.request.ProxyHandler({})
            opener = urllib.request.build_opener(proxy_handler)
            urllib.request.install_opener(opener)
        req = urllib.request.Request(url, None, data.headers)
        while True:
            try :
                response = urllib.request.urlopen(req)
                break
            except urllib.error.HTTPError as e :
                if not e == 503:
                break
        page = response.read()
        tree = html.fromstring(page)
        return tree

    #Public function
    #@param nrOfProxies Nr of proxies returned
    #@param https Only get https proxies
    #@param google Only get proxies that support google
    #Returns a list of http(s) proxies
    #Returns None if no proxy was found!
    #[ip, port, code, country,  anonymity, google, https, last checked]
    def get_http_proxy(self, nrOfProxies=1,https=False,google=False) :
        if (self.verbose) :
            print("[*]Parameters: nrOfProxies=%d, https=%r, google=%r" % (nrOfProxies, https, google))
    
        httpProxies = []
        tree = self._get_tree(data.url_http)
        found = 0
        i = 1
        bcolors.printGreen("Starting proxy scan!")
        while(found < nrOfProxies) :
            proxy = tree.xpath(data.path + "[%d]/td/text()" % i)
            if (self.verbose) :
                print("Found proxy: " + str(proxy))
            if (proxy == []) :
                print("Could not find proxy!")
                return None;
            if (self._validate(proxy, https, google) and self.format_proxies(proxy) not in self.blacklist) :
                if (self.verbose) :
                    bcolors.printGreen("Proxy meeting requirements found!")

                httpProxies.append(proxy)
                found += 1
            i += 1
        return httpProxies

    #Public function
    #@param nrOfProxies The number of proxies returned
    #Returns a list of socks-proxies
    #[ip,port,code,country,version,anonymity,https,last checked]
    def get_socks_proxy(self, nrOfProxies=1) :
        socksProxies = []
        tree = self._get_tree(data.url_socks)
        found = 0
        i = 1
        while (found < nrOfProxies) :
            proxy = tree.xpath(data.path + "[%d]/td/text()" % i)
            if (self._validate(proxy) and self.format_proxies(proxy) not in self.blacklist) :
                socksProxies.append(proxy)
                found += 1
            i += 1
        return socksProxies

    #Public function
    #@param proxies The proxies that you want formatted
    #Returns the proxies in the format: 
    # IP:Port
    def format_proxies(self, proxies) :
        formatted = []
        if (proxies == None or len(proxies) == 0) :
            return formatted
        for proxy in proxies :
            if (not proxy == None) :
                p = str(proxy[0]) + ":" + str(proxy[1])
                formatted.append(p)
        return formatted

    #Public function
    #Validates the current proxy
    #Does nothing if proxy is valid,
    #else prints error and stops program execution
    def validate_proxy(self) :
        if (self.verbose) :
            print("[*]Validating proxy...")
        try :
            ip = self.get_ip()
            ips = self.get_ip(True)
        except Exception as e:
            bcolors.printFail(("[-]Error occured while validating proxy!\n" + str(e)))
            print("Press enter to continue, or ctrl+c to interrupt...")
            input()
            ip = "Unknown"
            ips = "Unknown"
		
        if (self.verbose) :
            print("[*]Your IP is: " + str(self.myip) + "\n[*]Proxy(HTTP) ip is: " + str(ip) + "\n[*]Proxy(HTTPS) ip is: " + str(ips))

        if (ip == self.myip) :
            bcolors.printWarning("[-]HTTP proxy error detected! Press enter to continue, or Ctrl+C to interrupt...")
            input()
            
        if (ips == self.myip) :
            bcolors.printWarning("[-]HTTP proxy error detected! Press enter to continue, or Ctrl+C to interrupt...")
            input()

    def get_ip(self, https=False) :
        if (not https) :
            return (urllib.request.urlopen(urllib.request.Request('http://api.ipify.org')).read())
        return (urllib.request.urlopen(urllib.request.Request('https://api.ipify.org')).read())
    
    # Takes a proxy in the format of IP:Port and installs
    # an opener with that proxy
    #@param proxf, the formatted proxy
    #@param proxfhttps, optional formatted https proxy
    def install_proxy(self, proxf, proxfhttps = None) :
        if (proxfhttps == None) :
            proxy = urllib.request.ProxyHandler ({
                'http':proxf
            })
        else :
            proxy = urllib.request.ProxyHandler ({
                'http':proxf,
                'https':proxfhttps
            })
        opener = urllib.request.build_opener(proxy)
        urllib.request.install_opener(opener)
        self.currentHttpProxy = proxf
        self.currentHttpsProxy = proxfhttps
        if (self.verbose) :
            bcolors.printGreen("[+]New proxies installed!")
            
if __name__=='__main__' :
    p = Proxy(True)
    p.proxify()
    p.print_state()
    p.validate_proxy()
