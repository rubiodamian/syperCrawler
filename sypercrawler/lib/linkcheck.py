<<<<<<< HEAD
from urllib2 import urlopen, HTTPError, URLError

'''Checks if an url is broken or not and returns the request status code
"response" can be a status code (404,500,200) or,
 if the request have a redirection (like 301 or 302),
  the url of that redirection'''


def checkURL(url):

    try:
        response = urlopen(url=url, timeout=10)
        if(response.geturl() != url):
            return response.geturl()
        else:
            return response.getcode()
    except HTTPError as e:
        return e.getcode()
    except URLError as e:
        print('Exception', e, type(e))
    except Exception as e:
        print('Exception', e, type(e))
=======
from urllib2 import urlopen, HTTPError, URLError 


    
'''Checks if an url is broken or not and returns the request status code
    "response" can be a status code (404,500,200) 
    or, if the request have a redirection (like 301 or 302), the url of that redirection'''
def checkURL(url):
    try:  
        response = urlopen(url=url, timeout=10)
        if(response.geturl() != url):
            return response.geturl()
        else:
            return response.getcode()
    except HTTPError as e:
        return e.getcode()   
    except URLError as e:  
        print('Exception', e, type(e))  
    except Exception as e:  
        print('Exception', e, type(e))
>>>>>>> branch 'master' of https://github.com/rubiodamian/syperCrawler.git
