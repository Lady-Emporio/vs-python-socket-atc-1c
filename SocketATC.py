
import json
import socket
import requests
import time

sock = socket.socket()
sock.settimeout(1.0)


def talk(text):
	b_text=str.encode(text)
	sock.send(b_text)
	print("send: "+str(b_text))
	print("begin----------------------------")
	while(True):
		try:
			data = sock.recv(1024)
			str_data=data.decode("utf-8") 
			print(str_data)
			if(len(str_data)==0):
				break;
		except socket.timeout:
			#continue
			#print ('caught a timeout')
			break;
	print("end	---------------------------\n\n")

def SendAndGet(text):
	b_text=str.encode(text)
	sock.send(b_text)
	returnAnswer=""
	while(True):
		try:
			data = sock.recv(4096)
			returnAnswer+=data.decode("utf-8") 
			if(len(returnAnswer)==0):
				break;
		except socket.timeout:
			#continue
			#print ('caught a timeout')
			break;
	return returnAnswer;

def login():
	str_login="Action: login\r\nUsername: teleami1\r\nSecret: teleami1\r\nEvents: off\r\n\r\n"
	#str_login="Action: login\r\nUsername: teleami1\r\nSecret: teleami\r\n\r\n"
	talk(str_login)

def everySecSendStatusChannels():
	time.sleep(1)

	TextMessages=SendAndGet("Action: ExtensionStateList\r\n\r\n")
	ArrayMessages=TextMessages.split("\r\n\r\n");

	JsonMessages=[]
	#'Event: ExtensionStatus\r\nExten: 101\r\nContext: ext-local\r\nHint: PJSIP/101\r\nStatus: 4\r\nStatusText: Unavailable'
	for Textmessage in ArrayMessages:
		attts=Textmessage.split("\r\n")
		#['Event: ExtensionStatus',
		# 'Exten: 101',
		# 'Context: ext-local', 
		# 'Hint: PJSIP/101',
		# 'Status: 4', 
		# 'StatusText: Unavailable']
		if(len(attts)!=6):
			continue
		if(attts[0]!="Event: ExtensionStatus"):
			continue
		left_ValueIndex=0; right_ValueIndex=1;
		Index_Exten=1; Index_Hint=3; Index_Status=4; Index_StatusText=5;
		Exten_Value=attts[Index_Exten].split(":")[right_ValueIndex].strip()
		Hint_Value=attts[Index_Hint].split(":")[right_ValueIndex].strip()
		Status_Value=attts[Index_Status].split(":")[right_ValueIndex].strip()
		StatusText_Value=attts[Index_StatusText].split(":")[right_ValueIndex].strip()

		JsonMessages.append({
			"Exten"		: Exten_Value,#код
			"Hint"		: Hint_Value, #наименование
			"Status"	: Status_Value,#код	
			"StatusText": StatusText_Value,	#наименование
		})


	textJson=json.dumps(JsonMessages)
	r=requests.post("http://localhost:8080/test/hs/channels/set",data = textJson)
	print(r.content.decode("utf-8"))



sock.connect(("192.168.1.2", 7777))
login()



while(1):
	everySecSendStatusChannels();

end=None;