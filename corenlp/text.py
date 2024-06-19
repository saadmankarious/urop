from stanfordcorenlp import StanfordCoreNLP

# Initialize the StanfordCoreNLP object
nlp = StanfordCoreNLP('http://localhost', port=9000)

# Example text
text = "Stanford University is located in California. It is a great university."

# Perform various NLP tasks
print('Tokens:', nlp.word_tokenize(text))
print('Part of Speech:', nlp.pos_tag(text))
print('Named Entities:', nlp.ner(text))
print('Constituency Parsing:', nlp.parse(text))
print('Dependency Parsing:', nlp.dependency_parse(text))

# Close the StanfordCoreNLP object
nlp.close()
