# projects/services/openai_service.py
from django.conf import settings
from openai import OpenAI

class OpenAITaggingService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def generate_tags(self, title: str, description: str) -> list[str]:
        """
        Generate tags for a project using OpenAI's API
        
        Args:
            title: Project title
            description: Project description
            
        Returns:
            List of generated tags
        """
        try:
            prompt = f"""
            Based on the following project title and description, generate up to 5 relevant tags.
            Format the response as a comma-separated list of lowercase tags.
            
            Title: {title}
            Description: {description}
            
            Tags should be:
            - Relevant to AI, machine learning, and data science
            - Single words or short phrases (max 2-3 words)
            - All lowercase
            - No special characters
            - No hashtags
            
            Example format: machine learning, nlp, computer vision, tensorflow, data analysis
            """

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that generates relevant tags for AI and machine learning projects."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.5
            )
            
            # Extract tags from response
            tags = response.choices[0].message.content.strip()
            return tags
            
        except Exception as e:
            print(f"Error generating tags: {str(e)}")
            return ""