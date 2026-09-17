from transformers import BlipProcessor, BlipForConditionalGeneration


class CaptionGenerator:

    def __init__(self):
        self.processor = BlipProcessor.from_pretrained(
            "Salesforce/blip-image-captioning-base"
        )
        self.model = BlipForConditionalGeneration.from_pretrained(
            "Salesforce/blip-image-captioning-base"
        )

    def generate_caption(self, image):
        inputs = self.processor(images=image, return_tensors="pt")
        output = self.model.generate(**inputs, max_new_tokens=50)
        return self.processor.decode(
            output[0],
            skip_special_tokens=True
        )
