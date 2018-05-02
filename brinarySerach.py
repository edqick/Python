'''
二分查找
'''
def brinarySerach(arr,target,start,end):
    middle = (start + end) // 2
    if middle < start or middle >= end:
        return -1
    elif arr[middle] < target:
        return brinarySerach(arr,target,middle+1,end)
    elif arr[middle] > target:
        return brinarySerach(arr,target,start,middle-1)
    else:
        return middle

tar = -5
arr = [1,2,3,4,5,6,7,8,9,10]
print(brinarySerach(arr,tar,0,len(arr)))