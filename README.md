automated\_craigslist\_search
===========================

## Installation 

Run the following from your favorite directory to begin using `automated_craigslist_search`

		$ git clone git@github.com:robertdavidwest/api-automated_craigslist_search.git #assuming ssh install
		$ cd automated_craigslist_search
		$ python setup.py install

#### Test the install

	$ python
	Enthought Canopy Python 2.7.3 | 64-bit | (default, Dec  2 2013, 16:09:43) [MSC v
	.1500 64 bit (AMD64)] on win32
	Type "help", "copyright", "credits" or "license" for more information.
	>>> import automated_craigslist_search


#### Dependencies

* `beautifulsoup4` (web scrapin' n that)
* `pandas` (for all things data)

You can install both of these using pip:

	$ pip install pandas
	$ pip install beautifulsoup4

#### Some Examples

**Example 1: a simple search**

Using the function `search_craigslist`, we can mimic the craigslist search functionality and the resulting search results are stored in a `pandas.DataFrame`. For a full description of the function see the doc string.

The following search:
 
	>>> from automated_craigslist_search import connect_to_craigslist
	>>> search_key_words = "parrot cage"
	>>> df = connect_to_craigslist.search_craigslist(search_key_words,min_value=50, max_value=250,words_not_included="dead",city="newyork")

Will return:

	>>> df.head()
	     Date               Location Price Results                      						urls
	0  Jun 30   (Allentown PA 18102)   $50 Large Vintage Pedestal Birdcage/ Parrot Cage -...  	/mnh/fud/4543304897.html  
	1  Jun 29           (Pelham, NY)  $250 King's Large Parrot Cage - Like New!  				/wch/for/4545509813.html   
	2  Jul  1         (brentwood ny)   $50 Large parrot Cage for sale Must go TODAY   			/lgi/hsh/4547799198.html  
	3  Jul  1         (brentwood ny)   $50 Large parrot Cage for sale Must go TODAY -  			/lgi/for/4547724127.html  
	4  Jun 29      (South River, NJ)   $90 New Large Parrot Cage Bird Cages On Sale! 10 M...  	/jsy/fod/4507112277.html  
	
**Example 2: search and send results**

Using the function `search_and_send` you can e-mail (from a gmail account, this could be adapted to include others) out a html formatted display of the search results from a craigslist search to mailing list. Then from your OS you can run this function periodically using application like [Cron](https://help.ubuntu.com/community/CronHowto) for example. 

	>>> from automated_craigslist_search import connect_to_craigslist
	>>> mailing_list = ["pet_stores_in_ipswitch@yahoo.com", "dazed_parrots_in_bolton@gmail.com"]
	>>> my_gmail = <yourgmailusername>@gmail.com
	>>> password = <yourgmailpassword>
	>>> previous_alerts_df = connect_to_craigslist.search_craigslist('fe4%%^gh;l') # empty DataFrame, use this dataframe to prevent duplicate entries being sent
	>>> search_key_words = "parrot cage"
	>>> connect_to_craigslist.search_and_send(my_gmail, mailing_list, password, previous_alerts_df, search_key_words,min_value=50, max_value=250,words_not_included="dead",city="newyork")

*NOTE: If you have 2 step verification turned on, on your gmail account you will need to disable, or, set up a separate gmail account (I prefer the latter, you can then also set up a handle related to the task at hand)*

