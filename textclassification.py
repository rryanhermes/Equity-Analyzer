import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification

tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")

inputs = tokenizer("""

Tesla Inc. cut prices for many of its vehicles in the U.S., China and Europe over the weekend amid slumping sales, with the company’s shares under pressure in early trading on Monday.
On Friday, the EV maker cut prices for its Model Y, Model X and Model S vehicles in the U.S. by $2,000 each, and on Saturday it reduced the price of its Full Self-Driving driver-assistance mode in the U.S. by about a third, from $12,000 to $8,000.

""", return_tensors="pt")
with torch.no_grad():
    logits = model(**inputs).logits

predicted_class_id = logits.argmax().item()
model.config.id2label[predicted_class_id]

print(predicted_class_id)