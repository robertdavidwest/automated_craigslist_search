import urllib2
import bs4
import pandas
import pdb
import shutil 
import time
import datetime

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

def search_craigslist(seach_key_words, min_value=None, max_value=None, category='all for sale / wanted', words_not_included=''):
    """ 'search_craigslist' for specific keys words and over a specified price 
    range. The function will return a Pandas Dataframe containing the 'price',
    'title' and 'url' for every search result

    :param seach_key_words: a string of search key words separated by spaces
    :type seach_key_words: str or unicode

    :param min_value: minimum dollar value for search. Default value is nan, no lower bound on search.
    :type min_value: integer or float

    :param max_value: maximum dollar value for search. Default value is nan, no upper bound on search.
    :type max_value: integer or float

    :param category: craigslist search category. Default value is 'all for sale / wanted'
    :type category: str or unicode

    :param words_not_included: a string of words to be excluded from search results separated by spaces. Default value is empty string/
    :type priority: str or unicode
    
    :returns: a pandas dataframe containing search results
    :rtype: Pandas.DataFrame
    """  
    # Add functionality to change city, currenrly set on newyork    

    # construct search url from specified criteria    
    seach_key_words = seach_key_words.replace(' ','+')
    url = 'http://newyork.craigslist.org/search/' + get_category(category) + '?query=' + seach_key_words 
    if pandas.isnull(min_value) is not None:
        url = url + '&minAsk=' + str(min_value)
    
    if pandas.isnull(max_value) is not None:
        url = url + '&maxAsk=' + str(max_value)
        
    url = url + '&sort=rel'
    
    # Open url and use beautiful soup to find search results    
    response = urllib2.urlopen(url)
    soup = bs4.BeautifulSoup(response)
    
    # All data returned from the query is stored in <div class="content">
    search_content = soup.find_all('div', {'class':'content'})
    assert(len(search_content)==1) # There should only be one div class="content", if more than one returned, stop program
    search_content = search_content.pop()
    
    results = []
    urls = []
    price = []
    dates = []
    location = []
    
    for row in search_content.find_all('p',{'class':'row'}):    
        # text and url data
        class_pl_info = row.find('span',{'class':'pl'}) 
        # there is an href stored in 'class_pl_info' with a single 'a' tag
        #    - the method 'getText' will return unicode containing the search entry title
        #    - the method 'attrs' will return a dict, and the key 'href' will then return the respective url
        results.append(class_pl_info.find('a').getText())
        urls.append(class_pl_info.find('a').attrs['href'])
        
        # price data
        class_price_info = row.find('span',{'class':'price'}) 
        # class_price_info contains the respective price if one is specified
        if class_price_info == None:
            price.append(None)   
        else :
            price.append(class_price_info.getText())        
        
        # date of craigslist post
        date_info = row.find('span',{'class','date'})
        dates.append(date_info.getText())
    
        # Location
        location_info = row.find('span',{'class':'pnr'})
        location_info = location_info.find('small')
        # class_price_info contains the respective price if one is specified
       
        if location_info == None:
            location.append(None)   
        else :
            location.append(location_info.getText()) 
       
    # store results in pandas dataframe
    d = {'Results' : results, 'urls' : urls, 'Price' : price, 'Date' : dates, 'Location' : location }
    df = pandas.DataFrame(d)
    
    # Remove rows that contain words from the string 'words_not_included'
    words_not_included = words_not_included.split()
    for word in words_not_included:
        idx = [x.find(word) ==-1 for x in df.Results] # idx shows which rows do not contain excluded words
        df = df[idx] # only keep rows that do not contain excluded words

    return df
    
def create_html_output(df_criteria, df_results) :    
  
    # create timestamp string for output file
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H.%M.%S')
    output_filename = 'search_results_' + st + '.html'
    
    # reconstruct hrefs for output (adding 'http://newyork.craigslist.org' if needed 
    start_string = ['<a href="http://newyork.craigslist.org/' if x[:4]!='http' else '<a href="' for x in df_results.urls]
    
    df_results.Results = start_string + df_results.urls + '">' + df_results.Results + '</a>' 
    df_results = df_results.drop('urls',1)
    # adjust the pandas max_colwidth so that the output is not truncated when it is converted to html table
    pandas.set_option('max_colwidth',200)

    # convert output datafram into html table
    table = df_results.to_html(classes='df',index = False, justify='left',escape=False) # by setting escape=False we can keep the intended hrefs in the table

    # copy the html template file and rename
    shutil.copyfile('search_results_template.html', output_filename)

    # write the results to the file    
    with open(output_filename, 'a') as f:
        # Display search criteria 
        f.write('\n <p>Your automated craigslist query that had the following inputs: </p>')
        f.write(df_criteria.to_html())
        # Display results
        f.write('\n <p> has the following matching search results live right now: </p>')
        f.write(table)
        f.write('\n </body>')
        f.write('\n </html>')

                                      
if __name__ == "__main__":    
    
    search_key_words = 'burning man'
    words_not_included = ''#'wanted Wanted WANTED'
    min_value = 350
    max_value = 1300
    category = 'all for sale / wanted'
 
    df = search_craigslist(search_key_words, min_value,max_value, category, words_not_included)
    
    # Dataframe containing all search criteria
    index = ['search key words', 'Words excluded','Category', 'Minimum Price', 'Maximum Price']
    d = {'Search Criteria' : [search_key_words, words_not_included, 'all for sale / wanted', min_value, max_value]}
    criteria_df = pandas.DataFrame(d,index=index)
  
    create_html_output(criteria_df,df)
    