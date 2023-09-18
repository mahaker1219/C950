def merge(list_a, list_b):
    i, j = 0, 0
    m, n = len(list_a), len(list_b)
    output_list = []

    while i < m and j < n:
        if list_a[i][1] <= list_b[j][1]:  # Compare timestamps (second element in each sublist)
            output_list.append(list_a[i])
            i += 1
        else:
            output_list.append(list_b[j])
            j += 1

    while i < m:
        output_list.append(list_a[i])
        i += 1

    while j < n:
        output_list.append(list_b[j])
        j += 1

    return output_list


def merge_three(list_a, list_b, list_c):
    output_list = merge(list_a, list_b)
    return merge(output_list, list_c)
