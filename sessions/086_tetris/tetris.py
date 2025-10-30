from pyboy import PyBoy, WindowEvent
import random
import numpy as np


pyboy = PyBoy('Tetris.gb', debug=False, game_wrapper=True)

pyboy.set_emulation_speed(0)

print(pyboy.cartridge_title())

tetris = pyboy.game_wrapper()
frame = 0
old_total = 0
tetromino = 0
key = 0
y_max = 12
n_press = 1
old_array = np.zeros(tetris.shape).T
tetris.start_game(timer_div=0x00)

while not pyboy.tick(): #range(10000):
    frame += 1 
    rand = random.randint(0,1)
    for i in range(n_press):
        if key == -1:
            pyboy.send_input(WindowEvent.PRESS_ARROW_LEFT)
            pyboy.tick()
            pyboy.send_input(WindowEvent.RELEASE_ARROW_LEFT)
        elif key == 1:
            pyboy.send_input(WindowEvent.PRESS_ARROW_RIGHT)
            pyboy.tick()
            pyboy.send_input(WindowEvent.RELEASE_ARROW_RIGHT)
        elif key == 2:
            pyboy.send_input(WindowEvent.PRESS_BUTTON_A)
            pyboy.tick()
            pyboy.send_input(WindowEvent.RELEASE_BUTTON_A)
        else:
            pyboy.tick()
    new_array = np.array(tetris.game_area()) - 47
    if np.any(new_array != old_array):
        old_array = new_array
        print("frame: ", frame)
        #if np.sum(new_array[:6,:]) == 0:
        #    tetris.set_tetromino("I")
        s1 = np.sum(new_array[-y_max:,:], axis=0)
        pos_new = np.sum(new_array[:4,:], axis=0).argmax()
        target_min = s1.argmin()
        target_pos = pos_new - target_min
        print(pos_new, target_min, target_pos)
        if pos_new > 0 and target_pos > 0:
            n_press = np.abs(target_pos)
            key = -1
        elif pos_new > 0 and target_pos < 0:
            n_press = np.abs(target_pos)
            key = 1
        else:
            key = 2
        s2 = np.sum(new_array, axis=1)
        total = np.sum(new_array)
        print("Position new: ",pos_new)
        
        

    #print(np.max(s1), np.max(s2))
    #print(tetris.next_tetromino())
    #tetris.set_tetromino("I")
    #pyboy.send_input(WindowEvent.RELEASE_ARROW_DOWN)
pyboy.stop()