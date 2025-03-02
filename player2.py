import socket
import pygame
import threading

from grid import Grid

# Initialize Pygame
pygame.init()

# Set up the Pygame display
intface = pygame.display.set_mode((600, 600))
pygame.display.set_caption("player2")
intface.fill((135, 206, 235))
grid = Grid()
grid.draw(intface)
count1 = 0
count2 = 0
count3 = 0
count4 = 0
count5 = 0
player2 = []
player=2

# Function to create a thread
def create_thread(target):
    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()

# Server configuration
HOST = '127.0.0.1'
PORT = 5050
connection = False
conn, addr = None, None

# Function to handle received data
def received_data():
    global conn,player
    while True:
        try:
            data = conn.recv(1024).decode()
            print("Received:", data)
            data1 = data.split(',')
            inp =(int(data1[0]),int(data1[1]))
            player=2
            if inp in player2:
                img = pygame.image.load('E:/vkj/multigame/blast.png')
                imgrect=img.get_rect()
                imgrect.topleft=inp


                print(data1)

                intface.blit(img, imgrect)
                cellX, cellY = inp[0], inp[1]
                send_data1 = '{},{}'.format(cellX, cellY).encode()
                conn.send(send_data1)
                player2.remove(inp)
            if int(data1[0]) <600 and int(data1[1]) < 300:
                img = pygame.image.load('E:/vkj/multigame/blast.png')
                imgrect = img.get_rect()
                imgrect.topleft = inp
                player=1

                print(data1)

                intface.blit(img, imgrect)
        except ConnectionResetError:
            print("Connection closed by the server")
            break
    pygame.display.update()
# Function to connect to the server
def connect_server():
    global connection, conn, addr
    try:
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((HOST, PORT))
        print("Connected to server")
        connection = True
        create_thread(received_data)
    except ConnectionRefusedError:
        print("Connection refused by the server")

# Connect to the server
connect_server()
def add(x,count):
    global connection
    if connection:
        img = pygame.image.load('E:/vkj/multigame/{}.png'.format(x))
        position = (pygame.mouse.get_pos()[0] // 60 * 60, pygame.mouse.get_pos()[1] // 60 * 60)
        if (pygame.mouse.get_pos()[0] // 60 * 60) >=0 and (pygame.mouse.get_pos()[1] // 60 * 60) >= 300 :
            if not player2:
                intface.blit(img, position)
                print(position)
                player2.append(position)
            else:
                if position in player2:
                    pass
                else:
                    intface.blit(img, position)
                    player2.append(position)
                print(player2)
    else:
        print("Not connected to any client yet")
# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and count1 < 3:
            add(x='tank', count=count1)
            count1 += 1
        elif event.type == pygame.MOUSEBUTTONDOWN and count2 < 3:
            add(x='infantry',count=count2)
            count2+=1
        elif event.type == pygame.MOUSEBUTTONDOWN and count3 < 3:
            add(x='army-helicopter',count=count3)
            count3+=1
        elif count2 == 3 and event.type == pygame.MOUSEBUTTONDOWN and player==2:
            position = (pygame.mouse.get_pos()[0] // 60 * 60, pygame.mouse.get_pos()[1] // 60 * 60)
            print(position)
            if (pygame.mouse.get_pos()[0] // 60 * 60) <600 and (pygame.mouse.get_pos()[1] // 60 * 60) < 300:
                print('inn')
                cellX, cellY = position[0], position[1]
                send_data = '{},{}'.format(cellX, cellY).encode()
                player=1
                try:
                    conn.send(send_data)
                    conn.send('ok'.encode())
                except ConnectionResetError:
                    print("Connection closed by the client")
                    connection = False

    pygame.display.update()

# Clean up
pygame.quit()
