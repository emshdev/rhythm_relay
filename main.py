from    tkinter    import   Canvas, StringVar, Tk, ttk, IntVar, messagebox, Listbox, Toplevel
from    pandas     import   read_csv
import  re, time

class Window(Tk):
    def __init__(self):
        super().__init__()

        # Window Initialization
        self.title('리듬 끝말잇기')
        self.geometry('535x565')
        self.resizable(0, 0)
        self.attributes('-topmost', True)

        # Data Initialization
        self.data_init()

        # Form Initialization
        self.leftFrame = ttk.Frame(self)
        self.rightFrame = ttk.Frame(self)

        self.font_init()
        self.mode_init()
        ttk.Separator(self.leftFrame, orient='horizontal').pack(fill='x', padx=5, side='top')
        ttk.Label(self.leftFrame, text='절취선', justify='center').pack(fill='y', pady=5, side='top')
        ttk.Separator(self.leftFrame, orient='horizontal').pack(fill='x', padx=5, side='top')
        self.nextSong_init()
        self.rem_init()
        ttk.Separator(self.rightFrame, orient='horizontal').pack(fill='x', padx=5, side='top')
        self.currSong_init()
        ttk.Separator(self.rightFrame, orient='horizontal').pack(fill='x', padx=5, side='top')
        self.songlist_init()

        self.leftFrame.pack(fill='y', side='left')
        ttk.Separator(self, orient='vertical').pack(fill='y', side='left', pady=5)
        self.rightFrame.pack(fill='both', side='right', expand=1)

        # Variables Initialization
        self.var_init()

    # Initializations
    # (Literally) Initialize modules and variables

    # Database
    def data_init(self):
        # Loading Database (in UTF-8)
        self.data = read_csv('songlist.csv', encoding='UTF-8')
        data_filter = (self.data['Start_letter'].notnull()) & (self.data['End_letter'].notnull())
        self.data = self.data.loc[data_filter][['Song_name', 'Start_letter', 'End_letter']]

        # Creating lists based on self.data
        self.song_def = self.data.values.tolist()   # Back-up
        self.songlist = []      # Actual songlist (duplicates removed)
        [self.songlist.append(x) for x in self.song_def if x not in self.songlist]
        self.list_used = []     # List of used songs (empty as default)
        self.song_names = [x[0] for x in self.songlist]     # List of song names

    # List of fonts    
    def font_init(self):
        # Timer
        self.font1 = ('강원교육모두 Bold', 16)
        self.font2 = ('강원교육모두 Bold', 28)
        
        # Marquee
        self.font3 = ('Kotra Leap', 32)
        self.font4 = ('Kotra Leap', 20)
        self.font5 = ('Kotra Leap', 40)
        self.font6 = ('Kotra Leap', 24)
        self.font7 = ('Kotra Leap', 16)

    # Variables
    def var_init(self):
        # Booleans
        self.timerBool = False
        self.marqBool = False
        self.marqBool2 = False
        self.startBool = False
        self.pauseBool = False
        self.editBool = False
        
        # Ints and Doubles
        self.songcount = 0
        self.start_time = 0
        self.curr_time = 0
        
        # Strings
        self.songtext = '플레이한 목록\n'

    # Gamemode
    def mode_init(self):
        # Frame
        up = ttk.Frame(self.leftFrame)
        up.columnconfigure(0, minsize=70)
        up.columnconfigure(1, weight=1)
        up.columnconfigure(2, weight=1)
        up1 = ttk.Frame(up)
        
        # Radiobuttons
        self.game_mode = IntVar(value=0)
        self.num_songs = IntVar(value=1)
        self.rb_1 = ttk.Radiobutton(up, text='개인전', value=0, variable=self.game_mode, command=self.change_mode)
        self.rb_2 = ttk.Radiobutton(up, text='팀전', value=1, variable=self.game_mode, command=self.change_mode)

        # Spinbar
        self.sb = ttk.Spinbox(up1, from_=1, to=50, textvariable=self.num_songs, wrap=True, width=6, state='disabled', command=self.change_num, exportselection=0)

        # Start Button
        self.start_button = ttk.Button(up, text='출근', command=self.start_game)
        
        # Placing
        ttk.Label(up, text='현재 설정').grid(column=0, row=0, columnspan=2, sticky='news')
        self.rb_1.grid(column=0, row=1, columnspan=2, sticky='news')
        self.rb_2.grid(column=0, row=2, sticky='nwes')

        ttk.Label(up1, text='곡').pack(fill='both', side='right', expand=1)
        self.sb.pack(fill='both', side='right', expand=1)
        up1.grid(column=1, row=2, sticky='nes', padx=(0, 5))

        self.start_button.grid(column=2, row=0, rowspan=3, sticky='news')
        
        up.pack(fill='both', side='top', padx=5, pady=5)

    # Next Song
    def nextSong_init(self):
        # Frame
        mid = ttk.Frame(self.leftFrame)
        mid.columnconfigure(0, minsize=90)
        mid.columnconfigure(1, weight=1)
        mid1 = ttk.Frame(mid)
        mid2 = ttk.Frame(mid)

        # Variables
        self.chk_var = IntVar(value=0)
        initials = [
            'A', 'B', 'C', 'D', 'E', 'F',
            'G', 'H', 'I', 'J', 'K', 'L',
            'M', 'N', 'O', 'P', 'Q', 'R',
            'S', 'T', 'U', 'V', 'W', 'X',
            'Y', 'Z'
        ]
        self.song_str = StringVar()
        self.song_str.trace('w', self.update_songlist)

        # Input
        self.input = ttk.Entry(mid, textvariable=self.song_str, state='disabled')
        
        # Checkbox
        self.chk = ttk.Checkbutton(mid1, variable=self.chk_var, state='disabled', command=self.additional)

        # Combobox
        self.cb_1 = ttk.Combobox(mid1, values=initials, state='disabled', exportselection=0)
        self.cb_1.current(0)

        # Listbox with Scrollbar
        self.lb = Listbox(mid2, listvariable=StringVar(value=self.song_names), activestyle='none', selectmode='browse', state='disabled', exportselection=0, height=15)
        self.scroll = ttk.Scrollbar(mid2, orient='vertical', command=self.lb.yview)
        self.lb['yscrollcommand'] = self.scroll.set
        self.lb.bind('<<ListboxSelect>>', lambda e: self.add_button.configure(state='normal'))

        # Buttons
        self.add_button = ttk.Button(mid, text='곡 추가', state='disabled', command=self.add_song)
        self.pause_button = ttk.Button(mid, text='일시정지', state='disabled', command=self.pause_game)
        self.edit_button = ttk.Button(mid, text='곡 수정', state='disabled', command=self.edit_initial)

        # Placing
        ttk.Label(mid, text='곡 제목').grid(column=0, row=0, sticky='news', pady=(0, 5))
        ttk.Label(mid, text='알파벳 룰렛').grid(column=0, row=1, sticky='news', pady=(0, 5))

        self.input.grid(column=1, row=0, sticky='nwes', pady=(0, 5))
        self.chk.pack(side='left')
        self.cb_1.pack(fill='x', side='right', expand=1)
        mid1.grid(column=1, row=1, sticky='nwes', pady=(0, 5))

        self.lb.pack(fill='both', side='left', expand=1)
        self.scroll.pack(fill='y', side='right')
        mid2.grid(column=0, row=2, columnspan=2, sticky='nswe', pady=(0, 5))

        self.add_button.grid(column=1, row=3, sticky='news', pady=(0, 5))
        self.pause_button.grid(column=0, row=3, rowspan=2, sticky='news', padx=(0, 5))
        self.edit_button.grid(column=1, row=4, sticky='news')

        mid.pack(fill='both', side='top', padx=5, pady=5)

    # Remaining
    def rem_init(self):
        # Frame
        down = ttk.Frame(self.rightFrame)
        down.columnconfigure(0, weight=1)

        # Labels
        self.label3 = ttk.Label(down, font=self.font1, text='퇴근까지 걸린 시간')
        self.label4 = ttk.Label(down, font=self.font2, text='00:00:00')

        # Placing
        self.label3.grid(column=0, row=0)
        self.label4.grid(column=0, row=1)
        down.pack(fill='both', side='top', pady=10)

    # Current Song (Marquee)
    def currSong_init(self):
        # Canvas
        self.can1 = Canvas(self.rightFrame, width=240, height=150)
        self.can1.pack(side='top', pady=2)
        
        # Texts
        self.can1.create_text(122, 72, text='리듬\n끝말잇기', font=self.font3, justify='center', fill='black', tags=('sn'))
        self.can1.create_text(120, 300, text='다음 알파벳', font=self.font4, fill='black', tags=('txt'))
        self.can1.create_text(120, 300, text='A/A', font=self.font5, fill='orange', tags=('ni'))

    # Songlist (Marquee)
    def songlist_init(self):
        # Canvas
        self.can2 = Canvas(self.rightFrame, width=240, height=300)
        self.can2.pack(side='top', pady=2)

        # Text
        self.can2.create_text(122, 140, text='아직\n곡이\n없습니다!', font=self.font5, justify='center', fill='black', tags=('sl'))

    # Methods
    # Functions linked to modules and variables (Need optimization)

    # change_mode: Changes gamemode
    def change_mode(self):
        if self.game_mode.get() == 0:   # FFA
            self.label3['text'] = '퇴근까지 걸린 시간'
            self.label4['text'] = '00:00:00'
            self.sb['state'] = 'disabled'
        else:       # TM
            self.label3['text'] = '레진 정산까지'
            self.label4['text'] = '{}곡 남음'.format(self.num_songs.get())
            self.sb['state'] = 'readonly'

    # change_num: Changes number of songs to play (TM Only)
    def change_num(self):
        self.label4['text'] = '{}곡 남음'.format(self.num_songs.get())

    # marquee1: Marquee effect for 'current song'
    def marquee1(self):
        if self.marqBool:
            pos = self.can1.bbox('sn')
            if pos[2] < 0:
                self.can1.coords('sn', 240 + (pos[2] - pos[0]) // 2, 50)
            else:
                self.can1.move('sn', -2, 0)
            self.after(1000 // 30, self.marquee1)

    # marquee2: Marquee effect for 'list of used songs'
    def marquee2(self):
        if self.marqBool2:
            pos = self.can2.bbox('sl')
            if pos[3] < 0:
                self.can2.coords('sl', 122, 300 + (pos[3] - pos[1]) // 2)
            else:
                self.can2.move('sl', 0, -1)
            self.after(1000 // 45, self.marquee2)

    # update_songlist: Updates songlist on self.lb based on self.song_str (= self.input.get())
    def update_songlist(self, *argv):
        self.lb.see(0)
        if self.song_str == '\0':
            self.lb['listvariable'] = StringVar(value=self.song_names)
        else:
            typed_song = self.input.get()
            avail_songs = [x for x in self.song_names if re.match(typed_song, x, re.I)]
            self.lb['listvariable'] = StringVar(value=avail_songs)

    # timer: Updates time (FFA Only)
    def timer(self):
        self.curr_time = time.time()
        if self.timerBool:
            total_time = int(self.curr_time - self.start_time)
            hrs =  total_time// 3600
            mins = (total_time % 3600) // 60
            secs = total_time % 60
            self.label4['text'] = '{:02}:{:02}:{:02}'.format(hrs, mins, secs)
            if self.pauseBool:
                self.start_time = time.time() - total_time
            self.after(1, self.timer)

    # pause_game: Pauses/unpauses the timer
    def pause_game(self):
        if not self.pauseBool:
            self.pauseBool = True
            self.pause_button['text'] = '재개'

            self.input['state'] = 'disabled'
            self.chk['state'] = 'disabled'
            self.cb_1['state'] = 'disabled'
            self.add_button['state'] = 'disabled'
            self.lb['state'] = 'disabled'
            self.lb.select_clear(0, 'end')
        else:
            self.pauseBool = False
            self.pause_button['text'] = '일시정지'
            
            self.input['state'] = 'normal'
            self.chk['state'] = 'normal'
            if self.chk_var.get() == 1:
                self.cb_1['state'] = 'normal'
            self.add_button['state'] = 'normal'
            self.lb['state'] = 'normal'
            try:
                self.lb.see(self.lb.curselection())
            except:
                self.lb.see(0)

    # additional: Updates the end letter (When the reroll roulette is spinned)
    def additional(self):
        if self.chk_var.get() == 0:
            self.cb_1['state'] = 'disabled'
        else:
            self.cb_1['state'] = 'readonly'

    # find_song: Finds song with matching songName
    # └Return:  self.songlist.index(song) or -1
    def find_song(self, songName:str):
        for song in self.songlist:
            if songName == song[0]:
                return self.songlist.index(song)
        return -1
    
    # mode switch: Turns on/off the mode modules
    def mode_switch(self, state=True):
        if state == True:   # Enable gamemode
            self.start_button['text'] = '출근'
            self.rb_1['state'] = 'normal'
            self.rb_2['state'] = 'normal'

            if self.game_mode.get() == 0:   # FFA
                self.label4['text'] = '00:00:00'
                self.curr_time = 0
            else:   # TM
                self.sb['state'] = 'readonly'
                self.label4['text'] = '{}곡 남음'.format(self.num_songs.get())

        else:   # Disable gamemode
            self.rb_1['state'] = 'disabled'
            self.rb_2['state'] = 'disabled'
            self.sb['state'] = 'disabled'

            if self.game_mode.get() == 0:   # FFA
                self.start_button['text'] = '퇴근'
                self.pause_button['state'] = 'normal'

                self.start_time = time.time()
                self.timerBool = True
                self.timer()
            else:   # TM
                self.start_button['text'] = '리셋'
                self.start_button['state'] = 'disabled'

                self.songcount = self.num_songs.get()

    # input_reset: Clears self.input and deselects any item in self.lb
    def input_reset(self):
        self.lb.see(0)
        self.lb.select_clear(0, 'end')

        self.song_str.set('')
        self.input.focus()

        self.cb_1.current(0)
        self.cb_1['state'] = 'disabled'

        self.chk_var.set(0)

        self.add_button['state'] = 'disabled'

    # input_switch: Turns on/off the input modules
    def input_switch(self, state=True):
        if state == True:   # Enable input
            self.input['state'] = 'normal'
            self.chk['state'] = 'normal'
            self.lb['state'] = 'normal'
        else:   # Disable input
            self.input['state'] = 'disabled'
            self.chk['state'] = 'disabled'
            self.lb['state'] = 'disabled'
            
            self.pause_button['state'] = 'disabled'
            self.pause_button['text'] = '일시정지'

            self.start_button['state'] = 'normal'
            self.start_button['text'] = '리셋'
            self.can1.itemconfig('ni', text='끝')

            self.edit_button['state'] = 'disabled'

    # Child Window
    # For editting the end letter

    def edit_initial(self):
        # Blocking other inputs while this child window is open
        self.input['state'] = 'disabled'
        self.chk['state'] = 'disabled'
        self.cb_1['state'] = 'disabled'
        self.lb['state'] = 'disabled'
        self.add_button['state'] = 'disabled'
        self.edit_button['state'] = 'disabled'

        # Child window initialization
        self.child_win = Toplevel(self)
        self.child_win.geometry('250x250')
        self.child_win.resizable(0, 0)
        self.child_win.attributes('-topmost', True)
        self.child_win.protocol('WM_DELETE_WINDOW', self.restore_initial)

        # Canvas
        self.can3 = Canvas(self.child_win, width=240, height=80)
        self.can3.pack(side='top', pady=2)

        self.can3.create_text(122, 37, text=self.list_used[-1][0], font=self.font6, justify='center', fill='black', tags=('sn'))
        pos = self.can3.bbox('sn')
        if pos[2] - pos[0] >= 230:
            self.can3.coords('sn', 10 + (pos[2] - pos[0]) // 2, 37)
            self.editBool = True
            self.last_song()
        
        # Frame
        bottom = ttk.Frame(self.child_win)
        bottom.columnconfigure(0, weight=1)
        bottom.columnconfigure(1, weight=1)

        # Left: current letter
        ttk.Label(bottom, text='현재 이니셜', font=self.font1).grid(column=0, row=0)
        ttk.Label(bottom, text=self.alpha, font=self.font5).grid(column=0, row=1, padx=5, pady=5)

        # Right: replacing letter
        initials = [
            'A', 'B', 'C', 'D', 'E', 'F',
            'G', 'H', 'I', 'J', 'K', 'L',
            'M', 'N', 'O', 'P', 'Q', 'R',
            'S', 'T', 'U', 'V', 'W', 'X',
            'Y', 'Z'
        ]
        ttk.Label(bottom, text='바꿀 이니셜', font=self.font1).grid(column=1, row=0)
        self.end_letter = ttk.Combobox(bottom, values=initials, state='readonly', font=self.font5, width=2, exportselection=0, justify='center')
        self.end_letter.current(0)
        self.end_letter.grid(column=1, row=1, padx=5, pady=5)

        # Buttons
        ttk.Button(bottom, text='이니셜 변경', command=self.change_initial).grid(column=0, row=2, padx=5, sticky='nswe')
        ttk.Button(bottom, text='취소', command=self.restore_initial).grid(column=1, row=2, padx=5, sticky='nswe')

        bottom.pack(fill='both', side='top', expand=1, padx=5, pady=5)

    # restore_initial (Child Window): closes the child window (without any changes)
    def restore_initial(self):
        self.input['state'] = 'normal'
        self.chk['state'] = 'normal'
        self.lb['state'] = 'normal'

        if self.chk_var.get() == 1:
            self.cb_1['state'] = 'readonly'

        self.edit_button['state'] = 'normal'
        self.editBool = False
        self.child_win.destroy()
    
    # change_initial (Child Window): replaces the end letter, then calls self.restore_initial
    def change_initial(self):
        self.alpha = self.end_letter.get()
        self.can1.itemconfig('ni', text=self.alpha)
        self.input_reset()
        self.song_str.set(self.alpha)
        self.restore_initial()

    # last_song (Child Window): marquee effect for the child window
    def last_song(self):
        if self.editBool:
            pos = self.can3.bbox('sn')
            if pos[2] < 0:
                self.can3.coords('sn', 240 + (pos[2] - pos[0]) // 2, 37)
            else:
                self.can3.move('sn', -2, 0)
            self.after(1000 // 30, self.last_song)

    # Functions
    # Main functions with combination of methods

    # start_game
    # 1. Starts the game if self.start_button['text'] == '출근'
    # 2. Ends the game if self.start_button['text'] == '퇴근'
    # 3. Resets the game if self.start_button['text'] == '리셋'
    def start_game(self):
        if self.start_button['text'] == '출근':     # Start Game
            self.mode_switch(False)
            self.input_switch(True)
            self.input_reset()
            self.can1.itemconfig('sn', text='첫 곡을\n플레이 해주세요!', font=self.font6)
        
        elif self.start_button['text'] == '퇴근':   # End Game (FFA Only)
            if not self.startBool:
                messagebox.showerror('리듬 끝말잇기', '아직 첫 곡을 플레이하지 않았습니다.\n첫 곡을 플레이 해주세요.')
            else:
                self.timerBool = False
                self.pauseBool = False

                self.input_reset()
                self.input_switch(False)

        elif self.start_button['text'] == '리셋':   # Reset Game
            self.mode_switch(True)
            
            # Current Song
            self.marqBool = False
            self.can1.itemconfig('sn', text='리듬\n끝말잇기', font=self.font3)
            self.can1.coords('sn', 122, 72)
            self.can1.coords('txt', 120, 300)
            self.can1.coords('ni', 120, 300)

            # Songlist
            self.startBool = False
            for song in self.list_used:
                self.songlist.append(song)
                self.song_names.append(song[0])
            self.list_used.clear()

            # Used songs
            self.marqBool2 = False
            self.can2.itemconfig('sl', text='아직\n곡이\n없습니다!', font=self.font5)
            self.can2.coords('sl', 122, 140)
            self.songtext = '플레이한 목록\n'
    
    # add_song
    # 1. Finds the song from self.songlist
    # 2. Pops the song from self.songlist and pushes it to self.list_used
    # 3. Resets the input modules
    # 4. Draws the result onto self.can1 and self.can2
    def add_song(self):
        # Input
        songName = self.lb.get(self.lb.curselection())
        curr_song = self.find_song(songName)

        if curr_song == -1: 
            messagebox.showerror('리듬 끝말잇기', '곡이 선택되지 않은 상태입니다.\n곡을 선택해주세요.')
        else:
            self.alpha = self.songlist[curr_song][2]

            # End letter
            if self.chk_var.get() == 1:
                self.alpha = self.cb_1.get()
            if self.alpha.isnumeric():
                switch = {
                    '1': '1/E',
                    '2': '2/O',
                    '3': '3/E',
                    '4': '4/R',
                    '5': '5/E',
                    '6': '6/X',
                    '7': '7/N',
                    '8': '8/T',
                    '9': '9/E',
                    '0': '0/O'
                }
                self.alpha = switch.get(self.alpha)

            # Reset input
            self.input_reset()
            self.song_str.set(self.alpha)
        
            # Modify lists
            self.list_used.append(self.songlist[curr_song])
            self.songlist.remove(self.songlist[curr_song])
            self.song_names.remove(songName)

            # Start game
            if not self.startBool:
                self.startBool = True
                self.can1.coords('txt', 70, 130)
                self.can1.coords('ni', 190, 120)
                self.edit_button['state'] = 'normal'

            # Texts
            self.can1.itemconfig('sn', text=songName)
            self.can1.itemconfig('ni', text=self.alpha)
            self.songtext = self.songtext + songName + '\n'
            self.can2.itemconfig('sl', text=self.songtext, font=self.font7)

            # marquee1
            pos = self.can1.bbox('sn')
            self.can1.coords('sn', 122, 50)
            if pos[2] - pos[0] >= 230:
                self.can1.coords('sn', 10 + (pos[2] - pos[0]) // 2, 50)
                if not self.marqBool:
                    self.marqBool = True
                    self.marquee1()
            else:
                self.marqBool = False

            # marquee2
            pos2 = self.can2.bbox('sl')
            if pos2[3] - pos[1] >= 290:
                if not self.marqBool2:
                    self.marqBool2 = True
                    self.marquee2()
            else:
                self.can2.coords('sl', 122, 10 + (pos2[3] - pos2[1]) // 2)
                
            # Countdown (TM Only)
            if self.game_mode.get() == 1:
                self.songcount -= 1
                self.label4['text'] = '{}곡 남음'.format(self.songcount)
                if self.songcount == 0:
                    self.input_switch(False)

if __name__ == '__main__':
    app = Window()
    app.mainloop()