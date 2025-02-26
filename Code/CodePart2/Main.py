import os
import spacy

from Clean import CleanText

#change model depending on langauge?
nlp = spacy.load('en_core_web_sm')

#make sure to update the target repo later
directory = r'.\CS4250-Assignment1\Code\CodePart2\TargetRepoExample' 

for filename in os.listdir(directory):
    file_path = os.path.join(directory, filename)
    
    # Check if it's an HTML file
    if file_path.endswith('.html'):
        with open(file_path, 'r', encoding='utf-8') as handle:
                #clean text 
                cleanedText = CleanText(handle.read())

                #tokenize them using the model above
                doc = nlp(cleanedText)
                for token in doc:
                    print(token.text + "-->" + token.lemma_)


# #uncomment below to test
# text = """
#             <html>
# <body>

# <h1>My First Heading</h1>
# <p>My first paragraph.</p>

# </body>
# </html>
#             """
# print(CleanText(text))

# test = nlp("eat eating ate eaten")
# for token in test:
#     print(token.text + "-->" + token.lemma_)

