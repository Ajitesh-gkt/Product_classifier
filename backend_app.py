from fastapi import FastAPI, File, UploadFile
from PIL import Image
import torch
import torchvision.transforms as transforms
import torch.nn as nn
import io
from weak_model import CNNModel
import json

# Load the category mapping from JSON
with open("Category_mapper.json", "r") as f:
    category_mapping = json.load(f)

IMAGE_SIZE = (224,224)

app = FastAPI()

model = CNNModel()
model.load_state_dict(torch.load('weak_cnn_model_state_dict.pth'))
model.eval()

# Image transformations
transform = transforms.Compose([
    transforms.Resize(IMAGE_SIZE),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
])

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert('RGB')

        image = transform(image).unsqueeze(0)

        with torch.no_grad():
            outputs = model(image)
            _, predicted = torch.max(outputs.data, 1)
            predicted_id = int(predicted.item())
        
        category_name = category_mapping.get(str(predicted_id), "Unknown")

        return{
            "predicted_id": predicted_id,
            "category_name": category_name
        }
    except Exception as e:
        return {
            "error": str(e)
        }

        
