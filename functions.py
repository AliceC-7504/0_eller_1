def maxSeq(arr): # Calculates max streak in sequence
    maxLength = 0
    for i in range(len(arr)):
        count = 0
        streak = True
        while streak == True:
            if i+count<len(arr):
                if arr[i]==arr[i+count]:
                    count = count+1
                else:
                    streak=False
            else:
                streak=False
        if count>maxLength:
            maxLength=count
    return maxLength

def seqs(arr): # Returns a list with amount of each streak, [amount with direct switch, 2 in a row, 3 in a row...]
    maxLength = maxSeq(arr)
    result = list()
    for i in range(maxLength):
        result.append(0)
    index = 0
    while index < len(arr):
        for j in range(maxLength):
            k=j+1
            if index+k<len(arr):
                if arr[index] != arr[index+k]:
                    result[j] = result[j]+1
                    index = index+k
                    break      
            else: 
                result[j] = result[j]+1
                index = index+maxLength
                break
    return result