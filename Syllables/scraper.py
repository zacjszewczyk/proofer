from urllib import request as r # Getting URLs
from urllib.request import urlretrieve # Getting resources
from random import choice # Randomize user agent so scraper isn't blocked
from gzip import GzipFile # For gzip compressed webpages
import re

class Scraper:
    # Pool of user agents, for randomizing user agent string
    user_agent_list = [
        #Chrome
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        #Firefox
        'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
        'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
        'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)']

    h = ""

    # Method: scrape
    # Purpose: Get content at target URL.
    # Parameters: 
    # - url: Target URL (String)
    # Return: HTML content at target URL (String)
    def scrape(self, url):
        global h
        # Make the request with a random user agent string
        h = choice(self.user_agent_list)
        req = r.Request(url, headers = {'User-Agent': h})
        # Get the response
        res = r.urlopen(req)

        # Cleanup
        del req

        # Check for an error (HTTP status code >= 400)
        if (int(res.getcode()) >= 400):
            return "%s : Error encountered, : %s" % (url, res.getcode())

        if (("content-encoding" in res.info().keys()) and (res.info()["content-encoding"] == "gzip")):
            buf = res.read()
            f = GzipFile(fileobj=buf)
            res = f.read()
        else:
            res = res.read()

        # Try to decode the page with utf-8 and then ascii
        try:
            return res.decode('utf-8')
            return res.decode('ascii')
        # Notify the user on error
        except:
            print("%s : Encountered encoding error." % (url))
            return "%s : Encountered encoding error." % (url)

    def getHeaders(self):
        return h

    def makeLocal(self, __raw):
        regex = r"([\w-]+)=(\"|')([^\"']*)\2"
        for line in __raw.split('\n'):
            if ("<img" in line and "src=" in line):
                line = line.split("<img")[1].split(">")[0]
                matches = re.finditer(regex, line)
                for matchNum, match in enumerate(matches, start=1):
                    if ("data-" not in match.group() and "src=" not in match.group()):
                        continue
                    if ("?" in match.group(3)):
                        print("Value",":",match.group(3).split("?")[0])
                    else:
                        print("Value",":",match.group(3))
                    # for groupNum in range(0, len(match.groups())):
                    #     groupNum = groupNum + 1    
                    #     print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))
        return __raw