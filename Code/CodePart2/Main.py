import os
from nltk.stem import PorterStemmer

from Tokenizer import Tokenize
stemmer = PorterStemmer()

#make sure to update the target repo later
directory = os.path.join(os.getcwd(), r'Code\CodePart2\TargetRepoExample')

outputDir = "output"
os.makedirs(outputDir, exist_ok=True)


for filename in os.listdir(directory):
    file_path = os.path.join(directory, filename)
    
    # Check if it's an HTML file
    if file_path.endswith('.html'):
        with open(file_path, 'r', encoding='utf-8') as handle:
                #Tokenize
                tokenizedWords = Tokenize(handle.read())

                #stem
                with open(f"Output/OutputPart2/{filename}.StemmedOutput.txt", "w", encoding="utf-8") as file:
                    for word in tokenizedWords: 
                        output = stemmer.stem(word)
                        file.write(f"{output}\n")
                        # print(f"{word} ---> {output}")
                


