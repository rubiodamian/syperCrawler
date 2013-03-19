"""syperCrawler.lib.SafebrowsinglookupClient is a Singleton Class for the safebrowsinglookup.SafebrowsinglookupClient """

from sypercrawler.lib.browsinglookups.Safebrowsinglookup import SafebrowsinglookupClient as GoogleSafebrowsinglookupClient

class SafebrowsinglookupClient(object):
    ## Stores the unique Singleton instance-
    __instance = None
 
    ## The constructor
    #  @param self The object pointer.
    def __init__(self,debug=0, error=0):
        # Check whether we already have an instance
        if SafebrowsinglookupClient.__instance is None:
            # Create and remember instance
            #You need to change the api_key with yours api_key
            SafebrowsinglookupClient.__instance = GoogleSafebrowsinglookupClient('ABQIAAAARp_VkdjgYpMuADq7LFmUIhTkB2vh9AsorruAnk_xcKzZYC_sCQ',debug, error)
 
        # Store instance reference as the only member in the handle
        self.__dict__['_SafebrowsinglookupClient__instance'] = SafebrowsinglookupClient.__instance

    def lookup(self, *urls):
        return self.__instance.lookup(*urls)
    