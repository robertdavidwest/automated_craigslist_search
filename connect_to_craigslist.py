import urllib2
import bs4
import pandas
import pdb

def get_category(category):
    """ 'get_category' maps the craigslist category to the url search code

    :param category: a string specifying the craiglist category to search within
    :type seach_key_words: str or unicode

    :returns: the url search code
    :rtype: str

    """
    
    category_key = {'all for sale / wanted' : 'sss', \
                    'antiques' : 'ata', \
                    'appliances' : 'ppa', \
                    'arts+crafts' : 'ara', \
                    'atvs/uts/snowmobiles' : 'sna', \
                    'auto parts' : 'pta', \
                    'baby+kids' : 'baa', \
                    'barter' : 'bar', \
                    'beauty+hlth' : 'haa', \
                    'bikes' : 'bia', \
                    'boats' : 'boo', \
                    'books' : 'bka', \
                    'business' : 'bfa', \
                    'cars+trucks' : 'cta', \
                    'cds/dvd/vhs' : 'ema', \
                    'cell phones' : 'moa', \
                    'clothes+acc' : 'cla', \
                    'collectibles' : 'cba', \
                    'computers' : 'sya', \
                    'electronics' : 'ela', \
                    'farm+garden' : 'gra', \
                    'free stuff' : 'zip', \
                    'furniture' : 'fua', \
                    'garage sales' : 'gms', \
                    'general' : 'foa', \
                    'heavy equipment' : 'hva', \
                    'household' : 'hsa', \
                    'jewelry' : 'jwa', \
                    'matierals' : 'maa', \
                    'motorcycle parts & acc' : 'mpa', \
                    'motorcycles' : 'mca', \
                    'music instr' : 'msa', \
                    'photo+video' : 'pha', \
                    'recreational vehicles' : 'rva', \
                    'sporting' : 'sga', \
                    'tickets' : 'tia', \
                    'tools' : 'tla', \
                    'toys+games' : 'taa', \
                    'video gaming' : 'vga', \
                    'wanted' : 'waa' }
    
    return category_key[category]

def search_craigslist(seach_key_words, min_value, max_value, category='all for sale / wanted', words_not_included=''):
    """ 'search_craigslist' for specific keys words and over a specified price 
    range. The function will return a Pandas Dataframe containing the 'price',
    'title' and 'url' for every search result

    :param seach_key_words: a string of search key words separated by spaces
    :type seach_key_words: str or unicode

    :param min_value: minimum dollar value for search
    :type min_value: integer or float

    :param max_value: maximum dollar value for search
    :type max_value: integer or float

    :param category: craigslist search category
    :type category: str or unicode

    :param words_not_included: a string of words to be excluded from search results separated by spaces
    :type priority: str or unicode
    
    :returns: a pandas dataframe containing search results
    :rtype: Pandas.DataFrame
    """  
    # Add functionality to change city, currenrly set on newyork    
       
    # construct search url from specified criteria    
    seach_key_words = seach_key_words.replace(' ','+')
    url = 'http://newyork.craigslist.org/search/' + get_category(category) + '?query=' + seach_key_words + '&minAsk=' + str(min_value) + '&maxAsk=' + str(max_value) + '&sort=rel'
    
    # Proxy settings for work
    # username = "XXX"
    # pword = "XXX"  
    # proxy = urllib2.ProxyHandler({'http': 'http://' + username + ":" + pword + '@amweb.ey.net:80'})
    # auth = urllib2.HTTPBasicAuthHandler()
    # opener = urllib2.build_opener(proxy, auth, urllib2.HTTPHandler)
    # urllib2.install_opener(opener)
    
    # Open url and use beautiful soup to find search results    
    response = urllib2.urlopen(url)
    soup = bs4.BeautifulSoup(response)
    
    # All data returned from the query is stored in <div class="content">
    search_content = soup.find_all('div', {'class':'content'})
    assert(len(search_content)==1) # There should only be one div class="content", if more than one returned, stop program
    search_content = search_content.pop()
    
    text = []
    urls = []
    price = []
    for row in search_content.find_all('p',{'class':'row'}):    
        # text and url data
        class_pl_info = row.find('span',{'class':'pl'}) 
        # price data
        class_price_info = row.find('span',{'class':'price'}) 
        
        # there is one href stored in 'class_pl_info' with a single 'a' tag
        #    - the method 'getText' will return unicode containing the search entry title
        #    - the method 'attrs' will return a dict, and the key 'href' will then return the respective url
        text.append(class_pl_info.find('a').getText())
        urls.append(class_pl_info.find('a').attrs['href'])
        # class_price_info contains the respective price
        price.append(class_price_info.getText())
    
    # store results in pandas dataframe
    d = {'text' : text, 'urls' : urls, 'price' : price}
    df = pandas.DataFrame(d)

    # Remove rows that contain words from the string 'words_not_included'
    words_not_included = words_not_included.split()
    for word in words_not_included:
        idx = [x.find(word) ==-1 for x in df.text] # idx shows which rows do not contain excluded words
        df = df[idx] # only keep rows that do not contain excluded words
        
    return df    
    
        
if __name__ == "__main__":    

    search_key_words = 'burning man'
    words_not_included = '' #wanted Wanted WANTED'
    min_value = 350
    max_value = 1300
    category = 'tickets'
    #df = search_craigslist(search_key_words,min_value,max_value,category,words_not_included)
    df2 = search_craigslist(search_key_words,min_value,max_value,'all for sale / wanted',words_not_included)
    
    #print df
    print df2
    