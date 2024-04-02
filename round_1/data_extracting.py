import fitz
import mysql.connector

def files(pdf):
    doc = fitz.open(pdf)
    data = " "
    for page in doc:
        # print(page.get_text("text"))
        data += page.get_text("text")
    # print(data)
    return data


if __name__ == "__main__":  
    filename = "/home/vybog/Downloads/name_pd/BalajiCV.pdf"
    data = files(filename)

    mydb = mysql.connector.connect(
        host= "localhost",
        user = "root",
        password = "password",
        database = 'data'
    )
    mycursor = mydb.cursor()
    # creating table 
    # mycursor.execute("CREATE TABLE data (filename VARCHAR(255), data TEXT)")
    
    #show the tables
    # mycursor.execute("SHOW TABLES")

    # Inserting the values
    # sql = "INSERT INTO data(filename, data)values(%s, %s)"
    # val = (filename, data)
    # mycursor.execute(sql, val)
    # mydb.commit()
    # print(mycursor.rowcount, "record inserted")

    # Show the dumped values
    mycursor.execute("SELECT * FROM data")
    myresult = mycursor.fetchall()

    for x in myresult:
        print(x)