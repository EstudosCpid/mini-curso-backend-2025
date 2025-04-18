from pydantic import BaseModel

class CompanyRequest(BaseModel):
	name: str
	description: str
	telephone: str
	address: str
