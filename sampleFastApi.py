from fastapi import FastAPI, HTTPException, Body
app = FastAPI()
import uvicorn
from app.categoryData import Categories
from typing import Any



@app.get("/category/{category_id}")
def getCategory(category_id : int):
    result = [category for category in Categories if category["category_id"] == category_id]
    if not result:
        raise HTTPException(status_code=404, detail = f"The Category with id {category_id} is not found")
    result_list = result[0]
    return {
        "category_id" : result_list["category_id"],
        "category_name" : result_list["category_name"]
    }

@app.post("/category")
def createCategory(category : Any = Body(...)):
    new_id = len(Categories) + 1
    result = {
        "category_id" : new_id,
        "category_name" : category["category_name"]
    }
    Categories.append(result)
    return {"detail" : "The category with id {} has been created".format(new_id)}

@app.put("/category/{category_id}")
def updateCategory(category_id: int, category :Any = Body(...)):
    result = [category for category in Categories if category_id == category["category_id"]]
    if not result:
        raise HTTPException(status_code=404, detail = f"The category with id {category_id} is not found")
    result[0].update(category)
    return result[0]





@app.delete("/category/{category_id}")
def deleteCategory(category_id : int):
    result = [category for category in Categories if category_id == category["category_id"]]
    if not result:
        raise HTTPException(status_code=404, detail= f"The category with id {category_id} is not found")
    Categories.remove(result[0])
    return {
        "detail" : f"The category with id {category_id} has been deleted"
    }

@app.get("/category")
def getCategories(page : int = 1, limit : int = 10):
    start = (page - 1) * limit
    end = start + limit
    result_list = []
    for category in Categories:
        result = {
            "category_id": category["category_id"],
            "category_name": category["category_name"]
        }
        result_list.append(result)
    return result_list[start : end]





@app.get("/category/{category_id}/item")
def getItems(category_id : int, limit : int = 10, page : int = 1):
    start = (page - 1) * limit
    end = start + limit
    category_list = [category for category in Categories if category_id == category["category_id"]]
    if not category_list:
        raise HTTPException(status_code=404, detail= f"The category with id {category_id} is not found")
    result = [key for key in category_list[0] if key == "items"]
    if not result:
        return {
            "items" : None
        }
    return category_list[0]["items"][start : end]







@app.get("/category/{category_id}/item/{item_id}")
def getItems(category_id : int, item_id : int):
    category_list = [category for category in Categories if category_id == category["category_id"]]
    if not category_list:
        raise HTTPException(status_code=404, detail=f"The category with id {category_id} is not found")
    item_list = [item for item in category_list[0]["items"] if item_id == item["item_id"]]
    if not item_list:
        raise HTTPException(status_code= 404, detail=f"The Item with id {item_id} id not found")
    return item_list[0]

@app.post("/category/{category_id}/item")
def createItems(category_id : int, item : Any = Body(...)):
    category_list = [category for category in Categories if category_id == category["category_id"]]
    if not category_list:
        raise HTTPException(status_code=404, detail = f"The category with id {category_id} is not found")
    previous_id = category_list[0]["items"][-1]["item_id"]
    new_item_id = previous_id + 1

    create_item = {
        "item_id" : new_item_id,
        "item_name" : item["item_name"],
        "price" : item["price"]
    }
    category_list[0]["items"].append(create_item)
    return {
        "detail" : f"The item with id {new_item_id} has been created"
    }


@app.put("/category/{category_id}/item/{item_id}")
def updateItem (category_id : int, item_id : int, item : Any = Body(...)):
    category_list = [category for category in Categories if category_id == category["category_id"]]
    if not category_list:
        raise HTTPException(status_code=404, detail=f"The category with id {category_id} id not found")
    item_list = [item for item in category_list[0]["items"] if item["item_id"] == item_id]
    if not item_list:
        raise HTTPException(status_code=404, detail = f"The item with id {item_id} is not found")
    item_list[0].update(item)
    return {
        "detail" : f"The item with id {item_id} has been successfully updated"
    }

@app.delete("/category/{category_id}/item/{item_id}")
def deleteItem(category_id : int, item_id : int):
    category_list = [category for category in Categories if category_id == category["category_id"]]
    if not category_list:
        raise HTTPException(status_code=404, detail=f"The category with id {category_id} is not found")
    item_list = [item for item in category_list[0]["items"] if item_id == item["item_id"]]
    if not item_list:
        raise HTTPException(status_code=404, detail = f"The item with id {item_id} is not found")
    category_list[0]["items"].remove(item_list[0])
    return {
        "detail" : f"The item with id {item_id} has been deleted"
    }

@app.get("/getAll")
def getAll():
    return Categories







if __name__ == "__main__":
    uvicorn.run(app, host = "Localhost", port = 8002)







