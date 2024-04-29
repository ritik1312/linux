# !pip install mysql-connector-python
import mysql.connector
import json

with open("trainings_data.json") as file:
    data = json.load(file)
data["trainings"]

#connection object
conn_obj = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="abcd1234",
    database = "Trainings"
)

cur_obj = conn_obj.cursor()

print("DB successfully connected!")

delete_table = 'DROP TABLE IF EXISTS '
cur_obj.execute(delete_table + 'Participants')
cur_obj.execute(delete_table + 'Training_sessions')
cur_obj.execute(delete_table + 'Instructors')


create_table = 'CREATE TABLE IF NOT EXISTS'

create_instructors_table = create_table + """ Instructors (
    Id INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(50),
    Website VARCHAR(50)
)"""

cur_obj.execute(create_instructors_table)

create_training_sessions_table = create_table + """ Training_sessions (
    Id INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(50),
    Date DATE,
    Completed BOOLEAN,
    Instructor_id INT,
    FOREIGN KEY (Instructor_id) REFERENCES Instructors (Id)
)"""

cur_obj.execute(create_training_sessions_table)


create_participants_table = create_table + """ Participants (
    Id INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(50),
    Email VARCHAR(50),
    Session_id INT,
    FOREIGN KEY (Session_id) REFERENCES Training_sessions (Id)
)"""

cur_obj.execute(create_participants_table)
conn_obj.commit()

from datetime import datetime

def convert_date(date_str, format):
    date_time = datetime.strptime(date_str, format)
    return date_time.date()

insert_into_training_sessions = """INSERT INTO Training_sessions 
(Name, Date, Completed, Instructor_id) VALUES (%s, %s, %s, %s)"""

for training in data["trainings"]:
    name = training["name"]
    date = convert_date(training["date"], format='%B %d, %Y')
    completed = training["completed"]
    instructor = training["instructor"]
    participants_data = training["participants"]
    
    cur_obj.execute("INSERT INTO Instructors (Name, Website) VALUES (%s, %s)", list(instructor.values()))
    
    instructor_id = cur_obj.lastrowid
    cur_obj.execute(insert_into_training_sessions, [name, date, completed, instructor_id])

    session_id = cur_obj.lastrowid
    for participant in participants_data:
        participant['session_id'] = session_id
        cur_obj.execute("INSERT INTO Participants (Name, Email, Session_id) VALUES (%s, %s, %s)", list(participant.values()))


conn_obj.commit()
conn_obj.close()