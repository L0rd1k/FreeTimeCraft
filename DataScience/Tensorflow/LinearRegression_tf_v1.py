import tensorflow as tf
import numpy
import matplotlib.pyplot as plt
rng = numpy.random
training_epoch_num = 1000
learning_rate = 0.01
display_step = 1000

train_X = numpy.asarray([3.3,4.4,5.5,6.71,6.93,4.168,9.779,6.182,7.59,2.167, 7.042,10.791,5.313,7.997,5.654,9.27,3.1])
train_Y = numpy.asarray([1.7,2.76,2.09,3.19,1.694,1.573,3.366,2.596,2.53,1.221, 2.827,3.465,1.65,2.904,2.42,2.94,1.3])
n_samples = train_X.shape[0]

X = tf.placeholder("float")
Y = tf.placeholder("float")

Weight = tf.Variable(rng.randn(), name="weight")
Bias = tf.Variable(rng.randn(), name="bias")

# Linear Model
pred = tf.add(tf.multiply(X, Weight), Bias)

# Mean Squared
cost = tf.reduce_sum(tf.pow(pred - Y, 2)) / (2 * n_samples)

# Gradient descent
optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)

# Initialize variable - assign default values to them
init = tf.global_variables_initializer()

def run_training():
    with tf.Session() as sessn:
        sessn.run(init)
        for epoch in range(training_epoch_num):
            for(x, y) in zip(train_X, train_Y):
                sessn.run(optimizer, feed_dict = {X:x, Y:y})
                if(epoch + 1) % display_step == 0:
                    c = sessn.run(cost, feed_dict={X: train_X, Y:train_Y})
                    print("Epoch:", '%04d' % (epoch+1), "cost=", "{:.9f}".format(c),  "W=", sessn.run(Weight), "b=", sessn.run(Bias))
            
        print("Optimization Finished!")
        training_cost = sessn.run(cost, feed_dict={X: train_X, Y: train_Y})
        print("Training cost=", training_cost, "W=", sessn.run(Weight), "b=", sessn.run(Bias), '\n')   

        plt.plot(train_X, train_Y, 'ro', label='Original data')
        plt.plot(train_X, sessn.run(Weight) * train_X + sessn.run(Bias), label='Fitted line')
        plt.legend()
        plt.show()

run_training()