#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import torch
from torch import nn
import matplotlib.pyplot as plt

x_train = np.array([[3.3], [4.4], [5.5], [6.71], [6.93], [4.168],
                    [9.779], [6.182], [7.59], [2.167], [7.042],
                    [10.791], [5.313], [7.997], [3.1]], dtype=np.float32)
y_train = np.array([[1.7], [2.76], [2.09], [3.19], [1.694], [1.573],
                    [3.366], [2.596], [2.53], [1.221], [2.827],
                    [3.465], [1.65], [2.904], [1.3]], dtype=np.float32)


tensor_x_train = torch.from_numpy(x_train)
tensor_y_train = torch.from_numpy(y_train)



class linearRegression(nn.Module):
    def __init__(self):
        super(linearRegression, self).__init__()
        self.linear = nn.Linear(1, 1)  # input and output is 1 dimension

    def forward(self, x):
        out = self.linear(x)
        return out


model = linearRegression()

criterion = nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=1e-4)


num_epochs = 10000
for epoch in range(num_epochs):
    inputs = tensor_x_train
    target = tensor_y_train
    # forward
    out = model(inputs)
    loss = criterion(out, target)
    # backward
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    if (epoch+1) % 20 == 0:
        print('Epoch[{epoch+1}/{num_epochs}], loss: {loss.item():.6f}')

model.eval()
with torch.no_grad():
    predict = model(tensor_x_train)
predict = predict.data.numpy()

fig = plt.figure(figsize=(10, 5))
plt.plot(tensor_x_train.numpy(), tensor_y_train.numpy(), 'ro', label='Original data')
plt.plot(tensor_x_train.numpy(), predict, label='Fitting Line')
plt.legend()
plt.show()

# 保存模型
# torch.save(model.state_dict(), './linear.pth')