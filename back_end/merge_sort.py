def merge_sort(arr):
    if len(arr) > 1:

        # Finding the mid of the array
        mid = len(arr) // 2

        # Dividing the array elements
        L = arr[:mid]

        # into 2 halves
        R = arr[mid:]

        # Sorting the first half
        merge_sort(L)

        # Sorting the second half
        merge_sort(R)

        i = j = k = 0

        # Copy data to temp arrays L[] and R[]
        while i < len(L) and j < len(R):
            if L[i] <= R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        # Checking if any element was left
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1


def run_merge(records):
    list_of_numbers = []
    for record in records:
        list_of_numbers.append(records[record])

    merge_sort(list_of_numbers)

    final_sorted = []
    for number in list_of_numbers:
        final_sorted.append(list(records.keys())[list(records.values()).index(number)])

    final_leaderboard = final_sorted[::-1]
    final_score = list_of_numbers[::-1]

    rows = []
    rank = 1
    for i in range(len(final_score)):
        rows.append((rank, final_leaderboard[i], final_score[i]))
        rank += 1
    return rows


# run_merge({"Tristan": 4.6, "Nick": 2.5, "Andrej": 6.7, "Nathan": 3.2, "Henry": 5})