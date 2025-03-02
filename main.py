import socket
import pygame
from grid import Grid
import threading

# Initialize Pygame
pygame.init()

# Set up the Pygame display
intface = pygame.display.set_mode((600, 600))
pygame.display.set_caption("player1")
intface.fill((135, 206, 235))
# Create a Grid instance
grid = Grid()
grid.draw(intface)

# Initialize variables
running = True
count1 = 0
count2 = 0
count3 = 0
count4 = 0
count5 = 0
count=count1+count2
player1 = []
player=1

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
            if data=='ok':
                print('start')
            else:
                data1 = data.split(',')
                inp = (int(data1[0]), int(data1[1]))
                player = 1
                if inp in player1 :
                    img = pygame.image.load('E:/vkj/multigame/blast.png')
                    imgrect = img.get_rect()
                    imgrect.topleft = inp

                    print(data1)

                    intface.blit(img, imgrect)
                    cellX, cellY = inp[0], inp[1]
                    send_data1 = '{},{}'.format(cellX, cellY).encode()
                    conn.send(send_data1)
                    player1.remove(inp)
                if int(data1[0])>=0 and int(data1[1])>=300:
                    img = pygame.image.load('E:/vkj/multigame/blast.png')
                    imgrect = img.get_rect()
                    imgrect.topleft = inp
                    player=2

                    print(data1)

                    intface.blit(img, imgrect)




        except ConnectionResetError:
            print("Connection closed by the client")
            break


# Function to wait for connections
def wait_connect():
    global connection, conn, addr
    conn, addr = sock.accept()
    print('Client connected:', addr)
    connection = True
    create_thread(received_data)


# Create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(1)

# Start waiting for connections in a separate thread
create_thread(wait_connect)
def add(x,count):
    global connection
    if connection:
        img = pygame.image.load('E:/vkj/multigame/{}.png'.format(x))
        position = (pygame.mouse.get_pos()[0] // 60 * 60, pygame.mouse.get_pos()[1] // 60 * 60)
        if (pygame.mouse.get_pos()[0] // 60 * 60) < 600 and (pygame.mouse.get_pos()[1] // 60 * 60) < 300 :
            if not player1:
                intface.blit(img, position)
                print(position)
                player1.append(position)
            else:
                if position in player1:
                    pass
                else:
                    intface.blit(img, position)
                    player1.append(position)
                print(player1)
    else:
        print("Not connected to any client yet")
# Main loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and count1 < 3:
            add(x='tank',count=count1)
            count1+=1
        elif event.type == pygame.MOUSEBUTTONDOWN and count2 < 3:
            add(x='infantry',count=count2)
            count2+=1
        elif event.type == pygame.MOUSEBUTTONDOWN and count3 < 3:
            add(x='army-helicopter',count=count3)
            count3+=1
        elif count3==3 and event.type == pygame.MOUSEBUTTONDOWN and player==1:
            position = (pygame.mouse.get_pos()[0] // 60 * 60, pygame.mouse.get_pos()[1] // 60 * 60)
            print(position)
            if (pygame.mouse.get_pos()[0] // 60 * 60) >= 0 and (pygame.mouse.get_pos()[1] // 60 * 60) >= 300:
                print('inn')
                cellX, cellY = position[0], position[1]
                player=2
                send_data = '{},{}'.format(cellX, cellY).encode()

                try:
                    conn.send(send_data)
                except ConnectionResetError:
                    print("Connection closed by the client")
                    connection = False


    pygame.display.update()

# Clean up
pygame.quit()
