import socket
from cryptography.fernet import Fernet, MultiFernet
import os
import time
import datetime
from firebase import firebase

def main():
    """Defining main program """
    
    firebase= firebase_cloud_config() # Get firebase configuration
    sock = udp_config()               #Get udp configuration

    # Take user input to start the main program
    start_input=str(input("Welcome. Press Y when you are ready to start: ")) 

    while not start_input.lower() == "y":
        start_input=str(input("Welcome. Press Y when you are ready to start: "))
        
    if start_input.lower()=="y":
        sensor_1,sensor_2,sensor_3,sensor_4,key_log,path = create_data_logs() #Create 5 text files to store 4 sensors data and encryption key value with path details

    #Connect with the sensors and start recording the data
    print("Please turn on the sensors and follow the instruction","\n")
    connect_record_sensors(sock,sensor_1,sensor_2,sensor_3,sensor_4,key_log,firebase,path)

def firebase_cloud_config():
    """Return Firebase configuration """
    return firebase.FirebaseApplication('https://raahat-demo-project.firebaseio.com/', None)   

def udp_config():
    """Configure UDP server and return web-socket """
    UDP_IP = "192.168.137.1"
    UDP_PORT = 33333
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    sock.bind((UDP_IP, UDP_PORT))
    return sock

def create_data_logs():
    """Create Sensor data and encryption log files """
    
    path = "C:/Users/H. Rashid Raahat/Desktop/New folder (14)/ENcryption/Sensor_Data/"+str(time.time())
    file_name_input = str(input("Name the file : "))
    path = path+"("+file_name_input+")"
    os.mkdir(path)
    print ("Successfully created the directory %s" % path,"\n")
    
    sensor_1_log = open(path+"/PPG-1.txt", "a") 
    sensor_2_log = open(path+"/PPG-2.txt", "a")
    sensor_3_log = open(path+"/Temp.txt", "a")
    sensor_4_log = open(path+"/Acc.txt", "a")
    store_key = open(path+"/key.txt", "a")
    print ("Successfully created the log files","\n")
    
    return sensor_1_log,sensor_2_log,sensor_3_log,sensor_4_log,store_key,path
    
def connect_record_sensors(sock,sensor_1,sensor_2,sensor_3,sensor_4,key_log,firebase,path):
    encryption_key= get_encryption_key (key_log,path)
    availalbe_sensor_identity_list = list()
    
    try:
        while True:
            availalbe_sensor_identity_list.clear()
            
            for a in range (500):
                data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
                new = data.decode('utf-8').split(',')
                availalbe_sensor_identity_list.append(new[0])
          
            if len(availalbe_sensor_identity_list) == 0:
                Print("No sensor is connected. Turn on the sensor to connect"+"\n")
                
            if "PPG-1" in availalbe_sensor_identity_list[400:]:
                print("PPG-1 is connected")
                
            if "PPG-2" in availalbe_sensor_identity_list[400:]:
                print("PPG-2 is connected")
                
            if "Temp" in availalbe_sensor_identity_list[400:]:
                print("Temparature is connected")
                
            if "Acc" in availalbe_sensor_identity_list[400:]:
                print("Accelarometer is connected")

            user_input = int(input("Press 1 to start, 2 for scan, 3 to save the files and exit"))

            if user_input == 1:
                user_input_1(sock,encryption_key,firebase)

            elif user_input == 2:
                user_input_2()

            elif user_input == 3:
                user_input_3()

            else:
                print("Wrong selection. Process will start again.")

    except KeyboardInterrupt:
        store_exit(sensor_1,sensor_2,sensor_3,sensor_4)

def get_encryption_key (key_log,path):
    """Generate encryption key for encode and decode, store the key in a text file and return the key.  """
    key = Fernet.generate_key()
    string_key = key.decode('utf-8')
    key_log = open(path+"/key.txt", "a")
    key_log.write(string_key )
    key_log.close()
    
    f = Fernet(key)
    return f
    
def user_input_1(sock,encryption_key,firebase):
    """ Working flow for user selection 1"""
    data_dict = dict()
    timestamp_list = list()
    data_list= list()

    while True:
        try:
            for elements in range (100):
                data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
                lines = data.decode('utf-8').split(',')
                if lines[0] =="PPG-1":
                    data = (str(lines[2].rstrip())).encode('utf-8')
                    encrypted_data = encryption_key.encrypt(data)
                    time_stamp.append(str(datetime.datetime.now()))
                    data_list.append(encrypted_data.decode('utf-8'))
                    data_dict["Timestamp"] =time_stamp
                    data_dict["PPG-1"]=data_list
                    firebase.post("wireless_data_collection/", data_dict)
                    
                if lines[0] =="PPG-2":
                    data = (str(lines[2].rstrip())).encode('utf-8')
                    encrypted_data = encryption_key.encrypt(data)
                    time_stamp.append(str(datetime.datetime.now()))
                    data_list.append(encrypted_data.decode('utf-8'))
                    data_dict["Timestamp"] =time_stamp
                    data_dict["PPG-2"]=data_list
                    firebase.post("wireless_data_collection/", data_dict)
                    
                if lines[0] =="Temp":
                    data = (str(lines[2].rstrip())).encode('utf-8')
                    encrypted_data = encryption_key.encrypt(data)
                    time_stamp.append(str(datetime.datetime.now()))
                    data_list.append(encrypted_data.decode('utf-8'))
                    data_dict["Timestamp"] =time_stamp
                    data_dict["Temp"]=data_list
                    firebase.post("wireless_data_collection/", data_dict)

                if lines[0] =="Acc":
                    data = (str(lines[2].rstrip())).encode('utf-8')
                    encrypted_data = encryption_key.encrypt(data)
                    time_stamp.append(str(datetime.datetime.now()))
                    data_list.append(encrypted_data.decode('utf-8'))
                    data_dict["Timestamp"] =time_stamp
                    data_dict["PPG-1"]=data_list
                    firebase.post("wireless_data_collection/", data_dict)        
                
                print(data_dict)
                data_dict.clear()
                timestamp_list.clear()
                data_list.clear()

        except KeyboardInterrupt:
            store_exit(sensor_1,sensor_2,sensor_3,sensor_4)

def user_input_2():
     """ Working flow for user selection 2 """
     
    print("Searching Again")

def user_input_3(sensor_1,sensor_2,sensor_3,sensor_4):
     """ Working flow for user selection 2 """

     store_exit(sensor_1,sensor_2,sensor_3,sensor_4)

def store_exit(sensor_1,sensor_2,sensor_3,sensor_4):
    """ Store the sensor data and excute system exit."""
    
     sensor_1.close()
     sensor_2.close()
     sensor_3.close()
     sensor_4.close()
     print("All files are saved and closed successfully.")
     raise SystemExit

main()

