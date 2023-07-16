import mysql.connector
from mysql.connector import Error
import csv


def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = mysql.connector.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        if connection.is_connected():
            print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection


connection = create_connection(
    "Task_manager", "root", "12345678", "127.0.0.1", "3306"
)

def update_quary(query, data=0):
    cursor = connection.cursor()
    if data == 0:
        cursor.execute(query)
    else:
        cursor.execute(query, data)
    result = cursor.rowcount
    connection.commit()
    return result


def execute_query(query, data=0):
    cursor = connection.cursor()
    if data == 0:
        cursor.execute(query)
    else:
        cursor.execute(query, data)
    result = cursor.fetchone()
    connection.commit()
    return result


def execute_multi_query(query, data=0):
    cursor = connection.cursor()
    cursor.execute(query, data)
    if cursor.description is not None:
        result = cursor.fetchall()
    else:
        result = None
    connection.commit()
    return result


def Create_new_user(row):
    user_id = row[0]
    First_Name = row[1]
    Last_Name = row[2]
    Job_Title = row[3]
    Email = row[4]
    user = (user_id, First_Name, Last_Name, Email, Job_Title)
    create_users = """INSERT INTO users (User_id, First_name, Last_name, email, job_title) VALUES (%s, %s, %s, %s, %s);"""
    execute_query(create_users, user)


def Update_user(row):
    user_id = row[0]
    First_Name = row[1]
    Last_Name = row[2]
    Job_Title = row[3]
    Email = row[4]
    user = (user_id, First_Name, Last_Name, Email, Job_Title)
    newDetail = (user[1], user[2], user[3], user[4], user[0])
    update_user = """ UPDATE users SET First_Name = %s, Last_Name = %s, Email = %s, Job_Title = %s WHERE user_id = %s ;"""
    execute_query(update_user, newDetail)
        

def insert_and_update_users():
    with open('docs\Employees.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        cursor = connection.cursor()
        for row in csv_reader:
            if row[5] != "FALSE":
                check_user_query = "SELECT * FROM users WHERE User_id = %s"
                user_exists = execute_query(check_user_query, (row[0],))
                if user_exists:
                    Update_user(row)
                else:
                    Create_new_user(row)
            


    
    print("imporet executed successfully")
    cursor.close()
    # connection.close()

insert_and_update_users()





def main():

    def sign_in_log_in():
        num = int(input("Welcome! To sign in using your full name or email, press 1. To log in via password, press 2: "))
        if num == 1:
            sign_in()
        if num == 2:
            log_in()

    def crate_task(user_id):
        cursor = connection.cursor()
        Task_title = input("Type a title for your task: ")
        Description = input("Type a Description for your task: ")
        Status = 1
        Due_date = input("Type a Due date for your task, in YYYY-MM-DD format: ")
        priority_level = input("Type a priority level for your task, You can choose high, medium or low level: ")
        Category_id = input("Type a Category id for your task: ")
        new_task = (Task_title, Description, Status, Due_date, priority_level, Category_id)
        crate_new_task = """INSERT INTO Tasks (Task_title, Description, Status, Due_date, priority_level, Category_id)
        VALUES (%s, %s, %s, %s, %s, %s);"""
        cursor.execute(crate_new_task, new_task)
        last_insert_id = cursor.lastrowid
        connection.commit()
        add_Collaborators = """INSERT INTO Collaborators (Task_id, User_id) VALUES (%s, %s);"""
        new_link_task_user = (last_insert_id, user_id)
        execute_query(add_Collaborators, new_link_task_user)

    def Check_if_empty(user_id):
        isempti = """SELECT Task_title, Description, Status, Due_date, priority_level from 
                    Tasks t join Collaborators C on t.Task_id=C.Task_id where User_id = %s ;"""
        res = execute_multi_query(isempti, (user_id, ))
        if len(res) > 0:
            return True
        else:
            return False


    def displey_tasks(user_id):
        if Check_if_empty(user_id):
            userid = (user_id, )
            order = input("""You can choose your preferred sorting method \n
                                To sort by priority level, press 1\n
                                To sort by Category_id, press 2.\n
                                For unsorted display, press any key: """)
            match order:
                case 1:
                    orderby = "priority_level"
                case 2:
                    orderby = "Due_date"
                case _:
                    orderby = "priority_level"  
            tasks = f"""SELECT t.Task_id, Task_title, Description, Status, Due_date, priority_level from 
                    Tasks t join Collaborators C on t.Task_id=C.Task_id where User_id = %s 
                    order by  {orderby} ;"""
            
            res = execute_multi_query(tasks, userid)
            for row in res:
                for col in row:
                    print(col, end=' ')
                print()
        else:
            print("You have no tasks to display")
            Navigation_fun(user_id)
        

    def filter_tasks(user_id):
        if Check_if_empty(user_id):
            filter = int(input("""You can choose which tasks will be displayed for you.\n
                                    To filter by priority, tap 1\n
                                    To filter by date, tap 2\n
                                    To filter by category, tap 3: """))
            match filter:
                case 1:
                    filter_priority(user_id)
                case 2:
                    filter_date(user_id)
                case 3:
                    filter_category(user_id)
                case _:
                    displey_tasks(user_id)
        else:
            print("You have no tasks to display")
            Navigation_fun(user_id)

    def filter_priority(user_id):
        select_priority = input("You can type the priority level you want to focus on. high, medium, low: ")
        match select_priority:
            case "high":
                priority_level = "high"
            case "medium":
                priority_level = "medium"
            case "low":
                priority_level = "low"
            case _:
                priority_level = "high"  
        filterby = """SELECT Task_title, Description, Status, Due_date, priority_level from 
                        Tasks t join Collaborators C on t.Task_id=C.Task_id where User_id = %s and priority_level = %s and Status = 1;"""
        res = execute_multi_query(filterby, (user_id, priority_level))
        for row in res:
                for col in row:
                    print(col, end=' ')
                print()

    def filter_date(user_id):
        select_date = input("You can choose to display tasks until a certain date. Enter the desired number of months: ")
        get_time = f"""SELECT Task_title, Description, Status, Due_date, priority_level from 
                        Tasks t join Collaborators C on t.Task_id=C.Task_id 
                        where User_id = {user_id} and TIMESTAMPDIFF(month, CURDATE(), Due_date) < {select_date} and Status = 1;"""
        res = execute_multi_query(get_time)
        for row in res:
                for col in row:
                    print(col, end=' ')
                print()

    def filter_category(user_id):
        Category =  input("""Please select the category you would like to view: """)
        get_Category = f"""SELECT Task_title, Description, Status, Due_date, priority_level, Category_name
                            from 
                            Tasks t join Collaborators C on t.Task_id = C.Task_id 
                            join categories a on t.Category_id=a.Category_id
                            where User_id = {user_id} and a.Category_name = "{Category}" and Status = 1;"""
        res = execute_multi_query(get_Category)
        for row in res:
                for col in row:
                    print(col, end=' ')
                print()

    def execute_update(user_id, task_num, detail, newdetail):
        update_task = f""" UPDATE Tasks SET {detail} = "{newdetail}" WHERE Task_id = {task_num} ;"""
        num = update_quary(update_task)
        if num != 0:
            print("The update was completed successfully")
        else:
            print("something went wrong, try again")
            update_task(user_id)

    def update_task(user_id):
        displey_tasks(user_id)
        task_num = int(input("Select the task you want to update: "))
        num = int(input("""You can choose to update every detail in the displayed tasks.
                        to update title, press 1
                        to update Description, press 2
                        to update Status, press 3
                        to update Due date, press 4
                        to update priority level, press 5
                        to update Category, press 6: """))
        
        match num:
            case 1:
                case = "Task_title"
                newdetail = input("Please type the update you wish to perform: ")
                execute_update(user_id, task_num, case, newdetail)
            case 2:
                case = "Description"
                newdetail = input("Please type the update you wish to perform: ")
                execute_update(user_id, task_num, case, newdetail)
            case 3:
                case = "Status"
                newdetail = int(input("Please type the update you wish to perform: "))
                if newdetail != 0:
                    newdetail = 1
                else:
                    newdetail = 0
                execute_update(user_id, task_num, case, newdetail)
            case 4:
                case = "Due_date"
                newdetail = input("Please type the update you wish to perform, in YYYY-MM-DD format: ")
                execute_update(user_id, task_num, case, newdetail)
            case 5:
                case = "priority_level"
                newdetail = input("Please type the update you wish to perform, You can choose high, medium or low level: ")
                execute_update(user_id, task_num, case, newdetail)
            case 6:
                case = "Category_id"
                newdetail = input("Please type the update you wish to perform: ")
                execute_update(user_id, task_num, case, newdetail)   

    def delete_task(user_id):
        displey_tasks(user_id)
        Task_id = int(input("Select the task you want to delete: "))
        delete_Collaborators = f"""DELETE FROM Collaborators WHERE Task_id = {Task_id};"""
        execute_query(delete_Collaborators)
        delete_task = f"""DELETE FROM tasks WHERE Task_id = {Task_id};"""
        res = update_quary(delete_task)
        if res:
            print("The task was successfully deleted")
        else:
            print("something went wrong, try again")
            Navigation_fun(user_id)
      
        
    def Navigation_fun(user_id):
        num = int(input("""what do you want to do?\n
                                    To create a task, tap 1\n 
                                    To view your tasks, tap 2\n
                                    To view tasks by filter, tap 3\n
                                    To update task, tap 4\n
                                    To delete a task, tap 5: """))
        match num:
            case 1:
                crate_task(user_id)
            case 2:
                displey_tasks(user_id)
            case 3:
                filter_tasks(user_id)
            case 4:
                update_task(user_id)
            case 5:
                delete_task(user_id)
            case _:
                print("The key you entered is invalid, please restart the operation")


        
    def sign_in():
            username = input("Please enter your user name: ")
            if (" ") in username:
                splitname = username.split(" ")
                newname = (splitname[0], splitname[1])
                print(f"hello {newname}")
                find_user_name = """ select * from users where first_name = %s and Last_Name = %s """
                res = execute_query(find_user_name, newname)
            else:
                find_user_email = """ select * from users where email = %s  """
                res = execute_query(find_user_email, (username,))
            if res:
                if res[-1] == None:
                    password = int(input("You have not yet set a password. Please enter a password of up to 50 digits: "))
                    set_password = """UPDATE users set password = %s where user_id = %s ;"""
                    addpassword = (password, res[0])
                    num = update_quary(set_password, addpassword)
                    if num != 0:
                        print("Password set successfully")
                        Navigation_fun(res[0])
                    else:
                        print("something went wrong, try again")
                        sign_in()
                if res[-1] != None:
                    log_in()
            else:
                print("The user does not exist in the system")

    def log_in():
        cursor = connection.cursor()
        password = input("Please enter your password: ")
        find_user_password = """ select * from users where password = %s  """
        res = execute_query(find_user_password, (password,))
        if res:
            print("You have successfully connected to your user")
            Navigation_fun(res[0])
        else:
            print("The password you entered does not exist in the system")
            cursor.close()


    sign_in_log_in()

main()
