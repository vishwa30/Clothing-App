import openai
import json

class ClothingDescription:
    def __init__(self, api_key):
        self.client = openai.OpenAI(api_key=api_key)

    def describe_clothing(self, base64_image, prompt):
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                { 
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt,
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                                "detail": "high",
                            },
                        },
                    ],
                }
            ],
            max_tokens=250,
        )

        response_content = response.choices[0].message.content.strip('```json\n').strip('\n```')
        response_json = json.loads(response_content)

        return response_json

