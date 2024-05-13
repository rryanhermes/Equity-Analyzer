import tensorflow as tf
from transformers import AutoTokenizer, TFLayoutLMForQuestionAnswering
from datasets import load_dataset

tokenizer = AutoTokenizer.from_pretrained("impira/layoutlm-document-qa", add_prefix_space=True)
model = TFLayoutLMForQuestionAnswering.from_pretrained("impira/layoutlm-document-qa", revision="1e3ebac")

dataset = load_dataset("nielsr/funsd", split="train")
example = dataset[0]
question = "what's his name?"
words = example["words"]
boxes = example["bboxes"]

encoding = tokenizer(
    question.split(), words, is_split_into_words=True, return_token_type_ids=True, return_tensors="tf"
)
bbox = []
for i, s, w in zip(encoding.input_ids[0], encoding.sequence_ids(0), encoding.word_ids(0)):
    if s == 1:
        bbox.append(boxes[w])
    elif i == tokenizer.sep_token_id:
        bbox.append([1000] * 4)
    else:
        bbox.append([0] * 4)
encoding["bbox"] = tf.convert_to_tensor([bbox])

word_ids = encoding.word_ids(0)
outputs = model(**encoding)
loss = outputs.loss
start_scores = outputs.start_logits
end_scores = outputs.end_logits
start, end = word_ids[tf.math.argmax(start_scores, -1)[0]], word_ids[tf.math.argmax(end_scores, -1)[0]]
print(" ".join(words[start : end + 1]))