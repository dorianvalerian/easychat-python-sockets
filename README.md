# easychat

![easychat](media/ecgit.png)

A simple chat program built using Python and Socket Programming. High School project :)
This repo is mainly for version control.

---------------------------------------------------------------------------------------
### NOTES
To run this 'as-is':
Prerequisites:
1) Python3
2) mySQL*
2) These modules:
  a) pysimplegui
  b) threading
  c) socket
  d) prettytable

You must download all the files and not just easychat.py, by clicking on the "Code" button above. Then, run easychat.py to use the application.

In case you want to use this as an .exe file, use pyinstaller. However you will need to add any media files you use in this to the data section of the spec file created by pyinstaller.

As of right now, the program is accompanied by a GUI only till before the actual chatting starts (the client/server, login and connection windows). Feel free to fork this repo and request a pull.

This was originally for a school project, and the report for the same follows.

* It's entirely possible to run this without using SQL — you'll have to remove all the cursor.execute() statements and the like. Note that you will not be able to access chat history.

* You can use this over public IP at your own discretion, by setting up port forwarding on your router (i.e setting it so that requests to a specific port on your router, that is, to your public IP, will get forwarded to the port specified here in server.py on your local machine, that is, your local IP). This is not guaranteed to work because of various aspects such as firewalls and router limitations.
----------------------------------------------------------------------------------------


# OVERVIEW
In today’s increasingly digital world, not a day goes by when we don’t use texting platforms on our smartphones and laptops to communicate with our friends, family members, colleagues and coworkers. So, for my Computer Science project for class XII, I decided to try my hand at building a basic chat software ourselves, using Python and MySQL. The result was an app that I call easyChat.

# Features:
Easily connect with any other device, provided both the devices are on the same IP (Internet Protocol) address.
Send and receive messages in real-time.
Conversations will be saved onto a database, and can be accessed by the server at any time. On starting a new session, the contents of the previous session will be loaded onto both devices so the users can easily pick up from where they left off.
Hands-free mode: Our speech-recognition software will enable you to use your voice to send text messages.

# PRELIMINARY CONCEPTS
Communication Protocols: a communication protocol refers to the set of rules that computers use to communicate with each other. The protocol defines the signals that the computers will give each other, and other details such as how communication begins and/or ends.

For the purposes of this project, we have used the Transmission Control Protocol (TCP), which as a member of Internet Protocol suite makes sure that the data being transmitted over the connection doesn’t get corrupted and gets to the final destination (looked after by the IP) in the right order.

NOTE: Another possible protocol we could have used is User Datagram Protocol (UDP). However, it sacrifices reliability for speed.

Now, every TCP connection has two endpoints known as TCP Sockets, and python provides us with a whole sockets module dedicated to their creation and modification. This is what we will be using for this project.

We have also made use of the thread module in order to run parallel program threads in this project, which allows for a more natural chatting experience. Without the use of this module, the project would behave as a ‘walkie-talkie’ rather than a chat app, and would be rather limited in its functionality.

# Concepts of SQL:
In order to interface Python with MySQL, which is required for our project’s chat history functionality we have used the mysql.connector module.

# SOCKET PROGRAMMING
.socket() creates a new socket and assigns it a name that can be used in the program later on.

.connect() connects the client to the host with the given host name( could also be a local ip address) at the given port.

.recv() listens to the socket for any new messages.

.decode() converts the binary file into text.

.gethostname() Gets the name of the local host which in our case is the system on which we are working.

.bind() the server socket is associated with the host and is assigned the given port.

.listen() the socket waits for a connection request.

.close() deletes the socket once its job is over.

.encode() Converts the text into binary data packets for transmission.

.send() The message is sent to the socket and from there it is transmitted to all the client sockets attached with it.

Other modules used:
datetime, for the timestamp on the messages
prettytable,  to make simple ASCII tables for chat history
PySimpleGUI, for the Graphical User Interface of the initial naming window.
