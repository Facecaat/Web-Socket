import socket
import client_socket
import time
import sys

server_socket = socket.socket(socket.AF_INET, # задамем семейство протоколов 'Интернет' (INET)
                              socket.SOCK_STREAM, # задаем тип передачи данных 'потоковый' (TCP)
                              proto=0)       # выбираем протокол 'по умолчанию' для TCP, т.е. IP

'''
Так мы работаем с серверным сокетом, а в общем случае на серверной машине может быть 
несколько сетевых адаптеров, нам необходимо привязать созданный сокет к одному из них:
'''
try:
    server_socket.bind(("127.0.0.1", 53210))
except OSError as e:
    print(f"Error binding to port {e}")
    exit(1)
'''
Вызов bind() заставляет нас указать не только IP адрес, но и порт, на котором сервер будет 
ожидать (слушать) подключения клиентов.
Далее необходимо явно перевести сокет в состояние ожидания подключения, сообщив об 
этом операционной системе:
'''

backlog = 10 # размер очереди входящих подключений - backlog
server_socket.listen(backlog)

'''
Параметр backlog определяет размер очереди не обработанных 
программой соединений. Пока количество подключенных клиентов меньше, чем этот параметр, 
система будет принимать соединения сокет и помещать их в очередь. 
Как только количество установленных соединений в очереди достигнет 
значения backlog, новые соединения приниматься не будут. 
'''
def start_server(port=53210):
    while True:
        # Бесконечно обрабатываем входящие подключения
        client_socket, client_address = server_socket.accept()
        print("Connected by", client_address)

        while True:
            # Пока клиент не отключился, читаем передаваемые
            # им данные и отправляем их обратно
            data = client_socket.recv(1024)
            if not data:
                # Клиент отключился
                break
            client_socket.sendall(data)

        client_socket.close()

def running_programm():
    while True:
        user_input = input()
        if user_input in ["broadcast-server start", "start"]:
            start_server()
        elif user_input in ["broadcast-server connect", "connect"]:
            client_socket.connect_server()

#Проверка активности сервера в командной строке:
    #netstat - ano | findstr: 53210


