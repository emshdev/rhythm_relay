from tkinter import Canvas, Tk, ttk, IntVar, messagebox

from numpy import expand_dims, true_divide

class Window(Tk):
    def __init__(self):
        super().__init__()

        # Window Initialization
        self.title('리듬 끝말잇기')
        self.geometry('250x780')
        self.resizable(0, 0)

        # Form Initialization
        self.font_init()
        self.mode_init()
        ttk.Separator(self, orient='horizontal').pack(fill='x', padx=5, side='top')
        self.nextSong_init()
        ttk.Separator(self, orient='horizontal').pack(fill='x', padx=5, side='top')
        ttk.Label(self, text='절취선').pack(fill='y', pady=5)
        ttk.Separator(self, orient='horizontal').pack(fill='x', padx=5, side='top')
        self.rem_init()
        ttk.Separator(self, orient='horizontal').pack(fill='x', padx=5, side='top')
        self.currSong_init()
        ttk.Separator(self, orient='horizontal').pack(fill='x', padx=5, side='top')
        self.songlist_init()


        # Variables Initialization
        self.timerBool = False
        self.marqBool = False
        self.marqBool2 = False
        self.startBool = False
        self.songcount = 0
        self.songlist = '플레이한 목록\n'

    # List of fonts    
    def font_init(self):
        self.font1 = ('강원교육모두 Bold', 16)
        self.font2 = ('강원교육모두 Bold', 28)
        self.font3 = ('Kotra Leap', 32)
        self.font4 = ('Kotra Leap', 20)
        self.font5 = ('Kotra Leap', 40)
        self.font6 = ('Kotra Leap', 24)
        self.font7 = ('Kotra Leap', 16)

    # Gamemode
    def mode_init(self):
        # Frame
        up = ttk.Frame(self)
        up.columnconfigure(0, minsize=70)
        up.columnconfigure(1, weight=1)
        up1 = ttk.Frame(up)
        
        # Radiobuttons
        self.game_mode = IntVar(value=0)
        self.num_songs = IntVar(value=1)
        self.rb_1 = ttk.Radiobutton(up, text='개인전', value=0, variable=self.game_mode, command=self.change_mode)
        self.rb_2 = ttk.Radiobutton(up, text='팀전', value=1, variable=self.game_mode, command=self.change_mode)

        # Spinbar
        self.sb = ttk.Spinbox(up1, from_=1, to=50, textvariable=self.num_songs, wrap=True, state='disabled', command=self.change_num)

        # Start Button
        self.start_button = ttk.Button(up, text='출근', command=self.start_game)
        
        # Placing
        self.start_button.grid(column=2, row=0, rowspan=3, sticky='news')

        ttk.Label(up, text='현재 설정').grid(column=0, row=0, columnspan=2, sticky='news')
        self.rb_1.grid(column=0, row=1, columnspan=2, sticky='news')
        self.rb_2.grid(column=0, row=2, sticky='nwes')

        ttk.Label(up1, text='곡').pack(fill='both', side='right', expand=1)
        self.sb.pack(fill='both', side='left', expand=1)
        up1.grid(column=1, row=2, sticky='nwes', padx=(0, 5))
        
        up.pack(fill='both', side='top', padx=5, pady=5)
        
    # Remaining
    def rem_init(self):
        # Frame
        downFrame = ttk.Frame(self)
        downFrame.columnconfigure(0, weight=1)

        # Labels
        self.label3 = ttk.Label(downFrame, font=self.font1, text='퇴근까지 걸린 시간')
        self.label4 = ttk.Label(downFrame, font=self.font2, text='00:00:00')

        # Placing
        self.label3.grid(column=0, row=0)
        self.label4.grid(column=0, row=1)
        downFrame.pack(fill='both', side='top', pady=10)

    # Next Song
    def nextSong_init(self):
        # Frame
        mid = ttk.Frame(self)
        mid.columnconfigure(0, minsize=90)
        mid.columnconfigure(1, weight=1)
        mid1 = ttk.Frame(mid)

        # Variables
        self.chk_var = IntVar(value=0)
        initials = [
            'A', 'B', 'C', 'D', 'E', 'F',
            'G', 'H', 'I', 'J', 'K', 'L',
            'M', 'N', 'O', 'P', 'Q', 'R',
            'S', 'T', 'U', 'V', 'W', 'X',
            'Y', 'Z', '0', '1', '2', '3',
            '4', '5', '6', '7', '8', '9'
        ]

        # Labels (column 0)
        ttk.Label(mid, text='곡 제목').grid(column=0, row=0, sticky='news', pady=(0, 5))
        ttk.Label(mid, text='다음 이니셜').grid(column=0, row=1, sticky='news', pady=(0, 5))
        ttk.Label(mid, text='추가 이니셜').grid(column=0, row=2, sticky='news', pady=(0, 5))
        
        # Inputs (column 1)
        self.input = ttk.Entry(mid, state='disabled')
        self.cb_1 = ttk.Combobox(mid, values=initials, state='disabled')
        self.cb_1.current(0)
        self.chk = ttk.Checkbutton(mid1, variable=self.chk_var, state='disabled', command=self.additional)
        self.cb_2 = ttk.Combobox(mid1, values=initials, state='disabled')
        self.cb_2.current(0)

        self.input.grid(column=1, row=0, sticky='news', pady=(0, 5))
        self.cb_1.grid(column=1, row=1, sticky='news', pady=(0, 5))
        self.chk.pack(side='left')
        self.cb_2.pack(fill='x', side='right', expand=1)
        mid1.grid(column=1, row=2, sticky='nwes', pady=(0, 5))

        # Buttons
        self.add_button = ttk.Button(mid, text='곡 추가', state='disabled', command=self.add_song)
        self.add_button.grid(column=1, row=3, sticky='news')

        mid.pack(fill='both', side='top', padx=5, pady=5)

    # Current Song (Marquee)
    def currSong_init(self):
        self.can1 = Canvas(self, width=240, height=150)
        self.can1.pack(side='top', pady=2)
        
        self.can1.create_text(122, 72, text='리듬\n끝말잇기', font=self.font3, justify='center', fill='black', tags=('sn'))
        self.can1.create_text(120, 300, text='다음 알파벳', font=self.font4, fill='black', tags=('txt'))
        self.can1.create_text(120, 300, text='A/A', font=self.font5, fill='orange', tags=('ni'))

    # Songlist (Marquee)
    def songlist_init(self):
        self.can2 = Canvas(self, width=240, height=300)
        self.can2.pack(side='top', pady=2)

        self.can2.create_text(122, 140, text='아직\n곡이\n없습니다!', font=self.font5, justify='center', fill='black', tags=('sl'))

    # Changing Gamemode
    def change_mode(self):
        mode = self.game_mode.get()
        if mode == 0:
            self.label3['text'] = '퇴근까지 걸린 시간'
            self.label4['text'] = '00:00:00'
            self.sb['state'] = 'disabled'
        if mode == 1:
            self.label3['text'] = '레진 정산까지'
            self.label4['text'] = '{}곡 남음'.format(self.num_songs.get())
            self.sb['state'] = 'readonly'

    # Changing Number of Songs to Play
    def change_num(self):
        self.label4['text'] = '{}곡 남음'.format(self.num_songs.get())
    
    # Start Button Function
    def start_game(self):
        mode = self.game_mode.get()

        if self.start_button['text'] == '출근':     # Start Game
            # Gamemode
            self.rb_1['state'] = 'disabled'
            self.rb_2['state'] = 'disabled'
            self.sb['state'] = 'disabled'

            # Next Song
            self.input['state'] = 'normal'
            self.input.focus()
            self.cb_1['state'] = 'readonly'
            self.chk['state'] = 'normal'
            self.add_button['state'] = 'normal'

            # Current Song
            self.can1.itemconfig('sn', text='첫 곡을\n플레이 해주세요!', font=self.font6)

            if mode == 0:   # Free For All (FFA)
                self.timerBool = True
                self.timer(0)
                self.start_button['text'] = '퇴근'
            
            if mode == 1:   # Team Match (TM)
                self.start_button['text'] = '리셋'
                self.start_button['state'] = 'disabled'
                self.songcount = self.num_songs.get()
        
        elif self.start_button['text'] == '퇴근':   # End Game (FFA only)
            if not self.startBool:
                messagebox.showerror('리듬 끝말잇기', '아직 첫 곡을 플레이하지 않았습니다.\n첫 곡을 플레이 해주세요.')
            else:
                # Remaining
                self.timerBool = False

                # Gamemode
                self.start_button['text'] = '리셋'

                # Next Song
                self.input.delete(0, 'end')
                self.cb_1.current(0)
                self.cb_2.current(0)
                self.chk_var.set(0)
                self.input['state'] = 'disabled'
                self.cb_1['state'] = 'disabled'
                self.cb_2['state'] = 'disabled'
                self.chk['state'] = 'disabled'
                self.add_button['state'] = 'disabled'

                # Current Song
                self.can1.itemconfig('ni', text='끝')

        elif self.start_button['text'] == '리셋':   # Reset Game
            # Gamemode
            self.start_button['text'] = '출근'
            self.rb_1['state'] = 'normal'
            self.rb_2['state'] = 'normal'
            
            # Remaining
            if mode == 0:   # FFA
                self.label4['text'] = '00:00:00'
            if mode == 1:   # TM
                self.sb['state'] = 'readonly'
                self.label4['text'] = '{}곡 남음'.format(self.num_songs.get())
            
            # Current Song
            self.can1.itemconfig('sn', text='리듬\n끝말잇기', font=self.font3)
            self.can1.coords('sn', 122, 72)
            self.can1.coords('txt', 120, 300)
            self.can1.coords('ni', 120, 300)
            self.marqBool = False

            # Songlist
            self.marqBool2 = False
            self.can2.itemconfig('sl', text='아직\n곡이\n없습니다!', font=self.font5)
            self.can2.coords('sl', 122, 140)
            self.songlist = '플레이한 목록\n'

    # Timer For FFA
    def timer(self, t):
        if self.timerBool:
            hrs = t // 3600
            mins = (t % 3600) // 60
            secs = t % 60

            self.label4['text'] = '{:02}:{:02}:{:02}'.format(hrs, mins, secs)
            self.after(1000, self.timer, t + 1)

    # Additional Initial
    def additional(self):
        mode = self.chk_var.get()
        if mode == 0:
            self.cb_2['state'] = 'disabled'
        if mode == 1:
            self.cb_2['state'] = 'readonly'

    # Adding a Song to the Songlist
    def add_song(self):
        # Input
        songName = self.input.get()
        alpha = self.cb_1.get()
        if self.chk_var.get() == 1:
            alpha = alpha + '/' + self.cb_2.get()

        # Reset Input
        self.input.delete(0, 'end')
        self.input.focus()
        self.cb_1.current(0)
        self.cb_2.current(0)
        self.chk_var.set(0)
        self.cb_2['state'] = 'disabled'
        
        # Output
        if songName and not songName.isspace():
            # Canvas
            self.can1.itemconfig('sn', text=songName)
            self.can1.itemconfig('ni', text=alpha)
            self.can1.coords('txt', 70, 130)
            self.can1.coords('ni', 190, 120)
            
            # Marquee
            pos = self.can1.bbox('sn')
            if pos[2] - pos[0] >= 230 and not self.marqBool:
                self.can1.coords('sn', 10 + (pos[2] - pos[0]) // 2, 50)
                self.marqBool = True
                self.marquee1()
            elif pos[2] - pos[0] < 230:
                self.can1.coords('sn', 122, 50)
                self.marqBool = False

            # Song List
            self.startBool = True
            self.songlist = self.songlist + songName + '\n'
            self.can2.itemconfig('sl', text=self.songlist, font=self.font7)
            pos2 = self.can2.bbox('sl')
            if pos2[3] - pos[1] >= 290 and not self.marqBool2:
                self.marqBool2 = True
                self.marquee2()
            else: 
                self.can2.coords('sl', 122, 10 + (pos2[3] - pos2[1]) // 2)

            # For TM
            if self.game_mode.get() == 1:
                self.songcount -= 1
                self.label4['text'] = '{}곡 남음'.format(self.songcount)

                # No More Song
                if self.songcount == 0:
                    self.can1.itemconfig('ni', text='끝')
                    self.input['state'] = 'disabled'
                    self.cb_1['state'] = 'disabled'
                    self.cb_2['state'] = 'disabled'
                    self.chk['state'] = 'disabled'
                    self.start_button['state'] = 'normal'
                    self.add_button['state'] = 'disabled'
        else:   # Empty Input
            messagebox.showinfo('리듬 끝말잇기', '곡 제목 칸이 비어있습니다\n다시 적어주세요')

    # Marquee Effect 1
    def marquee1(self):
        if self.marqBool:
            pos = self.can1.bbox('sn')
            if pos[2] < 0:
                self.can1.coords('sn', 240 + (pos[2] - pos[0]) // 2, 50)
            else:
                self.can1.move('sn', -2, 0)
            self.after(1000 // 30, self.marquee1)

    def marquee2(self):
        if self.marqBool2:
            pos = self.can2.bbox('sl')
            if pos[3] < 0:
                self.can2.coords('sl', 122, 300 + (pos[3] - pos[1]) // 2)
            else:
                self.can2.move('sl', 0, -1)
            self.after(1000 // 45, self.marquee2)

if __name__ == '__main__':
    app = Window()
    app.mainloop()