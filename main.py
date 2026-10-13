from fastapi import FastAPI,Path,HTTPException,Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal,Optional
import json

app= FastAPI()

def load_data():
    with open('patients.json','r') as file:
        data=json.load(file)
    return data
def save_data(data):
    with open('patients.json','w') as file:
        json.dump(data,file)

data=load_data()

class Patient(BaseModel):

    id:Annotated[str,Field(...,description='ID of the patient',examples=['P001'])]
    name: Annotated[str,Field(...,description='Name of the patient')]
    gender: Annotated[Literal['Male','male','Female','female','Others'],Field(...,description='Gender of the patient')]
    city: Annotated[str,Field(...,description='Name of the city where patient is living')]
    age: Annotated[int,Field(...,description='Age of the patient',gt=0,lt=120)]
    height: Annotated[float,Field(...,description='Height of the patient in meters',gt=0)]
    weight: Annotated[float,Field(...,description='Weight of the patient in Kg',gt=0)]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi= round(self.weight/(self.height**2),2)
        return bmi

    @computed_field
    @property
    def verdict(self) ->str:
        if self.bmi<18.5:
            return "Underweight"
        elif self.bmi>22.5:
            return "obese"
        return "Normal"

class PatientUpdate(BaseModel):

    id:Annotated[Optional[str],Field(default=None)]
    name: Annotated[Optional[str],Field(default=None)]
    gender: Annotated[Optional[Literal['Male','male','Female','female','Others']],Field(default=None)]
    city: Annotated[Optional[str],Field(default=None)]
    age: Annotated[Optional[int],Field(default=None,gt=0)]
    height: Annotated[Optional[float],Field(default=None,gt=0)]
    weight: Annotated[Optional[float],Field(default=None,gt=0)]


@app.get("/")
def hello ():
    return {"message":"Patient Management System API "}

@app.get("/about")
def about():
    return {"message":"A fully functional API to manage your patient records"}

@app.get("/view")
def view():
    return data

@app.get('/patient/{patient_id}')
def view_patient(patient_id:str =Path(..., description='ID of the patient in the db',examples='P001')):
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404,detail='Patient not found')

@app.get('/sort')
def sort_patients(sort_by:str=Query(...,description='Sorting will be on the basis of height,weight and bmi',examples='bmi') ,
                  order:str=Query('ascending',description='Ordering of results will be done either in an ascending or descending manner',
                                  examples='ascending')):

    valid_fields=set(['height','weight','bmi'])

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400,detail=f'Bad Request from the client side. Please check from the accept ones: {valid_fields}')
    if order not in set(['ascending','descending']):
         raise HTTPException(status_code=400,detail=f'Bad Request from the client side.You can order the results either by ascending or descending')

    order_bool=True if order=='descending' else False
    result=sorted(data.values(), key=lambda x: x.get(sort_by,0),reverse=order_bool)

    return result

@app.post("/create")
def create_patient(patient : Patient):

    if patient.id in data:
        raise HTTPException(status_code=400,detail="The patient record already exists")

    #create a new patient record in the data
    data[patient.id]=patient.model_dump(exclude=['id'])

    #Save the data
    save_data(data)

    return JSONResponse(status_code=201,content={'message':'patient created successfully'})

@app.put('/edit/{patient_id}')
def update_details(patient_id: str,patient_update: PatientUpdate):

    if patient_id not in data:
        raise HTTPException(status_code=404,detail="Patient not found")

    patient_info=data[patient_id]
    updated_info=patient_update.model_dump(exclude_unset=True)          ###Checks and includes only the Non-None values
    for key,value in updated_info.items():
        patient_info[key]=value
    
    patient_info['id']=patient_id
    final_patient_dict=Patient(**patient_info).model_dump(exclude=['id'])
    data[patient_id]=final_patient_dict
    save_data(data)

    return JSONResponse(status_code=200,content={'message':"patient details updated"})

@app.delete("/delete/{patient_id}")
def delete_id(patient_id: str):

    if patient_id not in data:
        raise HTTPException(status_code=400,detail='Patient ID not in the records')

    del data[patient_id]
    save_data(data)
    return JSONResponse(status_code=200,content={'message':'patient details removed successfully'})
    












    
    



    





