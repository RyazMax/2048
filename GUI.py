#2048 - графический интерфейс
# Рязанов Максим

from tkinter import*
from game import Game
from tkinter import messagebox as mb

CELL_SIZE = 70
colors = {'0':'#CDC1B5',
          '':'#CDC1B5',
        '2':'#EDE3DA',
        '4':'#ECE0CA',
        '8':'#F2B177',
        '16':'#F59565',
        '32':'#F57C5F',
        '64':'#F65D3B',
        '128':'#EDCE71',
        '256':'#EDCC63',
        '512':'#F0C656',
        '1024':'#F5C340',
        '2048':'#FAC030'}
max_value = 2048


def init_board(can, width):
    cells = [[], []]
    for i in range(width):
        for j in range(width):
            cells[0].append(can.create_rectangle(j*CELL_SIZE+5,
                                              (i+1)*CELL_SIZE-5,
                                              (j+1)*CELL_SIZE-5,
                                              i*CELL_SIZE+5,
                                              fill=colors['0'],
                            outline=colors['0']))
            cells[1].append(can.create_text((j+0.5)*CELL_SIZE,
                                            (i+0.5)*CELL_SIZE,
                                            text='',
                                            font='Droid 14'))
    return cells

def init_can(width):
    global can, cells, game
    can = Canvas(root, width=CELL_SIZE * width, height=CELL_SIZE * width,
                 bg='#BAAEA0')
    can.pack()
    cells = init_board(can, width)
    game = Game(width, 0, 0.9)
    return can, cells, game

def update(mat,width,cells):
    for i in range(width):
        for j in range(width):
            if mat[i][j]>4: col = 'white'
            else: col ='#767267'
            if mat[i][j]:
                can.itemconfig(cells[1][i*width+j],text=str(mat[i][j]),fill=col)
            else:
                can.itemconfig(cells[1][i*width+j], text= '')
            tmp = mat[i][j] if mat[i][j]<max_value else max_value
            can.itemconfig(cells[0][i*width+j],fill=colors[str(tmp)],
                           outline=colors[str(tmp)])


def warn(text):
    mb.showinfo(' ',text)

def highlight(ls,width,mode):
    for one in ls:
        i = one[0]
        j = one[1]
        col = colors[str(game.mat[i][j])]
        can.delete(cells[0][i*width+j])
        if mode:
            cells[0][i*width+j] = can.create_rectangle(j*CELL_SIZE+5,
                                                    (i+1)*CELL_SIZE-5,
                                              (j+1)*CELL_SIZE-5,
                                              i*CELL_SIZE+5,
                                              fill=col, outline=col)
        else:
            cells[0][i*width+j] = can.create_rectangle(j*CELL_SIZE,
                                              (i+1)*CELL_SIZE,
                                              (j+1)*CELL_SIZE,
                                              i*CELL_SIZE,
                                              fill=col, outline=col)
            root.after(100,lambda: highlight(ls,width,1))
        can.lift(cells[1][i*width+j])

def turn (game, direct):
    tmp = game.make_turn(direct)
    if tmp[0]:
        update(game.mat, game.width, cells)
        highlight(tmp[1],game.width,0)
    if not game.avail_turns:
        warn('Вы проиграли')
        return False
    return True

def spin (game, cnt):
    for i in range(cnt):
        for j in 'wasd':
            if not turn(game, j): return

def change(size,frame):
    global WIDTH
    if not size.isdigit():
        mb.show('Введите натуральное число')
    else:
        WIDTH = int(size)
        can.destroy()
        init_can(WIDTH)
        frame.destroy()

def size():
    size_choice = Toplevel()
    ent = Entry(size_choice)
    but = Button(size_choice, text='Изменить', command=lambda: change(ent.get(),size_choice))
    ent.grid(row=1, column=0)
    but.grid(row=1, column=1)
    lbl = Label(size_choice, text='Введите размер поля')
    lbl.grid(row=0, column=0, columnspan=2)

def newgame():
    can.destroy()
    init_can(WIDTH)

WIDTH = 4
root = Tk()
root.title('2048')
menu = Menu(root)
menu.add_command(label='Размеры', command=size)
menu.add_command(label='Новая игра', command=newgame)

root.config(menu=menu)

can = Canvas()
cells = [[],[]]
game = 0
init_can(WIDTH)
root.bind('<Up>',lambda x: turn(game,'w'))
root.bind('<Down>', lambda x: turn(game,'s'))
root.bind('<Left>',lambda x: turn(game,'a'))
root.bind('<Right>',lambda x: turn(game,'d'))
root.bind('5', lambda x: spin(game,30))

root.mainloop()
