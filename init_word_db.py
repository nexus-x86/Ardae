import csv

def word_list(n):
    file = open('unigram_freq.csv')

    csvreader = csv.reader(file)

    words = []

    next(csvreader)

    cnt = 0
    for row in csvreader:
        if cnt > n: break
        words.append(row[0])
        cnt += 1
    
    return words
