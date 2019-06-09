from flask import Flask, jsonify, abort, request, url_for, render_template, redirect
import mysql.connector, datetime

app = Flask(__name__)
wsgi_app = app.wsgi_app

# connect to a database
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='password',
    database='temperatureData'
)

mycursor = mydb.cursor()

# main webpage with basic overview of room temperature
@app.route('/', methods=['GET'])
def homepage():
    data = update_data()
    myresult = data[0]
    last = data[1]
    status = check_status()
    
    return render_template('index.html', device = last[0][0], status = status, lowest = myresult[0][0], highest = myresult[1][0], average = myresult[2][0], current = last[0][1], time = last[0][2])

# reset all values in the database
@app.route('/reset', methods=['GET'])
def reset_data():
    names = ["Lowest", "Highest", "Average", "Count"]
    val = ()
    for i in range(len(names)):
        sql = "UPDATE stats SET value = %s WHERE name = %s"
        if i < 2:
            val = (None, names[i])
        else:
            val = (0, names[i])    
        mycursor.execute(sql, val)
    mycursor.execute("TRUNCATE TABLE temp")
    
    sql = "INSERT INTO temp (name, temperature, timestamp) values(%s, %s, %s)"
    val = ("esp8266#2", 0, str(datetime.datetime.now().strftime("%H:%M:%S %d/%m/%y")))
    mycursor.execute(sql, val)
    mydb.commit()
    return redirect('/')

# get temperature from esp8266
@app.route('/postjson', methods=['POST'])
def postJsonHandler():
    jsonData = request.json
    name = str(jsonData['title'])
    temperature = float(jsonData['temperature'])
    createDate = str(datetime.datetime.now().strftime("%H:%M:%S %d/%m/%y"))
    sql = "INSERT INTO temp (name, temperature, timestamp) VALUES (%s, %s, %s)"
    val = (name, temperature, createDate)
    mycursor.execute(sql, val)
    mydb.commit()
    
    update_stats(temperature)
    return "Json data received."

def update_stats(temp):
    mycursor.execute("SELECT value FROM stats")
    myresult = mycursor.fetchall()
    lowest = myresult[0][0]
    highest = myresult[1][0]
    average = myresult[2][0]
    count = myresult[3][0]
    
    if lowest is None:
        sql = "UPDATE stats SET value = %s WHERE name = %s"
        val = (temp, "Lowest")
        mycursor.execute(sql, val)
        sql = "UPDATE stats SET value = %s WHERE name = %s"
        val = (temp, "Highest")
        mycursor.execute(sql, val)
    elif temp < lowest:
        sql = "UPDATE stats SET value = %s WHERE name = %s"
        val = (temp, "Lowest")
        mycursor.execute(sql, val)
    elif temp > highest:
        sql = "UPDATE stats SET value = %s WHERE name = %s"
        val = (temp, "Highest")
        mycursor.execute(sql, val)
    
    average = (average * count + temp) / (count + 1)
    sql = "UPDATE stats SET value = %s WHERE name = %s"
    val = (average, "Average")
    mycursor.execute(sql, val)
    sql = "UPDATE stats SET value = %s WHERE name = %s"
    val = (count + 1, "Count")
    mycursor.execute(sql, val)
        
    mydb.commit()
    
def update_data():
    mycursor.execute("SELECT value FROM stats")
    myresult = mycursor.fetchall()
    mycursor.execute("SELECT name, temperature, timestamp FROM temp ORDER BY id DESC LIMIT 1")
    last = mycursor.fetchall()
    
    return (myresult, last)

def check_status():
    time_between = .25
    mycursor.execute("SELECT timestamp FROM temp ORDER BY id DESC LIMIT 1")
    last = mycursor.fetchone()
    now = datetime.datetime.now().strftime("%H:%M:%S %d/%m/%y")
    last_record = datetime.datetime.strptime(last[0], "%H:%M:%S %d/%m/%y")
    time_now = datetime.datetime.strptime(now, "%H:%M:%S %d/%m/%y")
    result = time_now - last_record
    
    if float(result.total_seconds() / 60) > time_between:
        return False
    else:
        return True

def get_data(size):
    mycursor.execute("SELECT temperature, timestamp FROM temp")
    myresult = mycursor.fetchall()
    data = []
    
    if len(myresult) >= size:
        for i in range(size - 1, -1, -1):
            data.append(myresult[len(myresult) - i - 1])
    else:
        for i in range(len(myresult) - 1, -1, -1):
            data.append(myresult[len(myresult) - i - 1])
        
    return data

# display values from database
@app.route('/get-data', methods=['GET'])
def get_tasks():
    data = get_data(10)
    return jsonify({'my_data': data})

if __name__ == '__main__':
    app.run(host='localhost', port=8888, debug=True)
    