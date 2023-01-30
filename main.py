import uvicorn
from fastapi import FastAPI, Body
from typing import Any
from enum import Enum

from pydantic import BaseModel
app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]




@app.get("/items/{item_id}")
def read_item(item_id : int, q :str | None = None):
    if q:
        return {
            "itemId" : item_id, "q" : q
        }
    return {
        "itemId" : item_id
    }


@app.get("/item/{item_id}")
def read_items(item_id : int, q: str | None = None, short : bool = False):
    item = {"itemId" : item_id}
    if q :
        item.update({"q" : q})
    if not short:
        item.update({"description" : "This is an amazing item that has a long description"})
    return item

class Item(BaseModel):

    name : str
    description : str | None = None
    price : float
    tax : float | None = None
@app.post("/item/")
def postDetails(data: Item):
    return data


@app.post("/itemsList/")
def CreateItems(item : Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

@app.put("/item/{itemId}")
def updateItems(item : Item, itemId : int):
    return {
        "Item_id" : itemId,
        **item.dict()
    }

@app.put("/items/{item_id}")
def updateItems(item : Item, item_id : int, q : str | None = None):
    result = {"Item_id" : item_id, **item.dict()}
    if q:
        result.update({"q" : q})
    return result





@app.get("/index")

def readIndex():
    return {
        "msg": "Hello World!"
    }

@app.get("/user")
def readUser():
    return{
        "user_name" : "Sai Nagu",
        "user_id" : 1,
        "user_location": "Hyderabad"
    }

@app.get("/userDetails")
def getUserdetails(employ_id: int, employ_name: str, employ_salary = None):
    return {
        "employeeId" : employ_id,
        "employeeName" : employ_name,
        "employeeSalary" : employ_salary
    }


@app.post("/employee")
def createUser (data: Any = Body(...)):
    return data
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}



if __name__ == "__main__":
    uvicorn.run(app, host = "0.0.0.0", port = 8000)