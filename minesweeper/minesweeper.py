import tkinter
import tkinter.messagebox
import random
import sys
import os

# development moved to repository grid-games

class App(tkinter.Tk):
    def __init__(self):
        super().__init__()

        self.title("minesweeper")
        self.resizable(0, 0)

        self.running = True
        self.populated = False
        self.clicks = 0
        self.flags_left = 40
        self.image_list = []
        self.button_list = []
        self.offsets = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]

        self.img_bomb = tkinter.PhotoImage(width=25, height=25, file=self.asset("boom.png"))
        self.img_unk = tkinter.PhotoImage(width=25, height=25, file=self.asset("question.png"))
        self.img_flag = tkinter.PhotoImage(width=25, height=25, file=self.asset("flag.png"))

        self.flag_mode = tkinter.BooleanVar(self, False)

        info_frame = tkinter.Frame(self)

        self.flag_counter = tkinter.Label(info_frame, text="40 flags left")
        self.clicks_counter = tkinter.Label(info_frame, text="0 clicks")
        flag_checkbox = tkinter.Checkbutton(info_frame, text="Flag mode", variable=self.flag_mode, onvalue=True, offvalue=False)
        
        flag_checkbox.pack(side="right", padx=10)
        self.flag_counter.pack(side="right", padx=10)
        self.clicks_counter.pack(side="right", padx=10)

        info_frame.pack()

        self.grid = []
        for r in range(16):

            row = []
            gui_row = tkinter.Frame(self)

            for c in range(16):
                button = tkinter.Button(gui_row, text="", image=self.img_unk, width=30, height=30)
                
                button.row = r
                button.col = c
                button.bomb = False
                button.revealed = False
                button.flagged = False
                button.safe = False

                button.config(command=(lambda button=button : self.click(button)))
                button.pack(side="left")

                self.button_list.append(button)
                row.append(button)

            gui_row.pack(side="bottom")
            self.grid.append(row)

    def asset(self, relative_path):
        try:                                            
            base_path = sys._MEIPASS                    
        except Exception:                               
            base_path = os.path.abspath(".")

        return os.path.join(base_path, "assets", relative_path)        

    def click(self, button):
        if self.running and not button.revealed:
            self.clicks += 1
            self.clicks_counter.config(text=f"{self.clicks} clicks")

            if self.flag_mode.get():
                if button.flagged:
                    button.flagged = False
                    button.config(image=self.img_unk)
                    self.flags_left += 1
                
                else:
                    button.flagged = True
                    button.config(image=self.img_flag)
                    self.flags_left -= 1
                
                self.flag_counter.config(text=f"{self.flags_left} flags left")

            else:
                button.revealed = True

                if button.bomb:
                    for button2 in self.button_list:
                        if button2.bomb:
                            button2.config(image=self.img_bomb)
                    
                    self.update()

                    self.running = False
                    tkinter.messagebox.showerror(title="fail", message="you lose :(")
                    self.destroy()

                else:
                    value = 0

                    for offset in self.offsets:
                        try:
                            if self.grid[button.row + offset[0]][button.col + offset[1]].bomb:
                                value += 1
                        except:
                            pass

                    img_value = tkinter.PhotoImage(width=25, height=25, file=self.asset(f"digit{value}.png"))
                    self.image_list.append(img_value)
                    button.config(image=img_value)

                    #spread(button, value)

                    total = 0
                    for button2 in self.button_list:
                        if button2.revealed or button2.bomb:
                            total += 1
                    
                    if total == 256:
                        running = False
                        tkinter.messagebox.showinfo(title="yay", message="you won :)")
                        self.destroy()

        if not self.populated:
            for offset in self.offsets:
                try:
                    self.grid[button.row + offset[0]][button.col + offset[1]].safe = True
                except:
                    pass

            count = 40
            while count > 0:
                row, col = random.randint(0, 15), random.randint(0, 15)
                tile = self.grid[row][col]
                if not tile.bomb and not tile.revealed and not tile.safe:
                    tile.bomb = True
                    count -= 1

            self.populated = True

if __name__ == "__main__":
    app = App()
    app.mainloop()