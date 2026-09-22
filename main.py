from fastapi import FastAPI
import json
app = FastAPI()
@app.get("/")
def hello():
	return {'message':'Hello world'}
@app.get("/about")
def about():
	return {'message': 'campusx is an education platform where you can learn AIN'}
@app.get("/view")
def load_data():
	with open('package.json', 'r') as f:
		data = json.load(f)
	return data