from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()

import mysql.connector
from mysql.connector import pooling
from mysql.connector import Error

connection_pool = pooling.MySQLConnectionPool(
            pool_name="pynative_pool",
            pool_size=5,
            pool_reset_session=True,
            host="localhost",
            user="root",
            passwd="Sai_Nagu@25794",
            database="test_db"
        )
connection_object = connection_pool.get_connection()
cursor = connection_object.cursor()
connection_object.autocommit = False


class Category(BaseModel):
    category_name: str


class Items(BaseModel):
    item_name : str
    price : float
    category_id : int| None = None




@app.get("/category")
def get(limit : int = 10, page : int = 1):
    try:
        offset = (page - 1) * limit
        sql_query = "SELECT * FROM category LIMIT %s OFFSET %s"
        val = [(limit), (offset)]
        cursor.execute(sql_query,val)
        result = cursor.fetchall()
        result_list = []
        if not result:
            result_list = {"detail " : f"The page {page} does not exist"}
        else:
            for item in result:
                result_list.append({
                    "category_id": item[0],
                    "category_name": item[1]
                })

    except Error as e:
        result_list = {"Error reading data from MySQL table": e}
    finally:
        return result_list



@app.get("/item")
def get(limit : int = 10, page : int = 1):
    try:
        offset = (page - 1) * limit
        sql = "SELECT * FROM item LIMIT %s OFFSET %s"
        val = [(limit), (offset)]
        cursor.execute(sql, val)
        result = cursor.fetchall()

        result_list = []
        if not result:
            result_list = {"detail " : f"The page {page} does not exist"}
        else:
            for item in result:
                result_list.append({
                    "item_id": item[0],
                    "item_name": item[1],
                    "price": item[2]
                })
    except Error as e:
        result_list = {"Error reading data from MySQL table": e}
    finally:
        return result_list


@app.get("/category/{category_id}")
def getCategory(category_id : int):
    try:
        sql = "SELECT * FROM category WHERE category_id = %s"
        val = [(category_id)]
        cursor.execute(sql, val)
        result = cursor.fetchone()
        result_list = []
        if not result:
            result_list = {"detail" : f"The category_id {category_id} is not found" }
        else:
            result_list = {
                "category_id" : result[0],
                "category_name" : result[1]
            }
    except Error as e:
        result_list = {"Error reading data from MySQL table": e}
    finally:
        return result_list

@app.post("/category")
def createCategory(category : Category):
    try:
        sql = "INSERT INTO category (category_name) VALUES (%s)"
        val = [(category.category_name)]
        cursor.execute(sql, val)
        connection_object.commit()
        if not category.category_name:
            result = {
                "detail" : "The value should not be empty"
            }
        else:
            result = {"detail" : "Data Inserted successfully into category table"}
    except Error as e:
        result = {"Failed to insert in category table ": e}
        connection_object.rollback()
    finally:
        return result

@app.put("/category/{category_id}")
def updateCategory(category_id :  int, category : Category):
    try:
        sql = "SELECT * FROM category WHERE category_id = %s"
        val = [(category_id)]
        cursor.execute(sql, val)
        getcategory = cursor.fetchone()
        if not getcategory:
            result = {"detail" : f"The category_id {category_id} is not found"}
        elif not category.category_name:
            result = {"detail" : "The value should not be empty"}
        else:
            sql = "UPDATE category SET category_name = %s WHERE category_id = %s"
            val = [(category.category_name), (category_id)]
            cursor.execute(sql, val)
            connection_object.commit()
            result = {"detail" : "Record updated successfully"}
    except Error as e:
        result = {"Failed to update data into category table " : e}
        connection_object.rollback()
    finally:
        return result

@app.delete("/category/{category_id}")
def deleteCategory(category_id : int):
    try:
        sql = "SELECT * FROM category WHERE category_id = %s"
        val = [(category_id)]
        cursor.execute(sql, val)
        getcategory = cursor.fetchone()
        if not getcategory:
            result = {"detail": f"The category_id {category_id} is not found"}
        else:
            sqlQuery_item = "DELETE FROM item WHERE category_id = %s"
            item_value = [(category_id)]
            cursor.execute(sqlQuery_item, item_value)
            sqlQuery_category = "DELETE FROM category WHERE category_id = %s"
            category_value = [(category_id)]
            cursor.execute(sqlQuery_category, category_value)
            connection_object.commit()
            result = {"detail" : f"The category with category_id {category_id} has been deleted successfully"}
    except Error as e:
        result = {"Failed to delete the data from category table " : e}
        connection_object.rollback()
    finally:
        return result

@app.get("/item/{item_id}")
def getCategory(item_id : int):
    try:
        sql = "SELECT * FROM item WHERE item_id = %s"
        val = [(item_id)]
        cursor.execute(sql, val)
        result = cursor.fetchone()
        result_list = []
        if not result:
            result_list = {"detail" : f"The item_id {item_id} is not found" }
        else:
            result_list = {
                "item_id" : result[0],
                "item_name" : result[1],
                "price" : result[2]
            }
    except Error as e:
        result_list = {"Error reading data from MySQL table": e}
    finally:
        return result_list

@app.post("/item")
def createCategory(item : Items):
    try:
        sql = "INSERT INTO item (item_name, price, category_id) VALUES (%s, %s , %s)"
        val = [(item.item_name), (item.price), (item.category_id)]
        cursor.execute(sql, val)
        connection_object.commit()
        if not item.item_name:
            result =  {
                "detail": "The value for item_name should not be empty"
            }
        else:
            result = {"detail" : "Data Inserted successfully into items table"}
    except Error as e:
        result = {"Failed to insert in item table ": e}
        connection_object.rollback()
    finally:
        return result


@app.put("/item/{item_id}")
def updateCategory(item_id :  int, item : Items):
    try:
        sql = "SELECT * FROM item WHERE item_id = %s"
        val = [(item_id)]
        cursor.execute(sql, val)
        getitem = cursor.fetchone()
        if not getitem:
            result = {"detail" : f"The item_id {item_id} is not found"}
        elif not item.item_name:
            result = {"detail" : "The value should not be empty"}
        else:
            sql = "UPDATE ITEM SET item_name = %s, price = %s WHERE item_id = %s"
            val = [(item.item_name), (item.price), (item_id)]
            cursor.execute(sql, val)
            connection_object.commit()
            result = {"detail" : "Record updated successfully"}
    except Error as e:
        result = {"Failed to update data into category table " : e}
        connection_object.rollback()
    finally:
        return result

@app.delete("/item/{item_id}")
def deleteItem(item_id : int):
    try:
        sql = "SELECT * FROM item WHERE item_id = %s"
        val = [(item_id)]
        cursor.execute(sql, val)
        getItem = cursor.fetchone()
        if not getItem:
            result = {"detail" : f"The item with item_id {item_id} is not found"}
        else:
            sqlQuery = "DELETE FROM item WHERE item_id = %s"
            values = [(item_id)]
            cursor.execute(sqlQuery, values)
            connection_object.commit()
            result = {"detail" : f"The item with item_id {item_id} has been deleted"}

    except Error as e:
        result = {"Failed to delete data in item table" : e}
        connection_object.rollback()
    finally:
        return result

@app.get("/category/{category_id}/item")
def getItems(category_id : int, limit : int = 10, page : int = 1 ):
    try:
        offset = (page - 1) * limit
        sql = "SELECT item_id, item_name, price FROM item WHERE category_id = %s LIMIT %s OFFSET %s"
        val = [(category_id), (limit), (offset)]
        cursor.execute(sql, val)
        result = cursor.fetchall()
        result_list = []
        if not result:
            result_list = {"detail" : "Items not found"}
        else:
            for item in result:
                result_list.append({
                    "item_id" : item[0],
                    "item_name" : item[1],
                    "price" : item[2]
                })
    except Error as e:
        result_list = {"Error reading data from MySQL table": e}

    finally:
        return result_list

@app.get("/category/{category_id}/item/{item_id}")
def getItems(category_id : int, item_id : int):
    try:
        sql = "SELECT item_id, item_name, price FROM item WHERE category_id = %s AND item_id = %s"
        val = [(category_id), (item_id)]
        cursor.execute(sql, val)
        result = cursor.fetchall()
        if not result:
            result_list = {"detail" : "Item not found"}
        else:
            result_list = {
                "item_id": result[0][0],
                "item_name": result[0][1],
                "price": result[0][2]
            }

    except Error as e:
        result_list = {"Error reading data from MySQL table": e}

    finally:
        return result_list


@app.get("/getAllCategories")
def getAllCategories(limit : int = 10, page : int = 1):
    try:
        offset = (page - 1) * limit
        sql = "SELECT * FROM category INNER JOIN item WHERE category.category_id = item.category_id LIMIT %s OFFSET %s"
        val = [(limit), (offset)]
        cursor.execute(sql, val)
        result_list = cursor.fetchall()
        category_id = []
        list_a = []
        for item in result_list:
            if item[0] in category_id:
                index = category_id.index(item[0])
                list_a[index]["Items"].append({
                    "item_id": item[3],
                    "item_name": item[4],
                    "price": item[5]
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
        if not list_a:
            list_a = {"detail" : f"The page {page} does not exist"}
    except Error as e:
        list_a = {"Error reading data from MySQL table": e}
    finally:
        return list_a


if __name__ == "__main__":
    import uvicorn
    try:
        uvicorn.run(app, host = "localhost", port = 8011)
    except Error as e:
        print({"Error connection msg ": e})

    finally:
        if connection_object.is_connected():
            connection_object.close()
            print("connection is closed")

