import timeit
import csv #For Task5

arr = [123, 111, 92, 77, 52, 25, 5, 1]
arr2 = [123, 111, 92, 77, 52, 25, 5, 1]
target = 10

#Task 1
def search_rec(arr, x, zero=0, end=len(arr)):
    if end >= zero:
        mid = (end+zero) // 2

        if arr[mid] == x:
            return mid
        
        elif arr[mid] > x:
            return search_rec(arr, x, zero, mid-1)

        else:
            return search_rec(arr, x, mid+1, end)
    
    else:
        return -1 #Element not found, handle outside func
    

def search(arr,x):
    zero = 0
    end = len(arr) - 1
    #Can initialize mid, but not neccesary in python
    while zero <= end:
        mid = (zero + end) // 2 #Floor division
        if arr[mid] < x:
            zero = mid + 1
        elif arr[mid] > x:
            end = mid -1
        else:
            return mid
    return -1 #Element not found, handle outside func



def measure_time(function,a,b,repetitions): #For below lcp functions
    total_time = 0
    for _ in range(repetitions):
        start_time = timeit.default_timer()
        function(a,b)
        end_time = timeit.default_timer()
        elapsed_time = end_time - start_time
        total_time += elapsed_time

    average_time = total_time / repetitions
    return average_time


repetitions = 10

time_ite = measure_time(search, arr, target, repetitions)
time_rec = measure_time(search_rec, arr, target, repetitions)

#print(f"Time taken on iterative: {time_ite}")
#print(f"Time taken on recursive: {time_rec}")

def bubble_sort(arr):
    n = len(arr)
    counter = 0
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                counter += 1
                print("Current array at stage", counter, ":", arr)
    return arr

def insert_sort(arr):
    for i in range(1, len(arr)):
        x = arr[i]

        j = i - 1
        while j >= 0 and x < arr[j]:
            arr[j+1] = arr[j]
            j -= 1
        arr[j+1] = x
        print("Current array at stage", i, ":", arr)
    return arr

"""
print("Bubble sort visualization :")
bubble_sort(arr)
print("\n")
print(arr)
print("\nInsert sort visualization :")
insert_sort(arr2)
print(f"\n{arr2}")
"""

def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        start = arr[:mid]
        end = arr[mid:]
        merge_sort(start)
        merge_sort(end)
        i = j = k = 0

        while i < len(start) and j < len(end):
            if start[i] < end[j]:
                arr[k] = start[i]
                i += 1
            else:
                arr[k] = end[j]
                j += 1
            k += 1
        
        while i < len(start):
            arr[k] = start[i]
            i += 1
            k += 1
        
        while j < len(end):
            arr[k] = end[j]
            j += 1
            k +=1
    return arr


def median_of_three(arr, low, high):
    mid = (low + high) // 2
    if arr[low] > arr[mid]:
        arr[low], arr[mid] = arr[mid], arr[low]
    if arr[low] > arr[high]:
        arr[low], arr[high] = arr[high], arr[low]
    if arr[mid] > arr[high]:
        arr[mid], arr[high] = arr[high], arr[mid]
    return mid

def partition(arr, low, high):
    pivot_index = median_of_three(arr, low, high)
    pivot = arr[pivot_index]
    arr[high], arr[pivot_index] = arr[pivot_index], arr[high]  # Move pivot to the end
    i = low - 1
    
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def quicksort(arr, low, high):
    if low < high:
        # Partitioning index, arr[p] is now at right place
        pi = partition(arr, low, high)

        # Separately sort elements before partition and after partition
        quicksort(arr, low, pi)
        quicksort(arr, pi + 1, high)

"""
print(f"Unsorted mergesort: {arr}")
merge_sort(arr)
print(f"Sorted mergesort: {arr}\n")

print(f"Unsorted quicksort: {arr2}")
high = len(arr2)
quicksort(arr2, 0, high-1)
print(f"Sorted quicksort: {arr2}")
"""

def shell_sort(arr):
    n = len(arr)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j-gap] > temp:
                arr[j] = arr[j-gap]
                j -= gap
            arr[j] = temp
        gap //= 2
    return arr

def heapify(arr, n, i):
    largest = i  # Initialize largest as root
    left = 2 * i + 1
    right = 2 * i + 2

    # Check if left child exists and is greater than root
    if left < n and arr[left] > arr[largest]:
        largest = left

    # Check if right child exists and is greater than largest so far
    if right < n and arr[right] > arr[largest]:
        largest = right

    # Change root, if needed
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]  # Swap
        # Heapify the affected sub-tree
        heapify(arr, n, largest)

def heapsort(arr):
    n = len(arr)

    # Build a max heap. n//2 -1 is last non-leaf node, -1 is heap root, step is -1. To change from asc to desc, change step to +1.
    for i in range(n // 2 - 1, -1):
        heapify(arr, n, i)

    # Extract elements one by one
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]  # Swap
        heapify(arr, i, 0)

"""" 
print(f"Unsorted shellsort: {arr}")
shell_sort(arr)
print(f"Sorted shellsort: {arr}\n")

print(f"Unsorted heapsort: {arr2}")
heapsort(arr2)
print(f"Sorted heapsort: {arr2}\n")
"""


import csv

import csv
import time

def heapify_csv(arr, n, i, key):
    largest = i  # Initialize largest as root
    left = 2 * i + 1
    right = 2 * i + 2

    # Check if left child exists and is greater than root
    if left < n and int(arr[left][key]) > int(arr[largest][key]):
        largest = left

    # Check if right child exists and is greater than largest so far
    if right < n and int(arr[right][key]) > int(arr[largest][key]):
        largest = right

    # Change root, if needed
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]  # Swap
        # Heapify the affected sub-tree
        heapify_csv(arr, n, largest, key)


def heapsort_csv(arr, key):
    n = len(arr)

    # Build a max heap. n//2 - 1 is last non-leaf node, -1 is heap root, step is -1.
    for i in range(n // 2 - 1, -1, -1):
        heapify_csv(arr, n, i, key)

    # Extract elements one by one
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]  # Swap
        heapify_csv(arr, i, 0, key)

def insertion_sort(arr, key):
    for i in range(1, len(arr)):
        key_item = arr[i]
        j = i - 1
        while j >= 0 and int(arr[j][key]) > int(key_item[key]):
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key_item


def quicksort(arr, key, low, high):
    if low < high:
        # Partition the array
        pi = partition(arr, key, low, high)

        # Recursively sort elements before and after partition
        quicksort(arr, key, low, pi - 1)
        quicksort(arr, key, pi + 1, high)


def partition(arr, key, low, high):
    pivot = int(arr[high][key])
    i = low - 1
    for j in range(low, high):
        if int(arr[j][key]) < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def hybrid_sort(arr, key, threshold=10):
    if len(arr) < threshold:
        insertion_sort(arr, key)
    else:
        quicksort(arr, key, 0, len(arr) - 1)








def get_median_min_max_salaries(csv_file):
    with open(csv_file, 'r', newline='') as file:
        reader = csv.DictReader(file)
        salaries = [int(row['salary_in_usd']) for row in reader]

    # Calculate median
    n = len(salaries)
    if n % 2 == 0:
        median = salaries[n // 2 - 1] #Arbitrary decision
    else:
        median = salaries[n // 2]

    # Minimum salary is the first element
    min_salary = salaries[0]

    # Maximum salary is the last element
    max_salary = salaries[-1]

    return median, min_salary, max_salary


# Read CSV file and sort it using heapsort & hybrid
csv_file = '/home/auxi/Desktop/Algoritmit/algoritmit/Exercise6/jobs_in_data.csv'
sorted_csv_file = '/home/auxi/Desktop/Algoritmit/algoritmit/Exercise6/sorted_csv_file.csv'
hybrid_csv_file = '/home/auxi/Desktop/Algoritmit/algoritmit/Exercise6/hybrid_csv_file.csv'

# Open input and output CSV files for heapsort
with open(csv_file, 'r', newline='') as infile, open(sorted_csv_file, 'w', newline='') as outfile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    # Process CSV rows in chunks
    key = 'salary_in_usd'
    chunk_size = 1000  # Adjust as needed
    while True:
        rows = [row for _, row in zip(range(chunk_size), reader)]
        if not rows:
            break
        
        heap_start_time = time.time() #Time the process
        heapsort_csv(rows, key)
        heap_end_time = time.time()

        for row in rows:
            writer.writerow(row)

# Open input and output CSV files for hybrid
with open(csv_file, 'r', newline='') as infile, open(hybrid_csv_file, 'w', newline='') as outfile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    # Process CSV rows in chunks
    key = 'salary_in_usd'
    chunk_size = 1000  # Adjust as needed
    while True:
        rows = [row for _, row in zip(range(chunk_size), reader)]
        if not rows:
            break
        
        hybrid_start_time = time.time() #Time the process
        hybrid_sort(rows, key)
        hybrid_end_time = time.time()

        for row in rows:
            writer.writerow(row)


heap_exec_time = heap_end_time - heap_start_time
hybrid_exec_time = hybrid_end_time - hybrid_start_time


umedian, umin, umax = get_median_min_max_salaries(csv_file)
print(f"In the unsorted CSV file, median : {umedian}. Minimum: {umin}. Maximum: {umax}\n")

median, minimum, maximum = get_median_min_max_salaries(sorted_csv_file)
print("CSV file sorted successfully using heap sort.\n")
print(f"In the heap sorted CSV file, median : {median}. Minimum: {minimum}. Maximum: {maximum}. Time taken: {heap_exec_time}s\n")


hmed, hmin, hmax = get_median_min_max_salaries(hybrid_csv_file)
print("CSV file sorted successfully using hybrid sorting.\n")
print(f"In the hybrid sorted CSV file, median : {hmed}. Minimum: {hmin}. Maximum: {hmax}. Time taken: {hybrid_exec_time}s")