from GoogleSearcher import Google
import vulnerability_scanner
import get_proxy
def web_scanner() :
    query = input("Input query: ")
    google = Google(True, 10, True)
    google.set_myip(get_proxy.getIP())
    google.conduct_search(query, 1)
    links = google.get_urls()
    #vulnerability_scanner.run_tests(links, 3, True)

if __name__ == '__main__' :
    print("Running web vulnerability scan...")
    web_scanner()
