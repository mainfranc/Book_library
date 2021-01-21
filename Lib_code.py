import Interface_code as i_c


def import_func():
    result = []
    with open('Full_library.txt', 'r') as source_file:
        for rw in source_file.readlines():
            result.append(tuple(rw.split(';')))
    return result


def lib_append(name_, auth_, year_, desc_):
    full_lib = import_func()
    nm = name_.get("1.0", 'end-1c')
    auth = auth_.get("1.0", 'end-1c')
    yr = year_.get("1.0", 'end-1c')
    des = desc_.get("1.0", 'end-1c')
    if all([name_, auth_]):
        if not yr.isnumeric():
            i_c.po_pup("Please enter the year as number")
        else:
            full_lib.append((nm, auth, yr, des))
            name_.delete("1.0", 'end')
            auth_.delete("1.0", 'end')
            year_.delete("1.0", 'end')
            desc_.delete("1.0", 'end')
            with open('Full_library.txt', 'a') as source_file:
                if ';'.join((nm, auth, yr, des)) != '':
                    source_file.write(';'.join((nm, auth, yr, des)) + '\n')
    else:
        i_c.po_pup("Please fill book name and author fields")


def lib_filter(root, name_, auth_, year_, desc_):
    full_lib = quick_sort(import_func())
    lib_to_show = []
    for i in range(len(full_lib)):
        if all([name_ in full_lib[i][0] and auth_ in full_lib[i][1] and
                year_ in full_lib[i][2] and desc_ in full_lib[i][3]]):
            lib_to_show.append(full_lib[i])
    i_c.search_books(root, lib_to_show)


def change_entry(root, name_, auth_, year_, desc_, name_old, auth_old, year_old, desc_old):
    full_lib = quick_sort(import_func())
    nm = name_.get("1.0", 'end-1c')
    auth = auth_.get("1.0", 'end-1c')
    yr = year_.get("1.0", 'end-1c')
    des = desc_.get("1.0", 'end-1c')
    if all([name_, auth_]):
        if not yr.isnumeric():
            i_c.po_pup("Please enter the year as number")
        else:
            str_to_search = f'{name_old};{auth_old};{year_old};{desc_old}'
            join_lst = joined_list(full_lib)
            ind_ = binary_search(str_to_search, join_lst)
            full_lib[ind_] = (nm, auth, yr, des)
            with open("Full_library.txt", "w") as source_file:
                source_file.truncate(0)
                for line in full_lib:
                    source_file.write(';'.join(line))
            i_c.search_books(root, full_lib)
    else:
        i_c.po_pup("Please fill book name and author fields")


def remove_entry(root, name_, auth_, year_, desc_):
    full_lib = quick_sort(import_func())
    str_to_search = f'{name_};{auth_};{year_};{desc_}'
    join_lst = joined_list(full_lib)
    ind_ = binary_search(str_to_search, join_lst)
    full_lib.pop(ind_)
    with open("Full_library.txt", "w") as source_file:
        source_file.truncate(0)
        for line in full_lib:
            source_file.write(';'.join(line))

    i_c.search_books(root, full_lib)


def quick_sort(container):
    lst_less = []
    lst_equal = []
    lst_greater = []

    if len(container) > 1:
        base_elem = container[0]
        for elem in container:
            if elem < base_elem:
                lst_less.append(elem)
            elif elem == base_elem:
                lst_equal.append(elem)
            elif elem > base_elem:
                lst_greater.append(elem)
        return quick_sort(lst_less) + lst_equal + quick_sort(lst_greater)
    else:
        return container


def binary_search(elem, arr):
    if arr:
        # len_arr = len(arr)
        len_of_curr_diap = len(arr) // 2
        beg_diap = 0
        while elem != arr[beg_diap + len_of_curr_diap - 1] and len_of_curr_diap != 1:
            if elem > arr[beg_diap + len_of_curr_diap - 1]:
                beg_diap += len_of_curr_diap
            if not len_of_curr_diap % 2:
                len_of_curr_diap //= 2
            else:
                len_of_curr_diap = len_of_curr_diap // 2 + 1
        if arr[beg_diap] == elem:
            return beg_diap
        if arr[beg_diap + len_of_curr_diap] == elem:
            return beg_diap + len_of_curr_diap
        if arr[beg_diap + len_of_curr_diap - 1] == elem:
            return beg_diap + len_of_curr_diap - 1
    return None


def joined_list(lst):
    result = []
    for i in lst:
        result.append(';'.join(i))
    return result
