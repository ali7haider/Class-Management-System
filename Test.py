

import sqlite3
conn=sqlite3.connect("DB.db")

sql = '''CREATE TABLE User (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            UserName TEXT NOT NULL,
            Password TEXT NOT NULL
        )'''

# Execute SQL statement to create User table
conn.execute(sql)

# Commit changes to database
conn.commit()

# Close database connection
conn.close()

conn=sqlite3.connect("DB.db")
sql = '''CREATE TABLE Class (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            ClassName TEXT NOT NULL,
            ClassLimit INTEGER NOT NULL,
            StudentInOneRow INTEGER NOT NULL,
            TeacherId INTEGER,
            FOREIGN KEY (TeacherId) REFERENCES Teacher(Id)
        )'''

# Execute SQL statement to create User table
conn.execute(sql)

# Commit changes to database
conn.commit()

# Close database connection
conn.close()

conn=sqlite3.connect("DB.db")
sql = '''CREATE TABLE Student (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            FullName TEXT NOT NULL,
            Date TEXT ,
            BehaviourPoint INTEGER,
            RewardPoint INTEGER,
            SEN BOOLEAN,
            MoreAble BOOLEAN,
            TeacherId INTEGER,
            FOREIGN KEY (TeacherId) REFERENCES Teacher(Id)
        )'''

# Execute SQL statement to create User table
conn.execute(sql)

# Commit changes to database
conn.commit()

# Close database connection
conn.close()

conn=sqlite3.connect("DB.db")
sql = '''CREATE TABLE Enroll (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            StudentId TEXT NOT NULL,
            ClassId INTEGER NOT NULL,
            TeacherId INTEGER NOT NULL,
            Seat Text,
            FOREIGN KEY (StudentId) REFERENCES Student2(Id)
            FOREIGN KEY (ClassId) REFERENCES CLass3(Id)
            FOREIGN KEY (TeacherId) REFERENCES User(Id)
        )'''

# Execute SQL statement to create User table
conn.execute(sql)

# Commit changes to database
conn.commit()

# Close database connection
conn.close()