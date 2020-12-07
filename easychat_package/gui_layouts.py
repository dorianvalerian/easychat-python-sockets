import PySimpleGUI as sg
from easychat_package import base64files

#the first host/join screen
def choice():
    global logo
    logo=base64files.static_logo
    global window
    global event
    sg.theme("light purple")
    layout = [[sg.Image(data=logo)],
                [sg.Button('Host (as Server)'), sg.Button('Join (as Client)')]]
    window = sg.Window('easyChat', layout, grab_anywhere=True, icon=r"D:\Downloads\ec2.ico")
    event, values = window.read()   # Read the event that happened and the values dictionary.

#entering server name/creds
def server_gui():
    global logo
    logo=base64files.static_logo
    global server_name
    global server_pwd
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

#waiting for client to join
def conn_wait(host):
    global window
    layout=[[sg.Text(f"Server will start on host: {host}  and port: 2903",size=(50,1))],
                    [sg.Text("Binded all IPv4 to 2903.",size=(50,1))],
                    [sg.Text("Waiting for incoming connections",size=(50,1))],
                    [sg.Image(r"media/purpleload.gif",key="-GIF-",background_color="black")], #I haven't used  a base64 string for this since gif base64s are just way too long.
                    [sg.Button("Cancel")]]
    sg.theme('Light Purple')
    window = sg.Window('easyChat', layout)

def conn_popup(addr):
    sg.popup_no_buttons(addr, "has connected to the server, and is now online.", keep_on_top=True, no_titlebar=True,auto_close=True,auto_close_duration=2)

def client_gui():
    global logo
    logo=base64files.static_logo
    global client_name_encoded
    global client_name
    global host
    global port
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