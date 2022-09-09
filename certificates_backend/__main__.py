import os
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Request, Header
from sqlalchemy.orm import Session

from certificates_backend.db_files import crud, models, schemas
from certificates_backend.db_files.connect import SessionLocal, engine
from certificates_backend.cert.cert_gen import cert_gen, delete_cert
from fastapi.staticfiles import StaticFiles

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="YOC Certificates Backend",
              description="Backend for the YOC certificates generator", version="0.1.0")
app.mount("/certificate-img", StaticFiles(directory="certificates"),
          name="certificates")

load_dotenv()
# Dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/organization/", response_model=schemas.Organization)
def create_org(org: schemas.OrganizationCreate, secret_key: str = Header(), db: Session = Depends(get_db)):
    if os.getenv("ADM_PASS") != secret_key:
        return HTTPException(status_code=401, detail="Unauthorized")
    try:
        db_org = crud.get_org_by_name(db, name=org.name)
        if db_org:
            raise HTTPException(
                status_code=400, detail="Organization already registered")
        return crud.create_org(db=db, org=org)
    except Exception as e:
        raise HTTPException(status_code=500)


@app.get("/organization/{org_id}", response_model=schemas.Organization)
def get_org(org_id: int, db: Session = Depends(get_db)):
    db_org = crud.get_org(db, org_id=org_id)
    if db_org is None:
        raise HTTPException(status_code=404, detail="Organization not found")
    return db_org


@app.post("/certificate/", response_model=schemas.Certificate)
def create_certificate(item: schemas.CertificateCreate, secret_key: str = Header(), db: Session = Depends(get_db)
                       ):
    if os.getenv("ADM_PASS") != secret_key:
        return HTTPException(status_code=401, detail="Unauthorized")
    try:
        org = crud.get_org_by_name(db, name=item.organization)
        db_cert = crud.create_cert(db=db, cert=item, org_id=org.id)
        cert_gen_out = cert_gen(name=db_cert.name, course=db_cert.course, yoc_director=db_cert.yoc_director,
                                organization=db_cert.organization, organization_rep=db_cert.organization_rep, organization_rep_designation=db_cert.organization_rep_designation, cert_id=db_cert.id)
        if cert_gen_out == 0:
            return db_cert
        else:
            raise HTTPException(
                status_code=500, detail="Certificate generation failed")
    except Exception as e:
        raise HTTPException(status_code=500)


@app.get("/certificate/{cert_id}", response_model=schemas.Certificate)
def get_certificate(cert_id: str, request: Request, db: Session = Depends(get_db)):
    db_cert = crud.get_cert(db, cert_id=cert_id)
    cert_gen_out = cert_gen(name=db_cert.name, course=db_cert.course, yoc_director=db_cert.yoc_director,
                                organization=db_cert.organization, organization_rep=db_cert.organization_rep, organization_rep_designation=db_cert.organization_rep_designation, cert_id=db_cert.id)
    db_cert.url = f"{str(request.url._url).replace('certificate', 'certificate-img')}.png"
    if db_cert is None:
        raise HTTPException(status_code=404, detail="Certificate not found")
    return db_cert


@app.get("/certificates/", response_model=list[schemas.Certificate])
def get_certificates(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    certs = crud.get_certs(db, skip=skip, limit=limit)
    return certs