import socket
import time
import datetime
import prettytable
import PySimpleGUI as sg
import threading
import queue
import base64files
import sql_init
#end of imports
logo=base64files.static_logo

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
                        [sg.Text('Enter your name, Server',justification='center',size=(50,1))],      
                        [sg.InputText("Dorian",size=(57,1), key="-name-")],
                        [sg.Text('...',justification='center',size=(50,1))],
                        [sg.Text('Enter your sql credentials',justification='center',size=(50,1))],
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
        global server_pwd
        server_pwd=str(values["-pwd-"])

        #going to connect to the mysql db and create a cursor object
        sql_init.initialise_db(server_pwd)
        mycursor=sql_init.con.cursor()

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
                        [sg.Text("Waiting for incoming connections",size=(50,1))],
                        [sg.Image(r"assets/purpleload.gif",key="-GIF-",background_color="black")], #I haven't used  a base64 string for this since gif base64s are just way too long.
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
            window['-GIF-'].update_animation(r"assets/purpleload.gif",  time_between_frames=100)
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

        print(base64files.server_welcome) #welcome message
        print("Last chat session:")
        print(records_server)

        mycursor.execute("delete from lastchat")
        sql_init.con.commit()
        mycursor.execute("insert into lastchat values('NULL','NULL','NULL')")
        sql_init.con.commit()

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
            sql_init.con.commit()
            mycursor.execute(f"insert into lastchat values ('{current_time}','{server_name}(Server)','{message}')")
            sql_init.con.commit()

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
            sql_init.con.commit()
            mycursor.execute(f"insert into lastchat values ('{current_time}','{client_name}(Client)','{incoming_message}')")
            sql_init.con.commit()

        mycursor.close()
        sql_init.con.close()
        break

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

        print(base64files.client_welcome) #welcome message

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
        break




