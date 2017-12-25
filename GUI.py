#2048 - графический интерфейс
# Рязанов Максим

from tkinter import*
from game import Game
from tkinter import messagebox as mb

CELL_SIZE = 50
colors = {'0':'gold',
        '2':'gray',
        '4':'#AAFFAA',
        '8':'orange',
        '16':'red',
        '32':'cyan',
        '64':'pink',
        '128':'purple',
        '256':'green',
        '512':'#0035FA',
        '1024':'#6615B0',
        '2048':'#white'}
max_value = 2048

def init_board(can, width):
    cells = [[], []]
    for i in range(width):
        for j in range(width):
            cells[0].append(can.create_rectangle(j*CELL_SIZE+3,
                                              (i+1)*CELL_SIZE-3,
                                              (j+1)*CELL_SIZE-3,
                                              i*CELL_SIZE+3,
                                              fill='gold'))
            cells[1].append(can.create_text((j+0.5)*CELL_SIZE,
                                            (i+0.5)*CELL_SIZE,
                                            text='',
                                            font='Droid 14'))
    return cells

def update(mat,width,cells):
    for i in range(width):
        for j in range(width):
            if mat[i][j]:
                can.itemconfig(cells[1][i*width+j],text=str(mat[i][j]))
            else:
                can.itemconfig(cells[1][i*width+j], text= '')
            tmp = mat[i][j] if mat[i][j]<max_value else max_value
            can.itemconfig(cells[0][i*width+j],fill=colors[str(tmp)])


def warn(text):
    mb.showinfo(' ',text)


def turn (game, direct):
    if game.make_turn(direct):
        update(game.mat, game.width, cells)
    if not game.avail_turns:
        warn('Вы проирали')


width = int(input('Размер'))
root = Tk()
root.title('2048')
can = Canvas(root,width=CELL_SIZE*width,height=CELL_SIZE*width,
             bg='silver')
can.pack()
cells = init_board(can,width)
game = Game(width, 0, 0.9)
root.bind('<Up>',lambda x: turn(game,'w'))
root.bind('<Down>', lambda x: turn(game,'s'))
root.bind('<Left>',lambda x: turn(game,'a'))
root.bind('<Right>',lambda x: turn(game,'d'))

root.mainloop()
