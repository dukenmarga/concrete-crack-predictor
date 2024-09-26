import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms.functional as func_transform
from PIL import ImageFile
from torchvision import transforms


def predict_concrete(img: ImageFile) -> str:
    model_path = "./concrete_crack_model.pth"
    inference_model = models.resnet18()
    num_ftrs = inference_model.fc.in_features
    inference_model.fc = nn.Linear(
        num_ftrs, 1
    )  # Match the checkpoint's fully connected layer (1 output)

    checkpoint = torch.load(model_path, map_location=torch.device("cpu"))
    inference_model.load_state_dict(checkpoint)

    inference_model.eval()

    # Apply the same transformations used during training (resize, normalize, etc.)
    transform = transforms.Compose(
        [
            transforms.ToPILImage(),
            transforms.ToTensor(),
            transforms.Normalize(
                (0.5, 0.5, 0.5), (0.5, 0.5, 0.5)
            ),  # Normalize to [-1, 1]
        ]
    )
    img_original = img
    img = func_transform.to_tensor(img_original)
    input_data = transform(img).unsqueeze(0)  # Add a batch dimension

    classification = {
        0: "No crack",
        1: "Crack",
    }

    with torch.no_grad():
        output = inference_model(input_data)

    # For binary classification, probabilities range is 0-1
    # with 0 is No Crack and 1 is Crack.
    # So confidence number for "Crack" case (< 0.5) should be transformed to > 0.5
    # to align with the confidence number mindset.
    probabilities = torch.sigmoid(output)[0][0]
    predicted_labels = (probabilities >= 0.5).float()
    if predicted_labels <= 0.5:
        probabilities = 1 - probabilities
    conf_number = probabilities.numpy() * 100  # Accuracy in percentage

    # Print the predicted class
    return f"Prediction: <strong>{classification[predicted_labels.item()]}</strong> with confidence: <strong>{conf_number:.2f}%</strong><br>"
