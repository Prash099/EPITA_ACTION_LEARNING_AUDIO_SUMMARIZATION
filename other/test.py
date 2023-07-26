from Scripts.Backend.URLScraper import URLScraper

scraper = URLScraper()
url = "https://en.wikipedia.org/wiki/Dish-bearers_and_butlers_in_Anglo-Saxon_England"
extracted_url_text = scraper.extract_text_from_website(url)
print("Website : \n", url)
# print("********************************************************")
# print("Extracted Text : \n", extracted_url_text)

# from Scripts.Backend.PassageSummarizer import PassageSummarizer

# summariser = PassageSummarizer()

# text = "The tower is 324 metres (1,063 ft) tall, about the same height as an 81-storey building, and the tallest structure in Paris. Its base is square, measuring 125 metres (410 ft) on each side. During its construction, the Eiffel Tower surpassed the Washington Monument to become the tallest man-made structure in the world, a title it held for 41 years until the Chrysler Building in New York City was finished in 1930. It was the first structure to reach a height of 300 metres. Due to the addition of a broadcasting aerial at the top of the tower in 1957, it is now taller than the Chrysler Building by 5.2 metres (17 ft). Excluding transmitters, the Eiffel Tower is the second tallest free-standing structure in France after the Millau Viaduct."
# print("Length of text before : ", len(extracted_url_text))

# summary = summariser.generate_summary_passages(extracted_url_text)
# print("Length of summary : ", len(summary))
# print("********************************************************")
# print("\n NOW PRINING SUMMARY : \n")
# print("********************************************************")
# print(summary)



from Scripts.Backend.QASummarizer import QASummarizer

summariser = QASummarizer()

# text = "The tower is 324 metres (1,063 ft) tall, about the same height as an 81-storey building, and the tallest structure in Paris. Its base is square, measuring 125 metres (410 ft) on each side. During its construction, the Eiffel Tower surpassed the Washington Monument to become the tallest man-made structure in the world, a title it held for 41 years until the Chrysler Building in New York City was finished in 1930. It was the first structure to reach a height of 300 metres. Due to the addition of a broadcasting aerial at the top of the tower in 1957, it is now taller than the Chrysler Building by 5.2 metres (17 ft). Excluding transmitters, the Eiffel Tower is the second tallest free-standing structure in France after the Millau Viaduct."
print("Length of text before : ", len(extracted_url_text))

summary = summariser.summarize_qa_texts(extracted_url_text)
print("Length of summary : ", len(summary))
print("********************************************************")
print("\n NOW PRINING SUMMARY : \n")
print("********************************************************")
print(summary)