import PySimpleGUI as sg
from easychat_package import gui_layouts #used to create gui windows where required
from easychat_package import client
from easychat_package import server
#end of imports

gui_layouts.choice() #the host/join choice window
event=gui_layouts.event
window=gui_layouts.window
if event == sg.WIN_CLOSED:     # If user closed window with X 
    exit()

elif event == 'Host (as Server)':
    window.close(); del window
    server.server() #from server.pu

elif event == 'Join (as Client)':
    window.close(); del window
    client.client() #from client.py