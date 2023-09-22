from flask import Flask, request

app = Flask(__name__)

@app.route('/lab1', methods = ["GET", "POST"])
def index():
	if request.method == "GET":
		return {"message": "SSS"}, 200
	elif request.method == "POST":
		data  = request.json
		for key , value in data.items():
			print("SD", key, value)
		return "confirmation"

if __name__== '__main__':
    app.run(debug=True)