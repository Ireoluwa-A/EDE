import math

def isNarcissistic(n): 
    n = abs(n)
    noOfDigits = getDigitCount(n)
    sum = 0
    while n > 0: 
        currDigit = n % 10
        sum += currDigit ** noOfDigits
        n //= 10
    return sum == n

def nthNearlyNarcissistic(n,r): 

    guess = 0
    result = 0
    found = 0
    while found < n:
        guess += 1
        if isNarcissistic(guess): 
            found += 1
            if n - guess < r:
                result = guess
    return guess 


def getDigitCount(n):
    return 1 + int(math.log10(abs(n)))

def main():
    #print(nthNearlyNarcissistic(14,0))
main()