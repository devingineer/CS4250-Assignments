import matplotlib.pyplot as plt
import sys
import os

directory = sys.argv[1]
docNum = sys.argv[2]

lines = 0
words = {}
frequency = {}

for fileName in os.listdir(directory):
    with open(directory + '\\' + fileName, 'r') as file:
        for line in file:
            line = line.strip()
            lines += 1
            if line in words.keys():
                words[line] += 1
            else:
                words[line] = 1

frequency = dict(sorted(words.items(),
                        key = lambda x: x[1],
                        reverse = True
                        )
                )

freq = []
i = 0

file_path = "Words" + docNum + ".csv"
with open(file_path, 'w') as file:
    for element in frequency.values():
        if i < 50:
            outText = str(list(frequency.keys())[i]) + ", frequency : " + str(element) + ", r: " + str(i+1) + ", Pr(%): "+ str("%.4f" % (list(frequency.values())[i]/lines)) + ", rPr: "+ str("%.4f" % ((i+1) * list(frequency.values())[i]/lines) + "\n")
            print(outText)
            file.write(outText)
        i += 1
        freq.append(element)



#zipf distribution
Zipf = [None]
Zipf += [.1/x for x in range(1, len(freq))]
plt.plot(Zipf, label = 'Zipf', ls = ':')

Prob = [None]
Prob += [freq[x] / lines for x in range(len(freq))]
plt.plot(Prob, label = "Crawl" + str(docNum), color = 'blue')

plt.xscale('log')
plt.yscale('log')

plt.xlabel('Rank')
plt.ylabel('Probability')
plt.title("Zipf's law for " + "Crawl" + str(docNum))
plt.legend()

plt.show()
