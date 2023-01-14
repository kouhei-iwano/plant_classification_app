import cv2
from PIL import Image
import numpy as np
import torch
from cucumber_leaf_face.recognition.model import *
from torchvision import transforms

def softmax(x):
    u = np.sum(np.exp(x))
    return np.exp(x) / u

def main(img_path):
    model_path = "cucumber_leaf_face/recognition/save_model/cucumber_resnet18_last_model.pth"
    label = [
        "健全",
        "うどんこ病",
        "灰色かび病",
        "炭疽病",
        "べと病",
        "褐斑病",
        "つる枯病",
        "斑点細菌病",
        "CCYV",
        "モザイク病",
        "MYSV",
    ]

    num_classes = 11


    model_ft = initialize_model(num_classes, use_pretrained=False)

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model_ft = model_ft.to(device)
    if torch.cuda.is_available():
        model_ft.load_state_dict(torch.load(model_path))
    else:
        model_ft.load_state_dict(
            torch.load(model_path, map_location=torch.device("cpu"))
        )
    model_ft.eval()

    img_path = "media/" + str(img_path)
    img = Image.open(img_path)
    img = transforms.Compose([
        transforms.Resize(224),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
    ])(img)
    img = img.view(1, 3, 224, 224)

    output = model_ft(img)
    output = output.detach().numpy()
    output = softmax(output)
    indices = np.argsort(-output)
    out_answer = []
    for i in range(5):
        out_answer.append(
            [label[indices[0, i]], round(100 * output[0, indices[0, i]], 2)]
        )
    return out_answer

if __name__ == "__main__":
    main()
