import urllib2
import bs4
import pandas

url = 'http://newyork.craigslist.org/search/sss?query=burning+man+tickets'
response = urllib2.urlopen(url)
soup = bs4.BeautifulSoup(response)


#currently, all the data is stored in <table class="wikitable sortable">
search_content = soup.find('div', {'class':'content'})
href_content = search_content.find_all('a')

results = []
for x in href_content:
    results.append([val.text.encode('utf8') for val in row.find_all('td')])

d = pandas.DataFrame(href_content)