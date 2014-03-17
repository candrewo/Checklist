from flask import Flask, render_template, request
 
app = Flask(__name__)      
 
@app.route('/')
def home():
 	return render_template('home.html')

@app.route('/results', methods=['POST'])
def results():
	item = request.form["item"]
	amount = request.form["amount"]
	return render_template('results.html', amount=amount, item=item)


if __name__ == '__main__':
  	app.run(debug=True)