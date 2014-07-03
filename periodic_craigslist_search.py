#!/usr/bin/env python
# encoding: utf-8
"""	:synopsis: "a craigslist search that will automatically e-mail the results when the search returns at least one entry. Run this file periodically from your server to set up craigslist alerts
	
    .. moduleauthor:: Robert D. West <robet.david.west@gmail.com>
"""
import automated_craigslist_search.connect_to_craigslist as connect_to_craigslist
import pandas
import sys

#############################################
# Search criteria
#############################################

search_key_words = 'burning man tickets'
words_not_included = 'INVENTORY needed Needed NEEDED wanted Wanted WANTED'
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
# Dataframe containing all search criteria
index = ['search key words', 'Words excluded','Category', 'Minimum Price', 'Maximum Price', 'City']
d = {'Search Criteria' : [search_key_words, words_not_included, 'all for sale / wanted', min_value, max_value, city]}
criteria_df = pandas.DataFrame(d,index=index)
 
# Dataframe containing results
df = connect_to_craigslist.search_craigslist(search_key_words, min_value,max_value, category, words_not_included, city)

# If Dataframe is not empty then e-mail results
if len(df != 0):
	email_message = connect_to_craigslist.create_html_output(criteria_df,df, city)
        
	f = open('/home/ubuntu/periodic_craigslist_search/ticket.alerts.from.robert.account.info.txt','r')
	password = f.read()
	
	for x in mailing_list:
		connect_to_craigslist.send_email(send_alerts_from, x, password,email_message)
