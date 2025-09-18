import google.generativeai as genai
import os
import cv2
from PIL import Image
import numpy as np



def extract_text_image(image_path):
  file_bytes = np.asarray(bytearray(image_path.read()),dtype=np.uint8)
  image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

  #image = cv2.imread(image_path)

  image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # to convert to RGB 
  image_grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # to grey
  _, image_bw = cv2.threshold(image_grey, 150,255, cv2.THRESH_BINARY) # to convert to black and white

  final_image = Image.fromarray(image_bw)

  key = os.getenv('GOOGLE_API_KEY')
  genai.configure(api_key='AIzaSyCA2uu5GaTNoNUXeelsTv0G4rgzzjRL_Zs')

  model = genai.GenerativeModel('gemini-2.5-flash-lite')

  prompt = ''' You act as an OCR application on the given image and text and extract the text 
  from it. give only the text as output, do not give any other explanation or description.

  '''
  response = model.generate_content([prompt, final_image])
  output_text = response.text
  return output_text