import tkinter as tk
from tkinter import Frame, ttk
import pandas as pd

# Base Window (Object Oriented)
class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # Window Initialization
        self.title('리듬 끝말잇기')
        self.geometry('600x600')
        self.resizable(False, False)

        # Widget Initialization
        self.init_font()
        self.read_songlist()
        self.init_songlist()
        self.reset_songlist()
        self.init_search()

    # List of fonts
    def init_font(self):
        self.font1 = ('여기어때 잘난체', 24)
        self.font2 = ('강원교육모두 Bold', 16)

    # Song list
    def read_songlist(self):
        songlist = pd.read_excel('list.xlsx').values.tolist()
        self.baseSL = []
        
        for item in songlist:
            if '있' in item[7] and item[3] * 60 + item[4] <= 180:
                self.baseSL.append((item[0], item[1], item[2],
                    '{}:{:02}'.format(item[3], item[4]), item[5], item[6],
                    item[8], item[9]))

    def init_songlist(self):
        # Widget Wrapper
        songlist_group = Frame(self)

        # Song list
        self.table = ttk.Treeview(
            songlist_group,
            columns=('title', 'search', 'composer', 'time',
                'game', 'section', 'start', 'end'),
            displaycolumns=('title', 'time', 'game'),
            show='headings',
            selectmode='browse'
        )
        self.table.column('time', width=40, stretch=0)
        self.table.column('game', width=120, stretch=0)
        self.table.heading('title', text='곡명', anchor='w')
        self.table.heading('time', text='시간', anchor='w')
        self.table.heading('game', text='수록 게임', anchor='w')

        # Scrollbar
        scroll = ttk.Scrollbar(
            songlist_group, 
            orient=tk.VERTICAL, 
            command=self.table.yview
        )
        self.table.configure(yscrollcommand=scroll.set)

        # Placing
        self.table.pack(side='left', expand=1, fill='x')
        scroll.pack(side='left', fill='y')
        songlist_group.pack(side='top', padx=10, pady=10, fill='x')
    
    def reset_songlist(self):
        self.currentSL = self.baseSL
        self.table.delete(*self.table.get_children())
        for item in self.currentSL:
            self.table.insert('', tk.END, values=item)
        #self.update()

    def init_search(self):
        # Widget Wrapper
        search_group = Frame(self)
        cb_group = Frame(search_group)

        # Game list
        self.gamelist = ttk.Combobox(
            cb_group, 
            state='readonly'
        )
        games = []
        for item in self.baseSL:
            if item[4] not in games:
                games.append(item[4])
        games.insert(0, '전체 게임')
        self.gamelist['values'] = games
        self.gamelist.current(0)

        # Section list
        self.sectionlist = ttk.Combobox(
            cb_group,
            state='disable'
        )

        # Search Bar
        self.searchbar = ttk.Entry(search_group)

        # Placing
        self.gamelist.pack(side='top')
        self.sectionlist.pack(side='bottom', pady=(10, 0))
        cb_group.pack(side='left')
        self.searchbar.pack(side='left', expand=1, fill='both', padx=(10, 0))
        search_group.pack(side='top', fill='x', padx=10)        

if __name__ == "__main__":
    app = App()
    app.mainloop()
