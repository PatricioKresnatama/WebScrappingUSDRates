from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.exchange-rates.org/history/IDR/USD/T')
soup = BeautifulSoup(url_get.content,"html.parser")

table = soup.find('table', attrs={'class':'table table-striped table-hover table-hover-solid-row table-simple history-data'})
tr = table.find_all('tr')
temp = [] #initiating a tuple

for i in range(1, len(tr)):
    row = table.find_all('tr')[i]
    
    #harga harian
    day_price = row.find_all('td')[2].text
    day_price = day_price.strip() #for removing the excess whitespace
    
    #get inflasi
    tanggal = row.find_all('td')[0].text
    tanggal = tanggal.strip() #for removing the excess whitespace
    
    temp.append((tanggal,day_price)) 

temp = temp[::-1]

#change into dataframe
df = pd.DataFrame(temp, columns = ('tanggal','day_price'))

#insert data wrangling here
df['day_price'] = df['day_price'].str.replace("IDR","")
df['day_price'] = df['day_price'].str.replace(",","")
df['day_price'] = df['day_price'].astype('float64')

#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'USD {df["day_price"].mean()}'

	# generate plot
	ax = df.plot(x = 'tanggal', y = 'day_price', figsize = (20,9))
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]


	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)
