# rChat
v 1.0

Real time chat server built on python,

This is a interactive version of rChat.

* After starting rChat server client can connect using either telnet or nc,
```
	eg. {nc SERV_IP 8080} or {telnet SERV_IP 8080}
```

Afer successful connection client will be greeted with a rChat banner. And will be asked for username,
Username should be more than 3 character and alphanumberic.

* Client can chat to other client using following command.
```
	:USERNAME MSG TO SEND
```
[COLON followed by your friends username]
This will allow you to chat to many using single window.

* Also one can set a default username, to send message directly without providing :USERNAME
```
	:default USERNAME
	MSG TO SEND
```

Message you will type without providing username at starting, will be routed to default username.

* At any time you can leave chat or quit,
```
	:quit
```
