import socket
import time
import datetime
import prettytable
import PySimpleGUI as sg
import threading
import queue
from easychat_package import base64files
from easychat_package import gui_layouts
from easychat_package import sql_init
#end of imports
global logo
logo=base64files.static_logo

def conn_listen(gui_queue):
    s.listen(1)
    global conn, addr
    try:
        conn, addr=s.accept()
        gui_queue.put("ConnEstb")
    except:
        pass

gui_layouts.choice() #the host/join choice window
event=gui_layouts.event
window=gui_layouts.window
if event == sg.WIN_CLOSED:     # If user closed window with X 
    exit()

elif event == 'Host (as Server)':
    window.close(); del window

    gui_layouts.server_gui() #server name/creds
    server_name=gui_layouts.server_name
    global server_pwd
    server_pwd=gui_layouts.server_pwd

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

    gui_layouts.conn_wait(host) #the waiting window with the gif
    window=gui_layouts.window

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

    print(addr, "has connected to the server, and is now online.")
    current_time = datetime.datetime.now().strftime("%d/%m/%Y--%H:%M:%S")
    print(current_time)
    gui_layouts.conn_popup(addr) #alerting server

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

elif event == 'Join (as Client)':
    window.close(); del window
    gui_layouts.client_gui() #client name, server host & port to connect to
    client_name=gui_layouts.client_name
    client_name_encoded=gui_layouts.client_name_encoded
    host=gui_layouts.host
    port=gui_layouts.port

    s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"Your local IP: {socket.gethostbyname(socket.gethostname())}") #gets clients local host
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