# Tweet-App-CSEN-493-34

                            CSEN 493: Directed Research Publish Subscribe Systems - Tweet App

* Description

The Tweet App is a small scale version of Twitter implemented using a publisher/subscriber socket programming model with a terminal interface. 
This app provides some of Twitter's features such as accessing an account, tweeting, messaging followers, creating and interacting with groups, to name a few.

* Dependencies

The following modules are required to to be set up before running the project.

- pip3
- colorama
  
In the terminal, enter the following command: 
sudo apt install -y python3-pip
pip3 install colorama

* Instructions to run

- Open the terminal in the home directory of the project and then run server.py
   Command: python3 server.py
   
- Open a new terminal in the home directory of the project and run the client.py  
   Command: python3 client.py

* Implemented commands

Enter the following commands in client.py terminal.

login <username>
register <username>
logout
search <username>
follow <username>
unfollow <username>
profile <username>
tweet <your tweet text>
msg <username> <your message text>
posts
group create <groupname>
group add <groupname> <username>
group remove <groupname> <username>
group members <groupname>
group delete <groupname>
stream <groupname> <your message text>
