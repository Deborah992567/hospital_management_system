from fastapi import FastAPI
from .database import engine, Base
from .routers import auth_routes, staff, departments, patients, appointments, pharmacy, lab, billing

# create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hospital Management System")

# include routers
app.include_router(auth_routes.router)
app.include_router(staff.router)
app.include_router(departments.router)
app.include_router(patients.router)
app.include_router(appointments.router)
app.include_router(pharmacy.router)
app.include_router(lab.router)
app.include_router(billing.router)
