import google.generativeai as genai
from PyPDF2 import PdfReader
import os
import os.path

apikey = secret_file

#file paths for folder directory and new folder directory
directory = r"user_uploads"
save_path =  r"textfiles"

#runs through every file in a directory
for name in os.listdir(directory):
    
    if name != ".gitkeep":
       
      with open(os.path.join(directory, name)) as f:
          #converting pdf to text
          reader = PdfReader(f"user_uploads/{name}")
          #finds the amount of pages in the pdf and creates a count to scroll through every page
          length_of_pdf = len(reader.pages)
          count = 0
          #creates text file in the TextFiles folder
          paths = name.replace(".pdf","")
          completePath = os.path.join(save_path,paths+'.txt')
          while count < length_of_pdf: 
            #goes through every page of the pdf and opens text file with absolute path and adds the content of every page to the 
            #text file
            file = open(completePath,"a")
            page_content = reader.pages[count].extract_text()
            file.write(page_content)
            file.close()
            count += 1

genai.configure(api_key=apikey)

# Set up the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 0,
  "max_output_tokens": 8192,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

convo = model.start_chat(history=[
])

csvpath = 'csvfiles'

#go through all the files in the folder and read them and put the syllabus into gemini ai
#gemini ai api response is requested to be returned as a csv 
#csv file is made and gemini ai response inputted 
for name in os.listdir(save_path):
    if name != ".gitkeep":
      with open(os.path.join(save_path, name)) as f:
        text = f.read()
        prompt = "give me the weighting and exact dates of all the assignements, tests or marked work in a python dictionary named after the course code in the syllabus file format with the coloumns Assignment,weight,date in YYYY-MM-DD: " + text
        convo.send_message(prompt)
        base_name, _ = os.path.splitext(name)  # Extract base name without .txt extension
        completePath = os.path.join(csvpath,base_name+'.csv')
        file = open(completePath,"w")
        file.write(convo.last.text)
        file.close()


