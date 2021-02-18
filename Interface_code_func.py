import tkinter as tk
from Lib_code import *


def po_pup(inf_):
    popup = tk.Tk()
    popup.wm_title("!")
    label = tk.Label(popup, text=inf_, font=('arial', 12))
    label.pack(side="top", fill="x", pady=10)
    but_ = tk.Button(popup, text="Ok", command=popup.destroy)
    but_.pack()
    popup.mainloop()


def back_to_main(root):
    root.destroy()
    main()


def create_header(root):
    lbl_name = tk.Label(root, text="input book name", width=20, height=1)
    lbl_name.grid(row=1, column=0, sticky='nw')
    lbl_author = tk.Label(root, text="input book author", width=20, height=1)
    lbl_author.grid(row=1, column=1, sticky='nw')
    lbl_year = tk.Label(root, text="input book year", width=20, height=1)
    lbl_year.grid(row=1, column=2, sticky='nw')
    lbl_desc = tk.Label(root, text="input book description", width=24, height=1)
    lbl_desc.grid(row=1, column=3, sticky='nw')


def add_books(root):
    root.destroy()
    root = tk.Tk()
    root.title('Add book')

    button_back = tk.Button(root, text='Back to main', width=12, height=1,
                            font=('arial', 16, 'bold'), command=lambda: back_to_main(root))
    button_back.grid(row=0, column=0, sticky='nw')
    create_header(root)
    book_name_text = tk.Text(root, width=20, height=2)
    book_name_text.grid(row=2, column=0, sticky='nw')
    book_author_text = tk.Text(root, width=20, height=2)
    book_author_text.grid(row=2, column=1, sticky='nw')
    book_year_text = tk.Text(root, width=20, height=2)
    book_year_text.grid(row=2, column=2, sticky='nw')
    book_desc_text = tk.Text(root, width=24, height=2)
    book_desc_text.grid(row=2, column=3, sticky='nw')

    button_add = tk.Button(root, text='Add book', width=12, height=1,
                           font=('arial', 16, 'bold'), command=lambda: lib_append(book_name_text,
                                                                                  book_author_text,
                                                                                  book_year_text,
                                                                                  book_desc_text))
    button_add.grid(row=3, column=0, sticky='nsew')

    root.mainloop()


def edit_screen(root, name_, auth_, year_, desc_):
    root.destroy()
    root = tk.Tk()
    root.title('enter the new values')
    button_back = tk.Button(root, text='Back to main', width=12, height=1,
                            font=('arial', 16, 'bold'), command=lambda: back_to_main(root))
    button_back.grid(row=0, column=0, sticky='nw')
    create_header(root)
    book_name_text = tk.Text(root, width=20, height=2)
    book_name_text.grid(row=2, column=0, sticky='nw')
    book_name_text.insert('end-1c', name_)
    book_author_text = tk.Text(root, width=20, height=2)
    book_author_text.grid(row=2, column=1, sticky='nw')
    book_author_text.insert('end-1c', auth_)
    book_year_text = tk.Text(root, width=20, height=2)
    book_year_text.grid(row=2, column=2, sticky='nw')
    book_year_text.insert('end-1c', year_)
    book_desc_text = tk.Text(root, width=24, height=2)
    book_desc_text.grid(row=2, column=3, sticky='nw')
    book_desc_text.insert('end-1c', desc_)

    button_add = tk.Button(root, text='Edit entry', width=12, height=1,
                           font=('arial', 16, 'bold'), command=lambda: change_entry(root, book_name_text,
                                                                                    book_author_text,
                                                                                    book_year_text,
                                                                                    book_desc_text,
                                                                                    name_, auth_, year_, desc_))
    button_add.grid(row=3, column=0, sticky='nsew')


def search_books(root, show_lib):
    full_lib = import_func()
    root.destroy()
    root = tk.Tk()
    root.title('View books')
    main_frame = tk.Frame(root)
    main_frame.pack()
    button_back = tk.Button(main_frame, text='Back to main', width=12, height=1,
                            font=('arial', 16, 'bold'), command=lambda: back_to_main(root))
    button_back.grid(row=0, column=0, sticky='nw')
    create_header(main_frame)
    book_name_text = tk.Text(main_frame, width=24, height=2)
    book_name_text.grid(row=2, column=0, sticky='nw')
    book_author_text = tk.Text(main_frame, width=24, height=2)
    book_author_text.grid(row=2, column=1, sticky='nw')
    book_year_text = tk.Text(main_frame, width=24, height=2)
    book_year_text.grid(row=2, column=2, sticky='nw')
    book_desc_text = tk.Text(main_frame, width=28, height=2)
    book_desc_text.grid(row=2, column=3, sticky='nw')

    button_search = tk.Button(main_frame, text='search book', width=12, height=1,
                              font=('arial', 16, 'bold'),
                              command=lambda: lib_filter(root,
                                                         book_name_text.get("1.0", 'end-1c'),
                                                         book_author_text.get("1.0", 'end-1c'),
                                                         book_year_text.get("1.0", 'end-1c'),
                                                         book_desc_text.get("1.0", 'end-1c')))
    button_search.grid(row=3, column=0, sticky='nw')
    button_search = tk.Button(main_frame, text='clear search', width=12, height=1,
                              font=('arial', 16, 'bold'), command=lambda: search_books(root, full_lib))
    button_search.grid(row=3, column=1, sticky='nw')

    table_frame = tk.Frame(root)
    canvas = tk.Canvas(table_frame)
    yscrollbar = tk.Scrollbar(table_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=yscrollbar.set)

    for rw in range(len(show_lib)):
        addition_ = tk.Text(scrollable_frame, width=3, height=2)
        addition_.grid(row=rw, column=0)
        addition_.insert('end-1c', rw + 1)
        for cl in range(len(show_lib[rw])):
            addition_ = tk.Text(scrollable_frame, width=24 if cl == 3 else 16, height=2)
            addition_.grid(row=rw, column=1 + cl)
            addition_.insert('end-1c', show_lib[rw][cl])
        addition_ = tk.Button(scrollable_frame, text='Edit', width=3, height=2,
                              command=lambda r=rw: edit_screen(root,
                                                               show_lib[r][0],
                                                               show_lib[r][1],
                                                               show_lib[r][2],
                                                               show_lib[r][3]))
        addition_.grid(row=rw, column=5)
        addition_ = tk.Button(scrollable_frame, text='Remove', width=6, height=2,
                              command=lambda r=rw: remove_entry(root,
                                                                show_lib[r][0],
                                                                show_lib[r][1],
                                                                show_lib[r][2],
                                                                show_lib[r][3]))
        addition_.grid(row=rw, column=6)

    table_frame.pack(fill="both")
    canvas.pack(side="left", fill="both", expand=True)
    yscrollbar.pack(side="right", fill="y")
    # scrollbar.grid(column=7, row=0, rowspan=6)

    root.mainloop()


def main():
    full_lib = import_func()
    root = tk.Tk()
    root.title('Book library')

    button1 = tk.Button(root, text='Add Book', width=20, height=1,
                        font=('arial', 16, 'bold'), command=lambda: add_books(root))
    button1.grid(row=1, column=0, sticky='nsew')
    button2 = tk.Button(root, text='Search Books', width=20, height=1,
                        font=('arial', 16, 'bold'), command=lambda: search_books(root, full_lib))
    button2.grid(row=2, column=0, sticky='nsew')
    root.mainloop()
