#!/usr/bin/env python
# encoding: utf-8
"""	:synopsis: "a craigslist search that will automatically e-mail the results when the search returns at least one entry. Run this file periodically from your server to set up craigslist alerts
	
    .. moduleauthor:: Robert D. West <robet.david.west@gmail.com>
"""
import automated_craigslist_search.connect_to_craigslist as connect_to_craigslist
import pandas

#############################################
# Search criteria
#############################################

search_key_words = 'burning man tickets - inventory - needed - wanted'
words_not_included = ''
min_value = 0
max_value = 2000
category = 'all for sale / wanted'
city = 'newyork'

#############################################
# E-mail information
#############################################
 
# the gmail address that alerts will come from: this will require the users password
send_alerts_from = "ticket.alerts.from.robert@gmail.com"
 
# the mailing list. A Python List of strings, each containing e-mail addresses:
mailing_list = ["robert.david.west@gmail.com"]
 
############################################# 

# Get gmail pword
f = open('/Users/robertdavidwest/Documents/python_general_library/testing_space/cragslist/ticket.alerts.from.robert.account.info.txt','r')
#f = open('/home/ubuntu/periodic_craigslist_search/ticket.alerts.from.robert.account.info.txt','r')
password = f.read()

# Open dataFrame of previous alert entries
previous_alerts = pandas.HDFStore('previous_alerts.h5')

# search and send results
df = connect_to_craigslist.search_and_send(send_alerts_from, mailing_list, password, search_key_words, previous_alerts.df, min_value=min_value, max_value=max_value, words_not_included=words_not_included, city='newyork')

# append current search results to full list
previous_alerts.df = previous_alerts.df.append(df)

# remove dupilicates
previous_alerts.df = previous_alerts.df.drop_duplicates()

# update previous search entries in hdf5 file
previous_alerts.df.to_hdf('previous_alerts.h5','df')
previous_alerts.close()

