#Used to do part A of Text analysis
import matplotlib.pyplot as plt
import sys

fileName = sys.argv[1]

lines = 0
words = {}
frequency = {}

with open(fileName, 'r') as file:
    #calculates frequencies of all words in the stemmed doc
    for line in file:
        lines += 1
        if line in words.keys():
            words[line] += 1
        else:
            words[line] = 1

#sort frequencies
frequency = dict(sorted(words.items(),
                        key = lambda x: x[1],
                        reverse = True
                        )
                )

#Turn frequencies into an array and display some data
freq = []
i = 0
for element in frequency.values():
    if i < 100:
        print(list(frequency.keys())[i], 
            "freq : ", list(frequency.values())[i], 
            " r: ", i+1, 
            " Pr(%): ", "%.4f" % (list(frequency.values())[i]/lines), 
            "rPr: ", "%.4f" % ((i+1) * list(frequency.values())[i]/lines)
            )
    i += 1
    freq.append(element)

#zipf distribution
Zipf = [None]
Zipf += [.1/x for x in range(1, len(freq))]
plt.plot(Zipf, label = 'Zipf', ls = ':')

#stemmed doc zipf distribution
Prob = [None]
Prob += [freq[x] / lines for x in range(len(freq))]
plt.plot(Prob, label = fileName, color = 'blue')

plt.xscale('log')
plt.yscale('log')

plt.xlabel('Rank')
plt.ylabel('Probability')
plt.title("Zipf's law for " + fileName)
plt.legend()

plt.show()
