import os
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
import requests

from certificates_backend.cert.cert_gen import cert_gen
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Aeromated Backend",
              description="Backend for the Aeromated certificates generator", version="0.1.0")
app.mount("/certificate-img", StaticFiles(directory="certificates"),
          name="certificates")

load_dotenv()
# Dependency


@app.get("/certificate/{cert_id}")
async def get_certificate(cert_id: str):
    res = requests.get(f"https://aeromates.hasura.app/api/rest/get-one?id={cert_id}", headers={'x-hasura-admin-secret': os.getenv('HASURA_ADMIN_SECRET')})
    if res.status_code == 200:
        result = res.json()['quizzes_quizzes_by_pk']
        if result is None:
            raise HTTPException(status_code=404, detail="Certificate not found")
        cert_gen(result['name'], cert_id)
        return {"certificate_id": cert_id, "certificate_url": f"/certificate-img/{cert_id}.png"}
    else:
        raise HTTPException(status_code=404, detail="Certificate not found")