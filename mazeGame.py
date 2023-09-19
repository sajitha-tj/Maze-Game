import pygame
import sys
import maze as mz

# initialize pygame
pygame.init()
clock = pygame.time.Clock()

# get the maze and initialize it
mazeFile = sys.argv[1]
maze = mz.Maze(mazeFile)
maze.print()

# set up the screen
S_WIDTH = maze.width
S_HEIGHT = maze.height
BLOCK_SIZE = 10  # size of a block in pixels
screen = pygame.display.set_mode(
    (BLOCK_SIZE*S_WIDTH, BLOCK_SIZE*S_HEIGHT))
pygame.display.set_caption('Maze Game')
icon = pygame.image.load('mazeGameIcon.ico')
pygame.display.set_icon(icon)

# draw the maze
walls = maze.walls
# blocks = []
for i in range(maze.height):
    for j in range(maze.width):
        if walls[i][j]:
            block = pygame.Rect(
                (BLOCK_SIZE*j, BLOCK_SIZE*i, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(screen, "blue", block)


running = True

# set up the player, start and goal blocks
player = pygame.Rect(
    (BLOCK_SIZE*maze.start[1], BLOCK_SIZE*maze.start[0], BLOCK_SIZE, BLOCK_SIZE))
startBlock = pygame.Rect(
    (BLOCK_SIZE*maze.start[1], BLOCK_SIZE*maze.start[0], BLOCK_SIZE, BLOCK_SIZE))
goalBlock = pygame.Rect(
    (BLOCK_SIZE*maze.goal[1], BLOCK_SIZE*maze.goal[0], BLOCK_SIZE, BLOCK_SIZE))

pygame.display.update()

count = 0
maze.solve()  # solve the maze

# main loop
while running:
    pygame.draw.rect(screen, "green", player)  # draw the player
    pygame.draw.rect(screen, "purple", startBlock)  # draw the start block
    pygame.draw.rect(screen, "red", goalBlock)  # draw the goal block

    # key = pygame.key.get_pressed()

    # event listner for quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # move the player through the solution
    if count < len(maze.solution[1]):
        action = maze.solution[1][count]
        print(action)
        player.y = action[0]*BLOCK_SIZE
        player.x = action[1]*BLOCK_SIZE
        count += 1

    # update the screen
    pygame.display.update()

    # set the fps
    clock.tick(20)

pygame.quit()
