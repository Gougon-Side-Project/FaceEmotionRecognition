import onnxruntime

import numpy as np
import torch

class EmotionPredictor():
    def __init__(self):
        self.session = onnxruntime.InferenceSession('cnn_model.onnx')

    def Predict(self, face):
        input = torch.tensor(np.expand_dims([face], 1), dtype=torch.float32)
        input_name = self.session.get_inputs()[0].name
        predict = self.session.run(None, {input_name: self.toNumpy(input)})[0]
        predict_score = np.max(predict)
        predict_emotion = np.argmax(predict)
        print('predict score :', predict_score)
        print('predict emotion :', predict_emotion)
        return predict_score, predict_emotion

    def toNumpy(self, tensor):
        return tensor.detach().cpu().numpy() if tensor.requires_grad else tensor.cpu().numpy()