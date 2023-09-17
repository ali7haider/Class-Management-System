
import sys
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtGui import QIntValidator
import iconsImage
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel,QMessageBox
import sqlite3
from PyQt5.QtCore import QMimeData
from PyQt5.QtGui import QDrag
from PyQt5.QtWidgets import QMainWindow, QFrame 
import json




class LoginSignUpWindow(QMainWindow):
    # Define the __init__() method to initialize the GUI elements
    def __init__(self):
        # Call the __init__() method of the superclass (QMainWindow) to inherit its properties
        super(LoginSignUpWindow, self).__init__()
        # Load the GUI design file "FinalSignInSignUp.ui" using the loadUi() function
        loadUi("FinalSignInSignUp.ui", self)
        # Set the window flag to remove the window frame
        self.setWindowFlag(Qt.FramelessWindowHint)
        
        # Connect the closeAppBtn button to the close() method
        self.btnClose.clicked.connect(self.close)
        # Connect the minimizeAppBtn button to the showMinimized() method
        self.btnMinimize.clicked.connect(self.showMinimized)
        
        # Set the current widget to the sign-in page
        self.stackedWidget.setCurrentWidget(self.SignInPage)
        
        # Connect the btnSignUp button to a lambda function that sets the current widget to the sign-up page
        self.btnSignUp.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.SignUpPage))
        # Connect the btnLogIn_3 button to a lambda function that sets the current widget to the sign-in page
        self.btnLogIn_3.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.SignInPage))
        
        # Connect the lblCreateAccount label to the on_lblCreateAccount_clicked() method when it is clicked
        self.lblCreateAccount.mousePressEvent = self.on_lblCreateAccount_clicked
        
        # Connect the closeAppBtn button to the close() method
        self.btnClose_2.clicked.connect(self.close)
        # Connect the minimizeAppBtn button to the showMinimized() method
        self.btnMinimize_2.clicked.connect(self.showMinimized)
        # Connect the btnRegister button to the addUserToDB() method when it is clicked
        self.btnRegister.clicked.connect(self.addUserToDB)
        # Connect the btnLogInTo button to the LoggingIn() method when it is clicked
        self.btnLogInTo.clicked.connect(self.LoggingIn)
    
    # Moving to SignUp Page by clicking Create Account link
    def on_lblCreateAccount_clicked(self, event):
        # Connecting SignUp Page through Create Account Link
        self.stackedWidget.setCurrentWidget(self.SignUpPage)
    # Define the mousePressEvent() method to handle mouse events and allow the user to drag the window
    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.dragPos = event.globalPos() - self.pos()
            event.accept()

    # Define the mouseMoveEvent() method to handle mouse events and allow the user to drag the window
    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.dragPos)
            event.accept()
    
    # Define the resetValues() method to reset the input fields and error messages
    def resetValues(self):
        self.txtUserName_2.setText("")
        self.txtConfirmPassword.setText("")
        self.txtPassword_2.setText("")
        self.lblPasswordError.setText("")
        self.lblConfirmPasswordError.setText("")
        self.lblUserNameError.setText("")
    def addUserToDB(self):
        # Get user input from text fields
        userName=self.txtUserName_2.text()
        cPassword=self.txtConfirmPassword.text()
        password=self.txtPassword_2.text()
        
        # Connect to database
        connection=sqlite3.connect("DB.db")
        cursor = connection.cursor()
        
        # Execute SQL statement to check if user already exists
        cursor.execute('SELECT * FROM User WHERE UserName=?', (userName,))
        result = cursor.fetchone()
        
        # Close database connection
        connection.close()
        
        # Check if user already exists
        if result is not None:
            self.lblUserNameError.setText("UserName Already Exist")
        else:
            # If user does not exist, check if password and confirm password match and have minimum of 8 characters
            self.lblUserNameError.setText("")
            if len(password)>=8 and len(cPassword)>=8:   
                if password==cPassword:
                    # Connect to database
                    conn=sqlite3.connect("DB.db")
                    
                    # Define SQL statement to insert new user into database
                    sql = "INSERT INTO User(UserName, Password) VALUES(?, ?)"
        
                    # Execute SQL statement with variables as parameters
                    conn.execute(sql, (userName, password))
        
                    # Commit changes to database
                    conn.commit()
        
                    # Close database connection
                    conn.close()
                    
                    # Show success message and reset text fields
                    QMessageBox.information(self, "Success", "User added successfully!")
                    self.txtUserName_2.setText("")
                    self.txtConfirmPassword.setText("")
                    self.txtPassword_2.setText("")
                    self.lblPasswordError.setText("")
                    self.lblConfirmPasswordError.setText("")
                    self.lblUserNameError.setText("")
                    self.resetValues()
                        
                else:
                    # If password and confirm password do not match, show error message
                    self.lblPasswordError.setText("")
                    self.lblConfirmPasswordError.setText("*Password sould be Same")                
            else:
                # If password and confirm password do not have minimum of 8 characters, show error message
                self.lblPasswordError.setText("*Minimum of 8 Character")
                self.lblConfirmPasswordError.setText("*Minimum of 8 Character")
                
    def LoggingIn(self):
        # Get user input from text fields
        userName=self.txtUserNameLogIn.text()
        password=self.txtPasswordLogIn.text()
        
        # Connect to database
        conn = sqlite3.connect("DB.db")
        
        # Define SQL statement to select user by username and password
        sql = "SELECT * FROM User WHERE UserName = ? AND Password = ?"
        
        # Execute SQL statement with parameters and get result
        result = conn.execute(sql, (userName, password)).fetchone()
        
        # Close database connection
        conn.close()
        
        # Check if result is not None
        if result is not None:
            # Authentication successful, store current user and open next window
            self.current_user = result[0]  # assuming the first column is the user ID
            idx=self.current_user
            
            # Print success message and open new window
            print("Authentication successful, opening next window...")
            self.NewWindow(idx)
        
            # Connect to database
            conn = sqlite3.connect("test.db")
        
            # Define SQL statement to select data for current user
            sql = "SELECT * FROM User WHERE Id = ?"
        
            # Execute SQL statement with parameters and get result
            result = conn.execute(sql, (self.current_user,)).fetchall()
        
            # Close database connection
            conn.close()
    
            # Process result, e.g. display data in a table
            print("Data for current user:", result)
        else:
            # Authentication failed, show error message
            print("Authentication failed, please try again.")
            
            self.lblPassword.setText("*Incorrect UserName or Password")   

    def NewWindow(self,idx):
        # Close the current window
        self.close()
        # Create a new instance of the TeacherWindow class and show it
        self.MainWindow=TeacherWindow(idx)
        self.MainWindow.show()

class TeacherWindow(QMainWindow):
    def __init__(self,teacherId):
        CurrentId=teacherId
        self.btnClicked=None
        # Call the parent class constructor
        super(TeacherWindow,self).__init__()
        # Load the UI file for the main window
        loadUi("AdminMainPage.ui",self)     
        # Set the current widget of the stackedWidget to HomePage
        self.stackedWidget.setCurrentWidget(self.HomePage)
        # Call the showingAllClasses method to populate the ClassList widget with all the classes
        self.showingAllClasses(CurrentId)
        # Call the fillClassTable method to populate the ClassTable widget with the data from the database
        self.fillClassTable(CurrentId)
        # Call the fillStudentTable method to populate the StudentTable widget with the data from the database
        self.fillStudentTable()

        # Connect the buttons to their corresponding methods
        self.btnMenuClass.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.ClassPage))
        self.btnHomeMenu.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.HomePage))
        self.btnStudent.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.StudentPage))

        # Call the methods to populate the widgets when their corresponding button is clicked
        self.btnHomeMenu.clicked.connect(lambda:self.showingAllClasses(CurrentId))
        self.btnMenuClass.clicked.connect(lambda:self.fillClassTable(CurrentId))
        self.btnStudent.clicked.connect(lambda:self.fillStudentTable())
        self.btnLogOut.clicked.connect(lambda:self.logOut())
        # Connect the buttons to their corresponding methods
        self.btnAddNewClass.clicked.connect(lambda:self.addNewClass(CurrentId))
        self.btnAddNewStudent.clicked.connect(lambda:self.addNewStudent(CurrentId))
        
    def logOut(self):
        self.close()
        self.SignInSignUp=LoginSignUpWindow()
        self.SignInSignUp.show()
    # Define a function to fill the student table with data from the database
    def fillStudentTable(self):
        # Create a connection to the database
        conn = sqlite3.connect('DB.db')
    
        # Create a cursor object to execute SQL queries
        cursor = conn.cursor()
    
        # Execute a SELECT statement to retrieve data from a table
        cursor.execute("SELECT FullName,Date,BehaviourPoint,RewardPoint,SEN,MoreAble FROM Student")
    
        # Fetch all the rows and store them in a variable
        rows = cursor.fetchall()
    
        # Set the number of rows and columns in the table
        self.tableStudentData.setRowCount(len(rows))
        self.tableStudentData.setColumnCount(6)
        self.tableStudentData.horizontalHeader().setVisible(True)
        self.tableStudentData.setHorizontalHeaderLabels(['Full Name', 'Date of Birth','BehaviourPoint','RewardPoint','SEN','MoreAble'])
        self.tableStudentData.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tableStudentData.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
    
        # Insert the data into the table
        for i, row in enumerate(rows):
            for j, col in enumerate(row):
                self.tableStudentData.setItem(i, j, QTableWidgetItem(str(col)))
    
        # Close the cursor and the database connection
        cursor.close()
        conn.close()
    
    # Define a function to fill the class table with data from the database
    def fillClassTable(self, CurrentId):
        # Create a connection to the database
        conn = sqlite3.connect('DB.db')
    
        # Create a cursor object to execute SQL queries
        cursor = conn.cursor()
    
        # Execute a SELECT statement to retrieve data from a table
        cursor.execute("SELECT ClassName,ClassLimit FROM Class WHERE TeacherId = ?", (CurrentId,))
    
        # Fetch all the rows and store them in a variable
        rows = cursor.fetchall()
    
        # Set the number of rows and columns in the table
        self.tableAllClasses.setRowCount(len(rows))
        self.tableAllClasses.setColumnCount(2)
        self.tableAllClasses.horizontalHeader().setVisible(True)
        self.tableAllClasses.setHorizontalHeaderLabels(['Class Name', 'Limit of Students'])
        self.tableAllClasses.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tableAllClasses.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
    
        # Insert the data into the table
        for i, row in enumerate(rows):
            for j, col in enumerate(row):
                self.tableAllClasses.setItem(i, j, QTableWidgetItem(str(col)))
    
        # Close the cursor and the database connection
        cursor.close()
        conn.close()
    
    # Define a function to clear the home page of all child widgets except the QVBoxLayout
    def clearHomePage(self):
        # Get the home page widget and remove all its child widgets
        for child in reversed(self.HomePage.children()):
            if not isinstance(child, QVBoxLayout):
                child.deleteLater()

    def showingAllClasses(self,CurrentId):
        # Clear the home page
        self.clearHomePage()
        # Create a label to display if there are no classes found
        lbl = QLabel("No classes found")
        lbl.setStyleSheet('color: rgb(77, 78, 186);font-size: 20pt;')
        # Connect to the database
        conn = sqlite3.connect("DB.db")
        cur = conn.cursor()
        # Retrieve all the class names for the current teacher
        cur.execute("SELECT ClassName FROM Class WHERE TeacherId = ?", (CurrentId,))
        classes = cur.fetchall()
        cur.close()
        conn.close()
        # Add buttons to the layout
        layout = self.HomePage.layout()
        layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        layout.setSpacing(20)
        for cls in classes:
            # Clear the label if classes are found
            lbl.setText("")
            # Create a button for each class
            btn = QPushButton(cls[0])
            btn.setStyleSheet('background-color: rgb(77, 78, 186); color: white;font-size: 14pt;')
            # Add the button to the layout
            layout.addWidget(btn)
        # Function to handle the button click event
        def on_button_clicked():
            self.btnClicked = self.sender()
            self.classDetails(CurrentId,self.btnClicked.text())
        # Connect all buttons to the same function
        for i in range(layout.count()):
            widget = layout.itemAt(i).widget()
            if isinstance(widget, QPushButton):
                widget.clicked.connect(on_button_clicked)
                
    def classDetails(self,CurrentId,btnName):
        # Open the ClassDetailsWindow for the selected class
        self.Class=ClassDetailsWindow(CurrentId,btnName)
        self.Class.show()
    
    def addNewClass(self,idx):
        # Open the AddNewClass window
        self.Class=AddNewClass(idx)
        self.Class.show()
        # Connect the Add and Cancel buttons to the appropriate functions
        self.Class.btnAdd.clicked.connect(lambda:self.fillClassTable(idx))
        self.Class.btnCancel.clicked.connect(lambda:self.fillClassTable(idx))
    
    def addNewStudent(self,idx):
        # Open the AddNewStudent window
        self.Class=AddNewStudent(idx)
        self.Class.show()
        # Connect the Add and Cancel buttons to the appropriate functions
        self.Class.btnAdd.clicked.connect(lambda:self.fillStudentTable())
        self.Class.btnCancel.clicked.connect(lambda:self.fillStudentTable())
    
    def mousePressEvent(self, event: QMouseEvent) -> None:
        # Function to handle mouse press events for window dragging
        if event.button() == Qt.LeftButton:
            self.dragPos = event.globalPos() - self.pos()
            event.accept()
    
    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        # Function to handle mouse move events for window dragging
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.dragPos)
            event.accept()
    

class AddNewClass(QMainWindow):
    def __init__(self,idx):
        # idx: current user id
        currentId=idx
        
        # Call the superclass constructor
        super(AddNewClass,self).__init__()
        
        # Load the user interface from the .ui file
        loadUi("AddNewClass.ui",self)
        
        # Connect the 'Cancel' button to the 'close' method of the window
        self.btnCancel.clicked.connect(lambda : self.close())
        
        # Set the validator for the 'Class Limit' text field to only accept integer values
        self.txtClassLimitStudent.setValidator(QIntValidator())
        
        # Connect the 'Add' button to the 'addNewClassToDB' method
        self.btnAdd.clicked.connect(lambda: self.addNewClassToDB(currentId))
    
    def addNewClassToDB(self, currentId):
        # Get the values entered by the user
        className = self.txtClassName.text()
        limit = int(self.txtClassLimitStudent.text())
        rowLimit=int(self.txtRowsStudent.text())
        
        # Check if the required fields are not empty and the limit is greater than 0
        if className!="" and limit>0:
            
            # Check if the limit is less than or equal to 20
            if limit<=20:
                # Connect to the database
                conn = sqlite3.connect("DB.db")
                
                # Define the SQL statement
                sql = "INSERT INTO Class(ClassName, ClassLimit,StudentInOneRow, TeacherId) VALUES (?, ?, ?,?)"
                
                # Execute the SQL statement with the variables as parameters
                conn.execute(sql, (className, limit, rowLimit,currentId))
                
                # Commit the changes to the database
                conn.commit()
                
                # Close the database connection
                conn.close()
                
                # Show a message box to inform the user that the class has been added successfully
                QMessageBox.information(self, "Success", "Class added successfully!")
                
                # Clear the input fields
                self.txtClassName.setText("")
                self.txtClassLimitStudent.setText("")
                self.txtRowsStudent.setText("")
            else:
                # Show an error message to the user if the limit is greater than 20
                self.lblLimitError.setText("*Limit Should be less than 20") 
  
class ClassDetailsWindow(QMainWindow):
    def __init__(self,idx,btnName):
        # Initialize the object with two input arguments, idx and btnName
        self.currentId=idx
        self.btnName=btnName
        self.ClassId=None
        # Set the current id, button name, and ClassId to None
        super(ClassDetailsWindow,self).__init__()
        # Call the superclass constructor
        loadUi("ClassStudents.ui",self)
        # Load the UI from the specified file into the current object
        self.fillSeats()
        # Call the fillSeats method to populate the seats
        self.btnAddStudentToClass.clicked.connect(lambda: self.addingStudentToClass())
        # Connect the "Add Student to Class" button to the addingStudentToClass method
        self.fillStudent()

    def addingStudentToClass(self):
        self.new=AddStudentToClass(self.currentId,self.ClassId)
        self.new.show()
        # self.fillStudent()

    def clearStudentPage(self):
        # get the home page widget and remove all its child widgets
        for child in reversed(self.RegisteredStudent.children()):
           if not isinstance(child, QVBoxLayout):
               child.deleteLater()
           
    def fillSeats(self):
        # connect to the database
        conn = sqlite3.connect("DB.db")
        cur = conn.cursor()
        
        # execute a SELECT query to get the class details
        cur.execute("SELECT ClassLimit,StudentInOneRow,Id FROM Class WHERE TeacherId = ? and ClassName = ?", (self.currentId,self.btnName,))
        classes = cur.fetchall()
        
        # close the cursor and the database connection
        cur.close()
        conn.close()
        
        # extract the relevant class details
        total_seats = classes[0][0]
        num_columns = classes[0][1]
        self.ClassId = classes[0][2]
        
        # create a grid layout to hold the seats
        grid = QGridLayout()
        
        # create and add labels for each chair with a border
        for i in range(total_seats):
            # calculate the row and column for this chair
            row = i // num_columns
            col = i % num_columns
            
            # create a frame to hold the chair label
            chair_frame = QFrame()
            chair_frame.setStyleSheet("border: 2px solid #4d4eba; ")
            chair_frame.setFrameShape(QFrame.Box)
            
            # create a layout for the chair frame
            chair_frame_layout = QGridLayout(chair_frame)
            
            # create a label for the chair
            chair_label = QLabel(f"Chair {i+1}")
            chair_label.setStyleSheet("QFrame { color: #4d4eba; }")
            chair_label.setAlignment(Qt.AlignCenter)
            chair_label.setAcceptDrops(True)
            
            # add the chair label to the chair frame layout
            chair_frame_layout.addWidget(chair_label, 0, 0)
            
            # add the chair frame to the grid layout
            grid.addWidget(chair_frame, row, col)
            
            # set the minimum height of the chair frame
            chair_frame.setMinimumHeight(70)
            chair_frame.setAcceptDrops(True)
    
            # set the cursor to a pointing hand
            chair_frame.setCursor(Qt.PointingHandCursor)
    
        grid_widget = QWidget()
        grid_widget.setLayout(grid)
        grid_widget.setStyleSheet("border: none;")
        seats_layout = self.Seats.layout()
        seats_layout.addRow(grid_widget)
    def fillStudent(self):
        # connect to the database
        conn = sqlite3.connect("DB.db")
        cur = conn.cursor()
        # select the full names and IDs of all students enrolled in the current class
        cur.execute("SELECT FullName,S.Id FROM Student S JOIN Enroll E ON S.Id = E.StudentId AND E.ClassId=?;",(self.ClassId,))
        classes = cur.fetchall()
        cur.close()
        conn.close()
       
        # create a grid layout with 2 columns
        grid = QGridLayout()
        num_columns=2
    
        # create and add labels for each student with a profile picture and name label
        for i in range(len(classes)):
            row = i // num_columns
            col = i % num_columns
            student_frame = QFrame()
            student_frame_layout = QVBoxLayout(student_frame)
            
            # create a profile pic widget with a default image
            profile_pic = QLabel()
            profile_pic.setPixmap(QPixmap("Profile.png")) # replace with path to your default profile pic
            profile_pic.setFixedSize(70, 70)
            student_frame_layout.addWidget(profile_pic)
        
            # create a label for the student name
            name_label = QLabel(classes[i][0]+str(classes[i][1]))
            name_label.setAlignment(Qt.AlignLeft)
            name_label.setContentsMargins(25, 0, 0, 0)
            student_frame_layout.addWidget(name_label)
        
            # make the student frame draggable
            student_frame.setMouseTracking(True)
            
            # make the student frame clickable and connect to the handleProfileClick function
            student_frame.setCursor(Qt.PointingHandCursor) # set the cursor to indicate that it's clickable
            def handle_mouse_press(event, sid, s):
                self.handleProfileClick(sid)
                self.startDrag(s, event)


            # connect the mousePressEvent to the handle_click function
            student_frame.mousePressEvent = lambda event, sid=classes[i][1], s=student_frame: handle_mouse_press(event,sid,s)
            student_frame.mousePressEvent = lambda event, sid=classes[i][1], s=student_frame: handle_mouse_press(event, sid, s)
            
            grid.addWidget(student_frame, row, col)
    
        # create a widget to hold the grid and add it to the RegisteredStudent layout
        grid_widget = QWidget()
        grid_widget.setLayout(grid)
        seats_layout = self.RegisteredStudent.layout()
        seats_layout.addRow(grid_widget)
    def startDrag(self, frame, event):
        # set the current student to the student whose profile is being dragged
        self.current_student = frame
        
        # create a mime data object to hold the data being transferred
        mime_data = QMimeData()
        
        # create a pixmap object to use as the drag cursor
        pixmap = QPixmap("ProfileDrag.png")
        
        # create a drag object and set its mime data and drag cursor
        drag = QDrag(frame)
        drag.setMimeData(mime_data)
        drag.setPixmap(pixmap)
        
        # start the drag operation
        drag.exec_(Qt.MoveAction)

        

    def handleProfileClick(self, student_id):
        # connect to the database
        conn = sqlite3.connect("DB.db")
        # create a cursor object
        cur = conn.cursor()
        # execute a SELECT statement to retrieve information for the selected student
        cur.execute("SELECT * FROM Student WHERE Id = ?", (student_id,))
        # fetch all rows of the query result
        classes = cur.fetchall()
        # close the cursor and database connection
        cur.close()
        conn.close()
        # set the student name label to the first field of the first row of the query result
        self.lblName.setText(classes[0][1])
        # set the student date of birth label to the second field of the first row of the query result
        self.lblDate.setText(classes[0][2])
        # set the student behaviour points label to the third field of the first row of the query result as a string
        self.lblBehaviourPoint.setText(str(classes[0][3]))
        # set the student reward points label to the fourth field of the first row of the query result as a string
        self.lblRewardPoint.setText(str(classes[0][4]))
        # set the student SEN label to "Yes" if the fifth field of the first row of the query result is 1, otherwise set it to "No"
        sen = "No"
        if classes[0][5] == 1:
            sen = "Yes"
        self.lblSEN.setText(sen) 
        # set the student More Able label to "Yes" if the sixth field of the first row of the query result is 1, otherwise set it to "No"
        moreAble = "No"
        if classes[0][6] == 1:
            moreAble = "Yes"
        self.lblMoreAble.setText(moreAble)

        
    

class AddStudentToClass(QMainWindow):
    def __init__(self, teacherId, Id):
        # Set class ID and teacher ID attributes
        self.ClassId = Id
        self.TeacherId = teacherId
        super(AddStudentToClass, self).__init__()
        # Load the user interface from AddStudentToClass.ui file
        loadUi("AddStudentToClass.ui", self)
        # Call the fillStudentTable method to populate the table with students' data
        self.fillStudentTable()

    def fillStudentTable(self):
        # Connect to the DB database
        conn = sqlite3.connect('DB.db')

        # Create a cursor object to execute SQL statements
        cursor = conn.cursor()

        # Execute a SELECT statement to retrieve student data from the Student table
        cursor.execute("SELECT FullName, Date, BehaviourPoint, RewardPoint, SEN, MoreAble, S.Id FROM Student S LEFT JOIN Enroll ON S.Id = Enroll.StudentId AND Enroll.ClassId = ? WHERE Enroll.StudentId IS NULL;", (self.ClassId,))

        # Fetch all the rows returned by the SELECT statement
        rows = cursor.fetchall()

        # Set the number of rows and columns in the table
        self.tableStudentData.setRowCount(len(rows))
        self.tableStudentData.setColumnCount(8)
        self.tableStudentData.hideColumn(7)

        # Set the horizontal header visible and its labels
        self.tableStudentData.horizontalHeader().setVisible(True)
        self.tableStudentData.setHorizontalHeaderLabels(['Add', 'Full Name', 'Added Date', 'BehaviourPoint', 'RewardPoint', 'SEN', 'MoreAble'])
        self.tableStudentData.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tableStudentData.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

        # Insert the data into the table
        for i, row in enumerate(rows):
            # Create an 'Add' button and connect it to the addRowData slot
            button = QPushButton('Add')
            button.clicked.connect(lambda _, row=i: self.addRowData(row))  # connect slot to button clicked signal
            self.tableStudentData.setCellWidget(i, 0, button)
            for j, col in enumerate(row):
                # Add a QTableWidgetItem for each column of the row
                self.tableStudentData.setItem(i, j+1, QTableWidgetItem(str(col)))

        # Close the cursor and the database connection
        cursor.close()
        conn.close()

    def addRowData(self, row):
        # create an empty list to store the data for this row
        row_data = []
        # iterate over all columns in the row
        for j in range(self.tableStudentData.columnCount()):
            # get the QTableWidgetItem object for this cell
            item = self.tableStudentData.item(row, j)
            # if the cell is not empty, append its text to the row_data list
            if item is not None:
                row_data.append(item.text())
            # if the cell is empty, append an empty string to the row_data list
            else:
                row_data.append('')
        
        # call a method to save the row data to a database or file
        self.addEnrollToDB(row_data[-1])
    
    def addEnrollToDB(self, studentId):
        # create a connection to the SQLite database
        conn = sqlite3.connect("DB.db")
        # define an SQL query to insert a new record into the Enroll table
        sql = "INSERT INTO Enroll(StudentId,ClassId, TeacherId) VALUES (?, ?, ?)"
        
        # execute the SQL query with the student ID, class ID, and teacher ID as parameters
        conn.execute(sql, (int(studentId),int(self.ClassId),int(self.TeacherId)))
        
        # commit the changes to the database
        conn.commit()
        
        # close the database connection
        conn.close()
        
        # show an information message box to indicate success
        QMessageBox.information(self, "Success", "Student added successfully!")
        
        # call a method to refill the table with updated data
        self.fillStudentTable()

    
        
        
class AddNewStudent(QMainWindow):
    def __init__(self,idx):
        currentId=idx
        super(AddNewStudent,self).__init__()
        loadUi("AddNewStudent.ui",self)

        # Connect cancel button to close window
        self.btnCancel.clicked.connect(lambda : self.close())

        # Set validators for BehaviourPoint and RewardPoint text fields
        self.txtBehaviourPoint.setValidator(QIntValidator())
        self.txtRewardPoint.setValidator(QIntValidator())

        # Connect add button to addNewStudentToDB method
        self.btnAdd.clicked.connect(lambda: self.addNewStudentToDB(currentId))

    def addNewStudentToDB(self,idx):
        # Get values from text fields and radio buttons
        fullName = self.txtFullName.text()
        DOB = self.dateDOB.text()
        behaviourPoint = int(self.txtBehaviourPoint.text())
        rewardPoint = int(self.txtRewardPoint.text())
        sen=None
        more=None
        if self.radioSen.isChecked():
            sen=True
        else:
            sen=False
        if self.radioMoreAble.isChecked():
            more=True
        else:
            more=False

        # Check if fullName field is not empty
        if fullName!="":
        
            # Connect to database
            conn = sqlite3.connect("DB.db")
            sql = "INSERT INTO Student(FullName,Date, BehaviourPoint,RewardPoint,SEN,MoreAble, TeacherId) VALUES (?, ?, ?,?,?,?,?)"
        
            # Execute SQL statement with variables as parameters
            conn.execute(sql, (fullName, DOB, behaviourPoint,rewardPoint,sen,more,idx))
        
            # Commit changes to database
            conn.commit()
        
            # Close database connection
            conn.close()

            # Show success message box and clear text fields
            QMessageBox.information(self, "Success", "Student added successfully!")
            self.txtFullName.setText("")
            self.txtRewardPoint.setText("")
            self.txtBehaviourPoint.setText("")

    
            
      
# Define the main function
def main():
    # Create an instance of the QApplication
    app = QApplication(sys.argv)

    # Create an instance of the LoginSignUpWindow and show it
    window = TeacherWindow(1)
    window.show()

    # Run the application and exit when done
    sys.exit(app.exec_())

# Call the main function
if __name__ == "__main__":
    main()