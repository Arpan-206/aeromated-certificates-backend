from sqlalchemy.orm import Session

from . import models, schemas


def get_org(db: Session, org_id: int):
    return db.query(models.Organization).filter(models.Organization.id == org_id).first()


def get_org_by_name(db: Session, name: str):
    return db.query(models.Organization).filter(models.Organization.name == name).first()


def create_org(db: Session, org: schemas.OrganizationCreate):
    db_org = models.Organization(name=org.name, registered_email=org.registered_email, representative=org.representative)
    db.add(db_org)
    db.commit()
    db.refresh(db_org)
    return db_org


def get_certs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Certificate).offset(skip).limit(limit).all()


def get_cert(db: Session, cert_id: int):
    return db.query(models.Certificate).filter(models.Certificate.id == cert_id).first()


def create_cert(db: Session, cert: schemas.CertificateCreate, org_id: int):
    db_cert = models.Certificate(**cert.dict(), org_id=org_id)
    db.add(db_cert)
    db.commit()
    db.refresh(db_cert)
    return db_cert

def revoke_cert(db: Session, cert_id: int):
    db_cert = db.query(models.Certificate).filter(models.Certificate.id == cert_id).first()
    db_cert.revoked = True
    db.commit()
    db.refresh(db_cert)
    return db_cert  