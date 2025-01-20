import numpy as np
from keras.models import load_model
from ela import convert_to_ela_image
from PIL import Image

def prepare_image(fname):
    image_size = (128, 128)
    ela_image = convert_to_ela_image(fname, 90).resize(image_size)
    return np.array(ela_image).flatten() / 255.0

def predict_result(fname):
    model = load_model("trained_model.h5")
    class_names = ["Forged", "Authentic"]
    
    test_image = prepare_image(fname)
    test_image = test_image.reshape(-1, 128, 128, 3)
    
    y_pred = model.predict(test_image)
    y_pred_class = round(y_pred[0][0])
    
    prediction = class_names[y_pred_class]
    confidence = f"{(y_pred[0][0] * 100):0.2f}" if y_pred_class == 1 else f"{(1 - y_pred[0][0]) * 100:0.2f}"
    
    # Generate ELA image path for display
    ela_filename = fname.split("/")[-1].split(".")[0] + "_ela.png"
    ela_path = "static/uploads/" + ela_filename
    convert_to_ela_image(fname, 90).save(ela_path)
    
    return prediction, confidence, ela_filename
