import io
from PIL import Image
from torchvision import models, transforms
from torch.nn import functional as F
import numpy as np
import cv2
import json
import os

def plot_hot(path):
    model_id = 1

    if model_id == 1:
        net = models.squeezenet1_1(pretrained=True)
        finalconv_name = 'features' # this is the last conv layer of the network
    elif model_id == 2:
        net = models.resnet18(pretrained=True)
        finalconv_name = 'layer4'
    elif model_id == 3:
        net = models.densenet161(pretrained=True)
        finalconv_name = 'features'

    net.eval()

    features_blobs = []
    def hook_feature(module, input, output):
        features_blobs.append(output.data.cpu().numpy())

    net._modules.get(finalconv_name).register_forward_hook(hook_feature)

    # get the softmax weight
    params = list(net.parameters())
    # print('param shape:',params[-1].size())  # 1000
    # print('param-2 shape:',params[-2].data.numpy().shape)  # (1000, 512, 1, 1)
    weight_softmax = np.squeeze(params[-2].data.numpy())
    # print(weight_softmax.shape)  # 1000*512
    def returnCAM(feature_conv, weight_softmax, class_idx):
        # generate the class activation maps upsample to 256x256
        size_upsample = (256, 256)
        bz, nc, h, w = feature_conv.shape
        output_cam = []
        for idx in class_idx:
            cam = weight_softmax[idx].dot(feature_conv.reshape((nc, h*w)))
            cam = cam.reshape(h, w)
            cam = cam - np.min(cam)
            cam_img = cam / np.max(cam)
            cam_img = np.uint8(255 * cam_img)
            output_cam.append(cv2.resize(cam_img, size_upsample))  # 灰度图
            # cv2.imwrite('hot_dog1.jpg', cv2.resize(cam_img, size_upsample))
        return output_cam


    normalize = transforms.Normalize(
       mean=[0.485, 0.456, 0.406],
       std=[0.229, 0.224, 0.225]
    )
    preprocess = transforms.Compose([
       transforms.Resize((224,224)),
       transforms.ToTensor(),
       normalize
    ])


    img_pil = Image.open(path)

    img_tensor = preprocess(img_pil)
    # img_variable = Variable(img_tensor.unsqueeze(0))
    img_variable = img_tensor.unsqueeze(0)
    logit = net(img_variable)

    # download the imagenet category list


    with open("labels.json",'r') as load_f:
        load_dict = json.load(load_f)
        # print(load_dict)


    # classes = {int(key):value for (key, value) in requests.get(LABELS_URL).json().items()}
    classes = {int(key):value for (key, value) in load_dict.items()}

    h_x = F.softmax(logit, dim=1).data.squeeze()
    probs, idx = h_x.sort(0, True)
    probs = probs.numpy()
    idx = idx.numpy()

    # output the prediction
    for i in range(0, 5):
        print('{:.3f} -> {}'.format(probs[i], classes[idx[i]]))


    # print('features_blobs[0] shape:',features_blobs[0].shape)  # 1*512*13*13
    # print('idx[0]',idx[0])  # 273
    # generate class activation mapping for the top1 prediction
    CAMs = returnCAM(features_blobs[0], weight_softmax, [idx[0]])

    # render the CAM and output
    print('output {image_name1} for the top1 prediction: {s}'.format(image_name1 = path,s = classes[idx[0]]))
    img = cv2.imread(path)
    height, width, _ = img.shape
    heatmap = cv2.applyColorMap(cv2.resize(CAMs[0],(width, height)), cv2.COLORMAP_JET)
    result = heatmap * 0.3 + img * 0.5
    cv2.imwrite('out_{name}'.format(name=path), result)
    print("done!")

