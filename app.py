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
url_get = requests.get('https://www.coingecko.com/en/coins/ethereum/historical_data/usd?start_date=2020-01-01&end_date=2021-06-30#panel')
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
table = soup.find('tbody', attrs={'class':''})
datarow = table.find_all('tr', attrs={'class':''})

row_length = len(datarow)

temp = [] #initiating a list 

for i in range(0, len(datarow)):

    #scrapping process
    #get Date
    row = table.find_all('tr', attrs={'class':''})[i]
    dateVal = row.find_all('th', attrs={'class':'font-semibold text-center'})[0].text
    
    #get Volume
    volumeVal = row.find_all('td', attrs={'class':'text-center'})[1].text
    volumeVal = volumeVal.strip() #to remove excess white space

    temp.append((dateVal, volumeVal)) 

temp = temp[::-1]

#change into dataframe
data = pd.DataFrame(temp, columns = ('dateVal', 'volumeVal'))

#insert data wrangling here
data['dateVal'] = data['dateVal'].astype('datetime64')
data['volumeVal'] = data['volumeVal'].str.replace("$","")
data['volumeVal'] = data['volumeVal'].str.replace(",","")
data['volumeVal'] = data['volumeVal'].astype('float64')
data = data.set_index('dateVal')

#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'{round(data["volumeVal"].mean(),2)}' #be careful with the " and ' 

	# generate plot
	ax = data.plot(figsize = (20,9)) 
	
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