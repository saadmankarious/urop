from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize the VADER sentiment intensity analyzer
analyzer = SentimentIntensityAnalyzer()

# Example text
text = "he looks so cute with his head poking out!! he also has a rattle in his head and crinkly feet which is good for stimming during our sessions. :) have a good monday everyone! "

# Analyze the sentiment
sentiment = analyzer.polarity_scores(text)

# Print the results
print(sentiment)
