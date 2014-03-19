from flask import Flask, render_template, request
import json
 
app = Flask(__name__)      
 
@app.route('/', methods=['GET', 'POST'])
def home():
 	items = {'apples': 1, 'oranges':2, 'bananas':3}
 	if request.method == 'POST':
		item = request.form["item"]
		amount = request.form["amount"]
		items[item] = amount
		return render_template('home.html', items=items)
	else:
		return render_template('home.html', items=items)


if __name__ == '__main__':
  	app.run(debug=True)