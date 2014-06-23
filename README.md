automated_craigslist_search
===========================

## Documentation

### How to use:

### Functions: 

`connect_to_craigslist.py` allows you to automate and repeat craigslist searches. Follow the instructions below to set up and automate craigslist searches.

The module `automated_craigslist_search` contains four functions: `create_html_output()`, `get_category()`, `search_craigslist()` and `send_email()`:

* `create_html_output(df_criteria, df_results):`

	Takes in two pandas dataframes one containing the search criteria and one containing the results of the craigslist search. The function transforms this data into html, ready to be e-mailed. The function returns a string containing the html. 
	
	Parameters:
     
    	:param me: a string containing the gmail address that mail will be sent from
 	    :type seach_key_words: str or unicode
    
	    :param you: a string containing the recipients email address
	    :type seach_key_words: str or unicode
    
  	  	:param html: a string containing the gmail user's password
 	    :type seach_key_words: str or unicode
    
 	    :param html: a string containing the html e-mail message to be sent
	    :type seach_key_words: str or unicode
    
	    :param html: a string containing the search key words that were used in the craiglist search
	    :type seach_key_words: str or unicode
    
   	 	:returns: a string containing html ready to be e-mailed
	    :rtype: str
    
* `get_category(category):`

    Maps the craigslist category to the url search code

	e.g.  `get_catagory('tickets')` will return the string 
	`'tia'`, this can be used in the url to search within the ticket category
	
	Parameters:
	
    	:param category: a string specifying the craiglist category to search within
	    :type seach_key_words: str or unicode

    	:returns: the url search code
    	:rtype: str

* `search_craigslist(seach_key_words, min_value=None, max_value=None, category='all for sale / wanted', words_not_included=''):`

    `search_craigslist` for specific keys words and over a specified price 
    range. The function will return a Pandas Dataframe containing the 'price',
    'title' and 'url' for every search result

	Parameters:
	
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
    
* `send_email(me, you, password, html):`

    `send_email` will send an email from the e-mail address `'me'`, to `'you'`. The email message sent is stored in 'html'. The function has no return output 
     
    Parameters:
     
    	:param me: a string containing the gmail address that mail will be sent from
	    :type seach_key_words: str or unicode

    	:param you: a string containing the recipients email address
   		:type seach_key_words: str or unicode

    	:param html: a string containing the gmail user's password
    	:type seach_key_words: str or unicode

	    :param html: a string containing the html e-mail message to be sent
    	:type seach_key_words: str or unicode

	    :param html: a string containing the search key words that were used in the craiglist search
    	:type seach_key_words: str or unicode

    
                                      
if __name__ == "__main__":    
    
    #############################################
    # Search criteria
    #############################################
    
    search_key_words = 'burning man tickets'
    words_not_included = ''#'wanted Wanted WANTED'
    min_value = 1
    max_value = 1500
    category = 'all for sale / wanted'
 
    #############################################
    # E-mail information
    #############################################
     
    # the gmail address that alerts will come from: this will require the users password
    send_alerts_from = "ticket.alerts.from.robert@gmail.com"
     
    # the mailing list. A Python List of strings, each containing e-mail addresses:
    mailing_list = ["robert.david.west@gmail.com", "robertdavidwest@gmail.com"]
     
    ############################################# 
    # Dataframe containing all search criteria
    index = ['search key words', 'Words excluded','Category', 'Minimum Price', 'Maximum Price']
    d = {'Search Criteria' : [search_key_words, words_not_included, 'all for sale / wanted', min_value, max_value]}
    criteria_df = pandas.DataFrame(d,index=index)
     
    # Dataframe containing results
    df = search_craigslist(search_key_words, min_value,max_value, category, words_not_included)
    
    # If Dataframe is not empty then e-mail results
    if len(df != 0):
        email_message = create_html_output(criteria_df,df)
 
        password = raw_input("Please enter your gmail password: ")
        for x in mailinglist:
            send_email(send_alterts_from, x, password,email_message, search_key_words)
    
    
    
    