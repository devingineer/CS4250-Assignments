import matplotlib.pyplot as plt
import sys
import math
import os

directory = sys.argv[1]
docNum = sys.argv[2]

uniqueWords = []
vocabulary = []

for fileName in os.listdir(directory):
    with open(directory + '\\' + fileName, 'r') as file:
        for line in file:
            if line not in uniqueWords:
                uniqueWords.append(line)
            vocabulary.append(len(uniqueWords))


#heaps vals
index1 = (int)(len(vocabulary) * .3)
index2 = (int)(len(vocabulary) * .65)
B = (math.log(vocabulary[index1], 10) - math.log(vocabulary[index2], 10)) / (math.log(index1, 10) - math.log(index2, 10))
k = round(vocabulary[index1] / (pow(index1, B)), 3)
B = round(B, 3)

print("Corpus: ", len(vocabulary), " UniqueWords: ", len(uniqueWords))
print("Heaps Values, Beta: ", B, "K: ", k)

#heaps plot
Heaps = [k * pow(x, B) for x in range(len(vocabulary))]
lbl = "Heaps " + str(k) + ", " + str(B)
plt.plot(Heaps, label = lbl, ls = ':')

plt.plot(vocabulary, label = "Crawl" + str(docNum), color = 'blue')

plt.xlabel('Words in Collection')
plt.ylabel('Words in Vocabulary')
plt.title("Vocabular growth for Crawl" + str(docNum))
plt.legend()

plt.show()
