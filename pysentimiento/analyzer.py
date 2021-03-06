import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from torch.nn import functional as F

class SentimentAnalyzer:
    def __init__(self, model_name="finiteautomata/beto-sentiment-analysis"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.id2label = self.model.config.id2label

    def predict(self, sentence):
        idx = torch.LongTensor(self.tokenizer.encode(sentence)).view(1, -1)
        output = self.model(idx)
        max_idx = torch.argmax(output.logits).item()
        return self.id2label[max_idx]

    def predict_probas(self, sentence):
        idx = torch.LongTensor(self.tokenizer.encode(sentence)).view(1, -1)
        output = self.model(idx)
        probs = F.softmax(output.logits, dim=1).view(-1)
        return {self.id2label[i]:probs[i].item() for i in self.id2label}
