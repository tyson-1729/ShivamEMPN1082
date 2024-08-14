import os
import pyodbc as odbc
from dotenv import load_dotenv
from flask import Flask, render_template, url_for

load_dotenv()

# SERVER = os.getenv("server")
# DATABASE = os.getenv("database")
# USERNAME = os.getenv("user")
# PASSWORD = os.getenv("password")
# DRIVER = os.getenv("driver")

SERVER='bootcampaug5server.database.windows.net'
DATABASE='bootcampaug5db'
USERNAME='bootcamp'
PASSWORD='Pass@123'
DRIVER='{ODBC Driver 18 for SQL Server}'

print("env vars", DRIVER)

app = Flask(__name__)

# Enable debug mode (only during development)
app.debug = True

# List of images for the carousel
images = ["1.jpg", "2.jpg", "3.jpg"]


@app.route("/")
def home():
    return render_template("index.html", image=images[0], index=0)


@app.route("/task1")
def task1():
    return render_template("index.html", image=images[0], index=0)


@app.route("/task2")
def task2():
    connection_string = f"Driver={DRIVER};Server=tcp:{SERVER},1433;Database={DATABASE};Uid={USERNAME};;Pwd={PASSWORD};Encrypt=yes;TrustServerCertificate=yes;Connection Timeout=200;"
    with odbc.connect(connection_string) as conn:
        with conn.cursor() as cursor:
            cursor.execute("""SELECT TOP 20 * FROM SalesLT.Customer;""")
            result = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
    conn.close()
    return render_template("task2.html", rows=result, columns=columns)


@app.route("/task3")
def task3():
    connection_string = f"Driver={DRIVER};Server=tcp:{SERVER},1433;Database={DATABASE};Uid={USERNAME};;Pwd={PASSWORD};Encrypt=yes;TrustServerCertificate=yes;Connection Timeout=200;"
    with odbc.connect(connection_string) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """SELECT 
                p.Name AS ProductName, p.Color, p.Size, p.Weight
                FROM SalesLT.Product p
                JOIN SalesLT.ProductCategory pc
                ON 
                p.ProductCategoryID = pc.ProductCategoryID
                """
            )
            result = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
    conn.close()
    return render_template("task3.html", rows=result, columns=columns)


@app.route("/carousel/<int:image_index>")
def carousel(image_index):
    return render_template("index.html", image=images[image_index], index=image_index)


if __name__ == "__main__":
    app.run(port=8000)
