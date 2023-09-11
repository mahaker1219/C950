def list_search(arr, term):
    for i in range(len(arr)):
        if arr[i] == term:
            return i
    return None
