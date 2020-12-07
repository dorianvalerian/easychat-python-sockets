import socket
import datetime
import prettytable
from easychat_package import base64files #used for the png images and any long-ish pieces of plaintext
from easychat_package import gui_layouts #used to create gui windows where required
#end of imports

def client():
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
        current_time = datetime.datetime.now().strftime("%d/%m/%Y--%H:%M:%S")
        print(current_time)
        print("")
        message=input(str(f"{client_name} (you)>>"))
        if "'" or '"' in message:
            message.replace("'","")
            message.replace('"','')
        if message=="chatexit":
            exit()
        message=message.encode()
        current_time = datetime.datetime.now().strftime("%d/%m/%Y--%H:%M:%S")
        print(current_time)
        s.send(message)
        print("")