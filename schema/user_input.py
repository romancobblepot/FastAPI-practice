from pydantic import BaseModel,Field,computed_field,field_validator
from typing import Annotated,Literal,Optional
from config.city_tier import tier_1_cities,tier_2_cities

class UserInput(BaseModel):
    age: Annotated[int,Field(...,description="Age of the user",gt=0,lt=120)]
    weight:Annotated[float,Field(...,description="Weight of the user in kgs",gt=0)]
    height:Annotated[float,Field(...,description="Height of the user in meters",gt=0)]
    income_lpa:Annotated[float,Field(...,description="Income of the user in lpa",ge=0)]
    is_smoker:Annotated[bool,Field(...,description="If the user smokes or not")]
    city:Annotated[str,Field(...,description="City of the user")]
    occupation:Annotated[Literal['retired', 'freelancer', 'student', 'government_job',
       'business_owner', 'unemployed', 'private_job'],Field(...,description="Occupation of the user")]

    @field_validator('city',mode='before')
    @classmethod
    def normalize_city(cls,v:str) ->str:
        return v.strip().title()

    @field_validator('occupation',mode='before')
    @classmethod
    def lower_occupation(cls,v:str) ->str:
        return v.strip().lower()
    
    @computed_field
    @property
    def bmi(self) ->float:
        return self.weight/(self.height**2)

    @computed_field
    @property
    def lifestyle_risk(self) ->str:
        if self.is_smoker and self.bmi>30:
            return "high"
        elif self.is_smoker or self.bmi>25:
            return "medium"
        return "low"

    @computed_field
    @property
    def age_group(self) ->str:
        if self.age<25:
            return "young"
        elif self.age<40:
            return "adult"
        elif self.age<60:
            return "middle_aged"
        return "senior"

    @computed_field
    @property
    def city_tier(self) ->int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        return 3