from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.settings.database import get_session
from app.schemas.company import CompanyRequest #, CompanyCreateRequest, CompanyUpdateRequest
from app.models.company import Company

router = APIRouter(prefix="/company", tags=["Company"])

def company_get(company_name: str, session: Session) -> bool:
	query = select(Company).where(Company.name == company_name)
	result = session.scalars(query).first()
	return result


def company_exists(company_name: str, session: Session) -> bool:
	result = company_get(company_name, session)
	return result is not None


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def company_create(
	company: CompanyRequest,
	session: Session = Depends(get_session),
):
	if company_exists(company.name, session):
		raise HTTPException(
			status.HTTP_400_BAD_REQUEST,
			"Company already registered.",
		)

	company_dict = company.model_dump()

	session.add(Company(**company_dict))
	session.commit()

	return company_dict


@router.get("/read/{company_name}")
async def company_read(
	company_name: str,
	session: Session = Depends(get_session),
):
	company = company_get(company_name, session)

	if not company:
		raise HTTPException(status.HTTP_404_NOT_FOUND, "Company not found")
	return company


@router.put("/update/{company_name}", status_code=status.HTTP_200_OK)
async def company_update(
    company_name: str,
    company: CompanyRequest,
    session: Session = Depends(get_session),
):
    if not company_exists(company_name, session):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Company not found")

    company_data = company.model_dump(exclude_unset=True)

    query = update(Company).where(Company.name == company_name).values(**company_data)

    session.execute(query)
    session.commit()

    return company_data


@router.delete("/delete/{company_name}")
async def company_delete(
	company_name: str,
	session: Session = Depends(get_session),
):
	company = company_get(company_name, session)

	if not company:
		raise HTTPException(status.HTTP_404_NOT_FOUND, "Company not found")

	session.delete(company)
	session.commit()

	return {"message": "Company removed from database"}
