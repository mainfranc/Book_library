import tkinter as tk


class Interface:
    class PopUp:
        def __init__(self, inf_):
            self.root = tk.Tk()
            self.root.wm_title("!")
            label = tk.Label(self.root, text=inf_, font=('arial', 12))
            label.pack(side="top", fill="x", pady=10)
            but_ = tk.Button(self.root, text="Ok", command=self.root.destroy)
            but_.pack()
            self.root.mainloop()

    def __init__(self):
        self.__full_lib = self.import_func()
        self.__root = None
        self.__book_name_text = None
        self.__book_author_text = None
        self.__book_year_text = None
        self.__book_desc_text = None

    def __del__(self):
        with open("Full_library.txt", "w") as source_file:
            source_file.truncate(0)
            for line in self.__full_lib:
                source_file.write(';'.join(line))

    def main(self):
        self.__root = tk.Tk()
        self.__root.title('Book library')
        button1 = tk.Button(self.__root, text='Add Book', width=20, height=1,
                            font=('arial', 16, 'bold'), command=lambda: self.add_books())
        button1.grid(row=1, column=0, sticky='nsew')
        button2 = tk.Button(self.__root, text='Search Books', width=20, height=1,
                            font=('arial', 16, 'bold'), command=lambda: self.search_books(self.__full_lib))
        button2.grid(row=2, column=0, sticky='nsew')
        self.__root.mainloop()

    def back_to_main(self):
        self.__root.destroy()
        self.main()

    def create_header(self, root):
        lbl_name = tk.Label(root, text="input book name", width=20, height=1)
        lbl_name.grid(row=1, column=0, sticky='nw')
        lbl_author = tk.Label(root, text="input book author", width=20, height=1)
        lbl_author.grid(row=1, column=1, sticky='nw')
        lbl_year = tk.Label(root, text="input book year", width=20, height=1)
        lbl_year.grid(row=1, column=2, sticky='nw')
        lbl_desc = tk.Label(root, text="input book description", width=24, height=1)
        lbl_desc.grid(row=1, column=3, sticky='nw')

        self.__book_name_text = tk.Text(root, width=20, height=2)
        self.__book_name_text.grid(row=2, column=0, sticky='nw')
        self.__book_author_text = tk.Text(root, width=20, height=2)
        self.__book_author_text.grid(row=2, column=1, sticky='nw')
        self.__book_year_text = tk.Text(root, width=20, height=2)
        self.__book_year_text.grid(row=2, column=2, sticky='nw')
        self.__book_desc_text = tk.Text(root, width=24, height=2)
        self.__book_desc_text.grid(row=2, column=3, sticky='nw')

    def add_books(self):
        self.__root.destroy()
        self.__root = tk.Tk()
        self.__root.title('Add book')
        button_back = tk.Button(self.__root, text='Back to main', width=12, height=1,
                                font=('arial', 16, 'bold'), command=lambda: self.back_to_main())
        button_back.grid(row=0, column=0, sticky='nw')
        self.create_header(self.__root)
        button_add = tk.Button(self.__root, text='Add book', width=12, height=1,
                               font=('arial', 16, 'bold'), command=lambda: self.lib_append())
        button_add.grid(row=3, column=0, sticky='nsew')
        self.__root.mainloop()

    def edit_screen(self, name_, auth_, year_, desc_):
        self.__root.destroy()
        self.__root = tk.Tk()
        self.__root.title('enter the new values')
        button_back = tk.Button(self.__root, text='Back to main', width=12, height=1,
                                font=('arial', 16, 'bold'), command=lambda: self.back_to_main())
        button_back.grid(row=0, column=0, sticky='nw')
        self.create_header(self.__root)
        self.__book_name_text.insert('end-1c', name_)
        self.__book_author_text.insert('end-1c', auth_)
        self.__book_year_text.insert('end-1c', year_)
        self.__book_desc_text.insert('end-1c', desc_)
        button_add = tk.Button(self.__root, text='Edit entry', width=12, height=1,
                               font=('arial', 16, 'bold'), command=lambda: self.change_entry(name_, auth_,
                                                                                             year_, desc_))
        button_add.grid(row=3, column=0, sticky='nsew')

    def search_books(self, show_lib):
        self.__root.destroy()
        self.__root = tk.Tk()
        self.__root.title('View books')
        main_frame = tk.Frame(self.__root)
        main_frame.pack()
        button_back = tk.Button(main_frame, text='Back to main', width=12, height=1,
                                font=('arial', 16, 'bold'), command=lambda: self.back_to_main())
        button_back.grid(row=0, column=0, sticky='nw')
        self.create_header(main_frame)
        button_search = tk.Button(main_frame, text='search book', width=12, height=1,
                                  font=('arial', 16, 'bold'),
                                  command=lambda: self.lib_filter())
        button_search.grid(row=3, column=0, sticky='nw')
        button_search = tk.Button(main_frame, text='clear search', width=12, height=1,
                                  font=('arial', 16, 'bold'), command=lambda: self.search_books(self.__full_lib))
        button_search.grid(row=3, column=1, sticky='nw')
        table_frame = tk.Frame(self.__root)
        canvas = tk.Canvas(table_frame)
        y_scrollbar = tk.Scrollbar(table_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=y_scrollbar.set)
        for rw in range(len(show_lib)):
            addition_ = tk.Text(scrollable_frame, width=3, height=2)
            addition_.grid(row=rw, column=0)
            addition_.insert('end-1c', rw + 1)
            for cl in range(len(show_lib[rw])):
                addition_ = tk.Text(scrollable_frame, width=24 if cl == 3 else 16, height=2)
                addition_.grid(row=rw, column=1 + cl)
                addition_.insert('end-1c', show_lib[rw][cl])
            addition_ = tk.Button(scrollable_frame, text='Edit', width=3, height=2,
                                  command=lambda r=rw: self.edit_screen(show_lib[r][0],
                                                                        show_lib[r][1],
                                                                        show_lib[r][2],
                                                                        show_lib[r][3]))
            addition_.grid(row=rw, column=5)
            addition_ = tk.Button(scrollable_frame, text='Remove', width=6, height=2,
                                  command=lambda r=rw: self.remove_entry(show_lib[r][0],
                                                                         show_lib[r][1],
                                                                         show_lib[r][2],
                                                                         show_lib[r][3]))
            addition_.grid(row=rw, column=6)
        table_frame.pack(fill="both")
        canvas.pack(side="left", fill="both", expand=True)
        y_scrollbar.pack(side="right", fill="y")
        self.__root.mainloop()

    @staticmethod
    def import_func():
        result = []
        with open('Full_library.txt', 'r') as source_file:
            for rw in source_file.readlines():
                result.append(tuple(rw.split(';')))
        return result

    def lib_append(self):
        self.__full_lib = self.import_func()
        nm = self.__book_name_text.get("1.0", 'end-1c')
        auth = self.__book_author_text.get("1.0", 'end-1c')
        yr = self.__book_year_text.get("1.0", 'end-1c')
        des = self.__book_desc_text.get("1.0", 'end-1c')
        if all([nm, auth]):
            if not yr.isnumeric():
                self.PopUp("Please enter the year as number")
            else:
                self.__full_lib.append((nm, auth, yr, des))
                self.__full_lib = sorted(self.__full_lib)
                self.__book_name_text.delete("1.0", 'end')
                self.__book_author_text.delete("1.0", 'end')
                self.__book_year_text.delete("1.0", 'end')
                self.__book_desc_text.delete("1.0", 'end')
        else:
            self.PopUp("Please fill book name and author fields")

    def lib_filter(self):
        self.__full_lib = sorted(self.__full_lib)
        lib_to_show = []
        for i in range(len(self.__full_lib)):
            if all([self.__book_name_text.get("1.0", 'end-1c') in self.__full_lib[i][0]
                    and self.__book_author_text.get("1.0", 'end-1c') in self.__full_lib[i][1]
                    and self.__book_year_text.get("1.0", 'end-1c') in self.__full_lib[i][2]
                    and self.__book_desc_text.get("1.0", 'end-1c') in self.__full_lib[i][3]]):
                lib_to_show.append(self.__full_lib[i])
        self.search_books(lib_to_show)

    def change_entry(self, name_old, auth_old, year_old, desc_old):
        self.__full_lib = sorted(self.__full_lib)
        nm = self.__book_name_text.get("1.0", 'end-1c')
        auth = self.__book_author_text.get("1.0", 'end-1c')
        yr = self.__book_year_text.get("1.0", 'end-1c')
        des = self.__book_desc_text.get("1.0", 'end-1c')
        if all([self.__book_name_text, self.__book_author_text]):
            if not yr.isnumeric():
                self.PopUp("Please enter the year as number")
            else:
                str_to_search = f'{name_old};{auth_old};{year_old};{desc_old}'
                join_lst = self.joined_list(self.__full_lib)
                ind_ = self.binary_search(str_to_search, join_lst)
                self.__full_lib[ind_] = (nm, auth, yr, des)
                self.search_books(self.__full_lib)
        else:
            self.PopUp("Please fill book name and author fields")

    def remove_entry(self, name_, auth_, year_, desc_):
        self.__full_lib = sorted(self.__full_lib)
        str_to_search = f'{name_};{auth_};{year_};{desc_}'
        join_lst = self.joined_list(self.__full_lib)
        ind_ = self.binary_search(str_to_search, join_lst)
        self.__full_lib.pop(ind_)
        self.search_books(self.__full_lib)

    @staticmethod
    def joined_list(lst):
        return [';'.join(i) for i in lst]

    @staticmethod
    def binary_search(elem, arr):
        if arr:
            # len_arr = len(arr)
            len_of_curr_d = len(arr) // 2 + 1
            beg_d = 0
            while elem != arr[beg_d + len_of_curr_d - 1] and len_of_curr_d != 1:
                if elem > arr[beg_d + len_of_curr_d - 1]:
                    beg_d += len_of_curr_d
                if not len_of_curr_d % 2:
                    len_of_curr_d //= 2
                else:
                    len_of_curr_d = len_of_curr_d // 2 + 1
            if arr[beg_d] == elem:
                return beg_d
            if beg_d + len_of_curr_d < len(arr):
                if arr[beg_d + len_of_curr_d] == elem:
                    return beg_d + len_of_curr_d
            if arr[beg_d + len_of_curr_d - 1] == elem:
                return beg_d + len_of_curr_d - 1
        return None
