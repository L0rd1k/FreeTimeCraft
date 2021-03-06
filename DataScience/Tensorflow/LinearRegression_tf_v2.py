#EXAMPLE FOR TENSORFLOW v2

import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

learning_rate = 0.01
rnd_range = np.random
display_step = 100
X = np.array([3.3,4.4,5.5,6.71,6.93,4.168,9.779,6.182,7.59,2.167, 7.042,10.791,5.313,7.997,5.654,9.27,3.1])
Y = np.array([1.7,2.76,2.09,3.19,1.694,1.573,3.366,2.596,2.53,1.221, 2.827,3.465,1.65,2.904,2.42,2.94,1.3])
Weight = tf.Variable(rnd_range.randn(), name="Weight")
Bias = tf.Variable(rnd_range.randn(), name="Bias")
optimizer = tf.optimizers.SGD(learning_rate)


def linear_regression(x):
    # y = mx + b - linear equation
    return Weight * x + Bias

def mean_square(y_pred, y_true):
    return tf.reduce_mean(tf.square(y_pred - y_true))


def run_optimization():
    with tf.GradientTape() as g:
        pred = linear_regression(X)
        loss = mean_square(pred, Y)
    gradients = g.gradient(loss, [Weight, Bias])
    optimizer.apply_gradients(zip(gradients, [Weight, Bias]))

def run_training(training_step):
    for step in range(1, training_step + 1):
        run_optimization()
        if step % display_step == 0:
            pred = linear_regression(X)
            loss = mean_square(pred, Y)     
            print("step: %i, loss: %f, W: %f, b: %f" % (step, loss, Weight.numpy(), Bias.numpy()))


def main():
    training_steps = 100
    run_training(training_steps)

    # Show result
    plt.plot(X, Y, 'ro', label='Original data')
    plt.plot(X, np.array(Weight * X + Bias), label='Fitted line')
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
