from transformers import PegasusForConditionalGeneration
from transformers import PegasusTokenizer
from transformers import pipeline
from .Preprocessing_eng_custom import Custom_preprocessing

class Summarize(object):
    
    def __init__(self):
        self.tokenizer = PegasusTokenizer.from_pretrained("google/pegasus-xsum")
        self.model = PegasusForConditionalGeneration.from_pretrained("google/pegasus-xsum")
        self.custom_preprocessing = Custom_preprocessing()      

    def summarize(self, target_text):
        target_text = self.custom_preprocessing.preprocessing_only_text(target_text=target_text)
        tokens = self.tokenizer(target_text, truncation=True, padding="longest", return_tensors="pt")
        summary = self.model.generate(**tokens, min_length = 30, max_length = 80)
        return self.tokenizer.decode(summary[0])

    def title(self, target_text):
        tokens = self.tokenizer(target_text, truncation=True, padding="longest", return_tensors="pt")
        summary = self.model.generate(**tokens)
        return self.tokenizer.decode(summary[0])

