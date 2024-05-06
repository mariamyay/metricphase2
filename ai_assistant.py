# -*- coding: utf-8 -*-
"""
Created on Mon May  6 19:37:56 2024

@author: Mariam
"""

import openai
import json
from vectordb import vector_db
openai.api_key = input("Enter your OpenAI API key: ")

class Assistant:
    def __init__(self, file_path):
        self.client = openai.OpenAI()
        self.file = self._upload_file(file_path)
        self.assistant = self._create_assistant()
        self.thread = self._create_thread()
        self.vector_db = vector_db

    def _upload_file(self, file_path):
        file = self.client.files.create(
            file=open(file_path, "rb"),
            purpose='assistants'
        )
        return file

    def _create_assistant(self):
        return self.client.beta.assistants.create(
            name="Assistant",
            instructions="You are a Q/A chatbot, answering questions based on the uploaded file to provide the best response to the user.",
            model="gpt-4-1106-preview",
            tools=[{"type": "retrieval",
                    "config": {
                        "timeout": 10,
                        "max_memory": "512MB"
                    }}],
            description="A chatbot that returns json based on the uploaded file.",
            file_ids=[self.file.id]
        )
    
    def ask_question(self, prompt):
       response = openai.Completion.create(
           engine="text-davinci-003",
           prompt=prompt,
           max_tokens=100
       )
       return response.choices[0].text.strip()

    def run_assistant(self):
        keep_asking = True
        while keep_asking:
            prompts = [
                "What is the name of the VC?",
                "What are the contact details of the VC?",
                "What industries does the VC invest in?",
                "What investment rounds does the VC participate in or lead?"
                ]
            vc_data = {}

            for prompt in prompts:
               user_question = self.ask_question(prompt)
               vc_data[prompt] = user_question
            with open('vc_data.json', 'w') as json_file:
                json.dump(vc_data, json_file)

            print("VC data has been saved to 'vc_data.json'.")
            vector_representation = self.convert_to_vector(vc_data)
            self.vector_db.add_vector(vector_representation)
            
            ask = input("Do you want to paste another URL? (yes/no)")
            keep_asking = ask.lower() == "yes"
        print("Thank you for using the Assistant. Have a great day!")
    
    
    def convert_to_vector(self, vc_data):
        vector_representation = [
            len(vc_data["What is the name of the VC?"]),
            len(vc_data["What are the contact details of the VC?"]),
            len(vc_data["What industries does the VC invest in?"]),
            len(vc_data["What investment rounds does the VC participate in or lead?"])
        ]
        return vector_representation
      

