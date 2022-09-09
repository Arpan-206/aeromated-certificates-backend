from typing import Union

from pydantic import BaseModel


class CertificateBase(BaseModel):
    name: str
    course: str
    organization: str
    yoc_director: str
    organization_rep: str
    organization_rep_designation: str


class CertificateCreate(CertificateBase):
    pass


class Certificate(CertificateBase):
    id: str
    generation_time: str
    url: Union[str, None] = None

    class Config:
        orm_mode = True


class OrganizationBase(BaseModel):
    registered_email: str
    name: str
    representative: str


class OrganizationCreate(OrganizationBase):
    pass


class Organization(OrganizationBase):
    id: int

    class Config:
        orm_mode = True
