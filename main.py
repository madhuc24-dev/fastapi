from fastapi import FastAPI, Path, Query, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator, computed_field
from typing import Annotated, Optional, Literal, Dict, List
import json

class Patient(BaseModel):

	id: Annotated[str, Field(..., description= "Id of the patient", title= "Patient Id", examples= ["P001, P002"])]
	name: Annotated[str, Field(..., description= "name of the patient", title= "Patient Name", examples= ["charan", "Madhu"])]
	city: Annotated[str, Field(..., description= "Name of the city", title= "City Name", examples= ["tirupati", "kadapa"])]
	age: Annotated[str,Field(..., description= "Age of patient", title= "Patient Age", examples= [10, 19])]
	gender: Annotated[Literal["male, female, others"], Field(..., description= "Gender of the patient", title= "Patient Gender")]
	height: Annotated[float, Field(..., description= "Height of patient in metres", title= "Patient Height", examples= [1.75, 1.55])]
	weight: Annotated[float, Field(..., description= "Weight of patient in kgs", title= "Patient weight", examples= [90.00, 21.22])]

	@computed_field
	@property
	def bmi(self) -> float:
		bmi = round(self.weight/(self.height**2), 2)
		return bmi

	@computed_field
	@property
	def verdict(self) -> str:
		if self.bmi < 18.5:
			return "under weight"
		elif 18.5 < self.bmi < 30:
			return "Normal" 
		else:
			return "Obese"


app = FastAPI()

def load_data():
	with open('patients.json', 'r') as f:
		data = json.load(f)
	return data

def save_data(data):
	with open("patients.json", "w") as file:
		json.dump(data, file)


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

def sort_patients(sort_by: str = Query(..., description = "sort on the basis of weight, height or bmi"), 
order: str = Query('asc', description = "sort in ascending or descending order")):
	
	if sort_by not in ["weight", "height", "bmi"]:
		raise HTTPException(status_code = 400, detail = "Invalid field, selct from height, weight, bmi")
	if order not in ['asc', 'desc']:
		raise HTTPException(status_code = 404, detail = "invalid order select from asc or desc")
	data = load_data()
	sort_order = True if order == "desc" else False
	sorted_data = sorted(data.values(), key = lambda x: x.get(sort_by, 0), reverse = sort_order)
	return sorted_data


@app.post('/create')

def create_patient(patient: Patient):

	data = load_data()

	if patient.id not in data:
		raise HTTPException(status_code= 400, detail= "Patient already exists")

	data[patient.id] = patient.model_dump(exclude = ["id"])

	save_data(data)

	return JSONResponse(status_code= 200, content= {"message": "patient added successfully"})




