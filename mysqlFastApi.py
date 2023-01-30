from fastapi import FastAPI, Body, HTTPException
import uvicorn
from typing import Any


app = FastAPI()

import mysql.connector

mydb = mysql.connector.connect(host = "localhost", user = "root", passwd = "Sai_Nagu@25794", database = "test_db")
mycursor = mydb.cursor()

from pydantic import BaseModel

class Category(BaseModel):
    category_name: str

class Items(BaseModel):
    item_name : str
    price : float
    category_id : int


@app.get("/category")
def getCategory(limit : int = 10, page : int = 1):
    start  = (page - 1 ) * limit
    end = start + limit
    sql = "SELECT * FROM category"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    result_list = []
    for item in result:
        result_list.append({
            "category_id" : item[0],
            "category_name" : item[1]
        })
    getResult = result_list[start : end]
    if not getResult:
        raise HTTPException(
            status_code=404, detail= f"The page {page} does not exist"
        )
    return getResult




@app.get("/category/{category_id}")
def getCategory(category_id : int):
    sql = "SELECT * FROM category WHERE category_id = %s"
    val = [(category_id)]
    mycursor.execute(sql, val)
    result = mycursor.fetchone()
    if not result:
        raise HTTPException(
            status_code=404, detail = f"The category with id {category_id} is not found"
        )
    return {
        "category_id" : result[0],
        "category_name" : result[1]
    }




@app.post("/category")
def createCategory(category : Category):

    sql = "INSERT INTO category (category_name) VALUES (%s)"
    val = [(category.category_name)]
    if not category.category_name:
        return {
            "detail" : "The value for category_name should not be empty"
        }
    mycursor.execute(sql, val)
    mydb.commit()
    return ({
        "detail" : "Data is saved"
    })




@app.put("/category/{category_id}")
def updateCategory(category_id : int, category : Category):
    getcategory = "SELECT * FROM category WHERE category_id = %s"
    values = [(category_id)]
    mycursor.execute(getcategory, values)
    result = mycursor.fetchone()
    if not result:
        return {
            "detail" : f"The category id {category_id} is not found"
        }
    sql = "UPDATE CATEGORY SET category_name = %s WHERE category_id = %s"
    val = [(category.category_name), (category_id)]
    if not category.category_name:
        return {
            "detail" : "The value for category_name should not be empty"
        }

    mycursor.execute(sql, val)
    mydb.commit()

    return {
        "detail" : "Data is updated"
    }


@app.delete("/category/{category_id}")
def deleteCategory(category_id : int):
    getcategory = "SELECT * FROM category WHERE category_id = %s"
    values = [(category_id)]
    mycursor.execute(getcategory, values)
    result = mycursor.fetchone()
    if not result:
        return {
            "detail": f"The category id {category_id} is not found"
        }
    sql = "DELETE FROM category WHERE category_id = %s"
    val = [(category_id)]
    mycursor.execute(sql, val)
    mydb.commit()
    return {
        "detail" : "The data is deleted"
    }


@app.get("/item")
def getCategory(limit : int = 10, page : int = 1):
    start  = (page - 1 ) * limit
    end = start + limit
    sql = "SELECT * FROM item"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    result_list = []
    for item in result:
        result_list.append({
            "item_id" : item[0],
            "item_name" : item[1],
            "price" : item[2]
        })
    getResult = result_list[start : end]
    if not getResult:
        raise HTTPException(
            status_code=404, detail= f"The page {page} does not exist"
        )
    return getResult


@app.get("/item/{item_id}")
def getCategory(item_id : int):
    sql = "SELECT * FROM item WHERE item_id = %s"
    val = [(item_id)]
    mycursor.execute(sql, val)
    result = mycursor.fetchone()
    if not result:
        raise HTTPException(
            status_code=404, detail = f"The item with id {item_id} is not found"
        )
    return {
        "item_id" : result[0],
        "item_name" : result[1],
        "price" : result[2]
    }

@app.post("/item")
def createCategory(item : Items):
    sql = "INSERT INTO item (item_name, price, category_id) VALUES (%s, %s, %s)"
    val = [(item.item_name),(item.price), (item.category_id)]
    if not item.item_name:
        return {
            "detail" : "The value for item_name should not be empty"
        }

    mycursor.execute(sql, val)
    mydb.commit()
    return ({
        "detail" : "Data is saved"
    })

@app.put("/item/{item_id}")
def updateCategory(item_id : int, item : Items):
    getitem = "SELECT * FROM item WHERE item_id = %s"
    values = [(item_id)]
    mycursor.execute(getitem, values)
    result = mycursor.fetchone()
    if not result:
        return {
            "detail": f"The item id {item_id} is not found"
        }
    sql = "UPDATE ITEM SET item_name = %s, price = %s, category_id = %s WHERE item_id = %s"
    val = [(item.item_name), (item.price), (item.category_id), (item_id)]
    if not item.item_name:
        return {
            "detail" : "The value for item_name should not be empty"
        }
    mycursor.execute(sql, val)
    mydb.commit()
    return {
        "detail" : "Data is updated"
    }

@app.delete("/item/{item_id}")
def deleteCategory(item_id : int):
    getitem = "SELECT * FROM item WHERE item_id = %s"
    values = [(item_id)]
    mycursor.execute(getitem, values)
    result = mycursor.fetchone()
    if not result:
        return {
            "detail": f"The item id {item_id} is not found"
        }
    sql = "DELETE FROM item WHERE item_id = %s"
    val = [(item_id)]
    mycursor.execute(sql, val)
    mydb.commit()
    return {
        "detail" : "The data is deleted"
    }

@app.get("/category/{category_id}/item")
def getItems(category_id : int, limit : int = 10, page : int = 1 ):
    start = (page - 1) * limit
    end = start + limit
    sql = "SELECT item_id, item_name, price FROM item WHERE category_id = %s"
    val = [(category_id)]
    mycursor.execute(sql, val)
    result = mycursor.fetchall()
    result_list = []
    for item in result:
        result_list.append({
            "item_id" : item[0],
            "item_name" : item[1],
            "price" : item[2]
        })
    return result_list[start : end]

@app.get("/category/{category_id}/item/{item_id}")
def getItems(category_id : int, item_id : int):
    sql = "SELECT item_id, item_name, price FROM item WHERE category_id = %s AND item_id = %s"
    val = [(category_id), (item_id)]
    mycursor.execute(sql, val)
    result = mycursor.fetchall()
    if not result:
        raise HTTPException(status_code=404, detail = f"The category id {category_id} with item_id {item_id} is not found")
    list_a = result[0]
    return {
        "item_id" : list_a[0],
        "item_name" : list_a[1],
        "price" : list_a[2]
    }
@app.get("/getAllCategories")
def getAllCategories(limit : int = 10, page : int = 1):
    start = (page - 1) * limit
    end = start + limit

    sql = "SELECT * FROM category INNER JOIN item WHERE category.category_id = item.category_id"
    mycursor.execute(sql)
    result_list = mycursor.fetchall()
    category_id = []
    list_a = []
    for item in result_list:
        if item[0] in category_id:
            index = category_id.index(item[0])
            list_a[index]["Items"].append({
                "item_id" : item[3],
                "item_name" : item[4],
                "price" : item[5]
            })

        else:
            list_a.append({
                "category_id": item[0],
                "category_name": item[1],
                "Items": [{
                    "item_id": item[3],
                    "item_name": item[4],
                    "price": item[5]
                }]
            })
            category_id.append(item[0])
    result_list = list_a[start : end]
    if not result_list:
        raise HTTPException(
            status_code=404, detail= f"The page {page} does not exist"
        )
    return result_list














if __name__ == "__main__":
    uvicorn.run(app, host = "Localhost", port = 8006)
