from fastapi import FastAPI, Path, HTTPException, Query
import json

app = FastAPI()

def load_data():
	with open('package.json', 'r') as f:
		data = json.load(f)
	return data


@app.get("/")
def hello():
	return {'message':' management system api'}


@app.get("/about")
def about():
	return {'message': 'A fully functional API to manage your patients record'}


@app.get("/view")
def view():
	data = load_data()
	return data


@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(..., description = "ID of the patient in the DATABASE", example = "P001") ):
	data = load_data()
	if patient_id in data:
		return data[patient_id]
	raise HTTPException(status_code = 404, detail = 'patient not found')

@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description = "sort on the basis of weight, height or bmi"), order: str = Query('asc', description = "sort in ascending or descending order") ):
	if sort_by not in ["weight", "height", "bmi"]:
		raise HTTPException(status_code = 400, detail = "Invalid field, selct from height, weight, bmi")
	if order not in ['asc', 'desc']:
		raise HTTPException(status_code = 404, detail = "invalid order select from asc or desc")
	data = load_data()
	sort_order = True if order == "desc" else False
	sorted_data = sorted(data.values(), key = lambda x: x.get(sort_by, 0), reverse = sort_order)
	return sorted_data



