import uvicorn
from fastapi import FastAPI, Body
from typing import Any
app = FastAPI()


@app.get("/index")
def read_root():
    return {"Hello": "World"}


@app.get("/employee")
def employee(employee_id: int, employee_name: str, employee_salary=None):
    return {"employee_id": employee_id, "employee_name": employee_name, "employee_salary": employee_salary}

@app.post("/employee/data")
def employee_create(data: Any = Body(...)):
    return data


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080)
