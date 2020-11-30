import socket
import sys
import time
from time import sleep
import mysql.connector
import datetime
import prettytable
import PySimpleGUI as sg
import base64
import threading
import logging
import queue
#end of imports

#region logo
logo="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"
#endregion

def conn_listen(gui_queue):
    s.listen(1)
    global conn, addr
    try:
        conn, addr=s.accept()
        gui_queue.put("ConnEstb")
    except:
        pass


sg.theme("light purple")
# STEP 1 define the layout
layout = [[sg.Image(data=logo)],
            [sg.Button('Host (as Server)'), sg.Button('Join (as Client)')]
]

#STEP 2 - create the window
window = sg.Window('easyChat', layout, grab_anywhere=True, icon=r"D:\Downloads\ec2.ico")


# STEP3 - the event loop
while True:
    event, values = window.read()   # Read the event that happened and the values dictionary
    if event == sg.WIN_CLOSED:     # If user closed window with X 
        exit()
        break



    elif event == 'Host (as Server)':
        window.close(); del window


        layout = [[sg.Image(data=logo, size=(400,400))],
                        [sg.Text('Enter your name, Server.',justification='center',size=(50,1))],      
                        [sg.InputText("Dorian",size=(57,1), key="-name-")],
                        [sg.Text('...',justification='center',size=(50,1))],
                        [sg.Text('Enter your sql credentials.',justification='center',size=(50,1))],
                        [sg.Text(' If this is your first time hosting on this device, we will create a new',justification='center',size=(50,1))],
                        [sg.Text('databse called <easychat>,',justification='center',size=(50,1))],
                        [sg.Text('and within it two new tables for the purposes of this program.',justification='center',size=(50,1))],
                        [sg.Text('If not, we will use the dababase and tables created on the first use.',justification='center',size=(50,1))],
                        [sg.InputText(size=(57,1),key="-pwd-")],
                        [sg.Submit('Log in',size=(50,1))]]
        sg.theme('Light Purple')
        window = sg.Window('easyChat', layout)
        event, values = window.read() 
        if event == sg.WIN_CLOSED:
            exit()
        window.close(); del window

        server_name = values["-name-"] or "Server"
        server_pwd=str(values["-pwd-"])




        mydb=mysql.connector.connect(
            host="localhost",
            user="root",
            #region
            password=server_pwd
            #endregion
        )

        mycursor = mydb.cursor()

        mycursor.execute("SHOW DATABASES like 'easychat'")
        count3=0
        for i in mycursor:
            count3+=1

        if count3==0:
            mycursor.execute("CREATE DATABASE easyChat")
            

        mycursor.execute("USE easyChat")

        mycursor.execute("show tables like 'chatrecord'")
        count1=0
        for i in mycursor:
            count1+=1

        mycursor.execute("show tables like 'lastchat'")
        count2=0
        for i in mycursor:
            count2+=1

        if count1==0:
            mycursor.execute("CREATE TABLE chatrecord (time varchar(50), name VARCHAR(255), message VARCHAR(255))")

        if count2==0:
            mycursor.execute("CREATE TABLE lastchat (time varchar(50), name VARCHAR(255), message VARCHAR(255))")
            mycursor.execute("insert into lastchat values('NULL','NULL','NULL')")
            mydb.commit()



        #ini

        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host=socket.gethostname() #gets local host name of your device
        ipaddr=socket.gethostbyname(host)
        host=ipaddr
        port=2903
        s.bind(('0.0.0.0',port))
        print(f"Server done binding to host {host} and port 2903 successfully.")
        print("Server is waiting for incoming connections.")

        layout=[[sg.Text(f"Server will start on host: {host}  and port: 2903",size=(50,1))],
                        [sg.Text("Binded all IPv4 to 2903.",size=(50,1))],
                        [sg.Text("Waiting for incoming connections.",size=(50,1))],
                        [sg.Image(r"D:\DnD\purpleload.gif",key="-GIF-",background_color="black")],
                        [sg.Button("Cancel")]]
        sg.theme('Light Purple')
        window = sg.Window('easyChat', layout)

        gui_queue = queue.Queue()

        while True:
            event,values= window.read(timeout=70)
            if event == sg.WIN_CLOSED:
                exit()
            if event == "Cancel":
                exit()
            window['-GIF-'].update_animation(r"D:\DnD\purpleload.gif",  time_between_frames=100)
            thread_id = threading.Thread(target=conn_listen, args=(gui_queue,), daemon=True)
            thread_id.start()


            try:
                message = gui_queue.get_nowait()    # see if something has been posted to Queue
            except queue.Empty:                     # get_nowait() will get exception when Queue is empty
                message = None
            
            if message is not None:
                break


        window.close(); del window

        sg.popup_no_buttons(addr, "has connected to the server, and is now online.", keep_on_top=True, no_titlebar=True,auto_close=True,auto_close_duration=2)

        print(addr, "has connected to the server, and is now online.")
        current_time = datetime.datetime.now().strftime("%d/%m/%Y--%H:%M:%S")
        print(current_time)
        print()

        records_server=prettytable.PrettyTable(["Time","User","Message"])

        mycursor.execute("select * from lastchat")
        lastrecords=""
        for (time, name, message) in mycursor:
            record=f"{time} {name} {message}"
            lastrecords=lastrecords+record+"\n"

            records_server.add_row([time,name,message])

        lastrecords=lastrecords.encode()
        conn.send(lastrecords)
        
        client_name=conn.recv(1024)
        client_name=client_name.decode()

        server_name_encoded=server_name.encode()
        conn.send(server_name_encoded)

        print("""
        Hi! Welcome to easyChat! Please note that this is somewhat limited — once you send a message, you must wait for a response from the other end before sending another message. Please avoid using apostrophes. If you (the server only) want to search for an older message, please type 'dbsearch <keyword you want to search>'. \n
        """)


        print("Last chat session:")
        print(records_server)



        mycursor.execute("delete from lastchat")
        mydb.commit()
        mycursor.execute("insert into lastchat values('NULL','NULL','NULL')")
        mydb.commit()



        








        while 1:
            message=input(str(f"{server_name} (You, server)>>"))

            if "'" or '"' in message:
                message.replace("'","")
                message.replace('"','')


            
            while "dbsearch" in message:
                mycursor.execute(f"select * from chatrecord where message like '%{message[9:]}%'")
                records_search=prettytable.PrettyTable(["Time","User","Message"])
                for (time, name, message) in mycursor:
                    records_search.add_row([time,name,message])
                print(records_search)
                message=input(str(f"{server_name} (You, server)>>"))
            
            if message=="chatexit":
                exit()


            current_time = datetime.datetime.now().strftime("%d/%m/%Y--%H:%M:%S")
            print(current_time)
            mycursor.execute(f"insert into chatrecord values ('{current_time}','{server_name}(Server)','{message}')")
            mydb.commit()
            mycursor.execute(f"insert into lastchat values ('{current_time}','{server_name}(Server)','{message}')")
            mydb.commit()
            #need to convert into bytes, as interface of socket only supports bytes
            message=message.encode()
            conn.send(message)
            print("")
            incoming_message=conn.recv(1024)
            incoming_message=incoming_message.decode()
            print(f"{client_name} (Client): ",incoming_message)
            if "'" or '"' in incoming_message:
                incoming_message.replace("'","")
                incoming_message.replace('"','')
            current_time = datetime.datetime.now().strftime("%d/%m/%Y--%H:%M:%S")
            mycursor.execute(f"insert into chatrecord values ('{current_time}','{client_name}(Client)','{incoming_message}')")
            print(current_time)
            print("")
            mydb.commit()
            mycursor.execute(f"insert into lastchat values ('{current_time}','{client_name}(Client)','{incoming_message}')")
            mydb.commit()




        mycursor.close()
        mydb.close()



    elif event == 'Join (as Client)':
        window.close(); del window
        layout = [[sg.Image(data=logo,size=(400,400))],[sg.Text('Enter your name, client.',justification='center',size=(50,1))],      
                        [sg.InputText("Client",size=(57,1), key="-clientname-")],
                        [sg.Text("Host ",justification='center'), sg.InputText(key="-host-", size=(50,1))],
                        [sg.Text("Port ",justification='center'), sg.InputText("2903",key="-port-",size=(51,1))],     
                        [sg.Submit(size=(50,1))]]    
        sg.theme('Light Purple')
        window = sg.Window('easyChat', layout)    

        event, values = window.read()
        if event == sg.WIN_CLOSED:
            exit()
        window.close(); del window

        client_name = values["-clientname-"] or "Client"
        client_name_encoded=client_name.encode()
        host=values["-host-"] or "192.168.1.5"
        port=int(values["-port-"] or 2903)


        s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        '''host=str(input("Server hostname: "))
        port=int(input("Enter port: "))'''
        host22=socket.gethostname() #gets local host name of your device
        ipaddr=socket.gethostbyname(host22)
        print(ipaddr)
        '''host=input("Host: ") or "192.168.1.5"
        port=int(input("Port: ") or 2903)'''
        print(f"Attempting to connect to Host: {host} and Port: {port}...")
        s.connect((host,port))
        print("Connected to chat server.")
        print("")

        records_client=prettytable.PrettyTable(["Time","User","Message"])

        incoming_records=s.recv(1024)
        incoming_records=incoming_records.decode()
        incoming_records=incoming_records.split("\n")
        incoming_records.pop()
        for i in incoming_records:
            i=i.split()
            m=""
            for j in i[2:]:
                m=m+j+" "
            m=m.rstrip()
            records_client.add_row([i[0],i[1],m])


        s.send(client_name_encoded)

        server_name=s.recv(1024)
        server_name=server_name.decode()

        print("""
        Hi! Welcome to easyChat! Please note that this is somewhat limited — once you send a message, you must wait for a response from the other end before sending another message. Please avoid using apostrophes.\n
        """)

        print("Last chat session:")
        print(records_client)

        while 1:

            incoming_message=s.recv(1024)
            incoming_message=incoming_message.decode()
            print(f"{server_name} (Server): ",incoming_message)
            print("")
            message=input(str(f"{client_name} (you)>>"))
            if "'" or '"' in message:
                message.replace("'","")
                message.replace('"','')
            if message=="chatexit":
                exit()
            message=message.encode()
            s.send(message)
            print("")






        continue
window.close();del window




