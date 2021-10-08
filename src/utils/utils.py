import ast


def split_bases(bases):
    clean_bases = []
    for base in bases:
        base = ast.literal_eval(base)
        clean_bases = clean_bases + base
    return clean_bases


def my_sort(bases_count, sorted_list, bases):
    if len(sorted_list) == 0:
        sorted_list.insert(0, bases_count[list(bases_count)[0]])
        bases.insert(0, list(bases_count)[0])
        bases_count.pop(list(bases_count)[0])
        return my_sort(bases_count, sorted_list, bases)
    for base in bases_count:
        for ct in range(0, len(sorted_list)):
            if sorted_list[ct] >= bases_count[base]:
                sorted_list.insert(ct, bases_count[base])
                bases.insert(ct, base)
                bases_count.pop(base)
                return my_sort(bases_count, sorted_list, bases)
    if len(bases_count) != 0:
        sorted_list.append(bases_count[list(bases_count)[0]])
        bases.append(list(bases_count)[0])
        bases_count.pop(list(bases_count)[0])
        return my_sort(bases_count, sorted_list, bases)
    return sorted_list, bases
