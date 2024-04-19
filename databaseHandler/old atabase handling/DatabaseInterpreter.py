import threading
import time
import queue

import pyodbc

from DatabseRequest import DatabaseRequest


def execute_query(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    return rows


def execute_procedure(connection, procedure_name, **kwargs):
    cursor = connection.cursor()
    params = ','.join([f'@{key}=?' for key in kwargs.keys()])
    values = list(kwargs.values())

    try:
        cursor.execute(f"EXEC {procedure_name} {params}", *values)

        try:
            rows = cursor.fetchall()
        except pyodbc.Error as e:
            rows = None

        connection.commit()
        return rows


    except pyodbc.Error as e:
        print(e)
        return None

class DatabaseInterpreter:


    def __init__(self, conn_str):
        self.conn_str = conn_str
        self.my_thread = None
        self.instructions_queue = queue.Queue()
        self.log = queue.Queue()
        self.is_running = True

    def threadingFunction(self):

        # Establishing a connection to the database
        connection = pyodbc.connect(self.conn_str)
        print("Connected to the database.")

        while self.is_running:
            if not self.instructions_queue.empty():
                DBrequest = self.instructions_queue.get()

                if DBrequest.request.lower() == 'exit':
                    break

                try:
                    if DBrequest.request.lower().startswith('select'):

                        # Execute a query and display the results
                        DBrequest.result = execute_query(connection, DBrequest.request)


                    elif DBrequest.request.lower().startswith('exec'):

                        args = DBrequest.request.split("\t")[1:]

                        procedure_name = args[0]
                        procedure_args = args[1:]
                        params = {}
                        for arg in procedure_args:
                            key, value = arg.split('=')
                            params[key.strip('@')] = value.strip()

                        DBrequest.result = execute_procedure(connection, procedure_name, **params)

                    else:
                        DBrequest.errorMessage = "Invalid command."

                except pyodbc.Error as e:
                    DBrequest.errorMessage = e

                self.log.put(DBrequest)
                DBrequest.done=True
            else:
                time.sleep(1)

    def startInterpreter(self):
        self.my_thread = threading.Thread(target=self.threadingFunction)
        self.my_thread.start()

    def safeStopInterpreter(self):
        self.addInstruction(DatabaseRequest('EXIT'))

    def killInterpreter(self):
        self.is_running=False
        self.addInstruction(DatabaseRequest('EXIT'))

    def addInstruction(self, instruction):
        self.instructions_queue.put(instruction)


if __name__ == "__main__":
    interpreter1 = DatabaseInterpreter('DRIVER={SQL Server};SERVER=localhost\\SQLEXPRESS;DATABASE=RPG;Trusted_Connection=yes;')
    interpreter1.startInterpreter()
    request1 = DatabaseRequest("select * from Race")
    interpreter1.addInstruction(request1)
    interpreter1.safeStopInterpreter()
    while(not request1.done):
        time.sleep(0.5)
    print(interpreter1.log.get().result)
