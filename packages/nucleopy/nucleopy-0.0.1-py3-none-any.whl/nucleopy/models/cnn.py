"""
Creates a convolutional neural network model
in TensorFlow
"""

import tensorflow as tf
import math
import numpy as np
import os


class CNN:
    def __init__(self, X, y, test_X, test_y, numfeatures, featuresize, numclasses,
                 convolutions, fullyconnected, epochs, activation, learningrate=0.001,
                 optimizer="adam", dropout=0.1, batchsize=100, path=os.getcwd()+'/models/', name='CNN'):
        """
        Sets up the parameters for the CNN

        :param X: Input features
        :param y: Output labels
        :param test_X: Test input features
        :param test_y: Test output labels
        :param numfeatures: Number of features per point (not the overall number of features)
        :param featuresize: Size/length of the features
        :param numclasses: Number of labels/classes
        :param convolutions: Number of convolutional layers
        :param fullyconnected: Number of fully connected layers
        :param epochs: Number of epochs
        :param activation: Activation function
        :param learningrate: Learning rate (default is 0.001)
        :param optimizer: Optimizer (default is Adam)
        :param dropout: Dropout rate (default is 0.1)
        :param batchsize: Size of batches to be processed (default is 100)
        :param path: File path to directory of saved model
        :param name: Name of the model
        """

        self.labels = numclasses
        self.numfeatures = numfeatures
        self.featuresize = featuresize
        self.conv = convolutions
        self.fc = fullyconnected
        self.epochs = epochs
        self.activation = activation
        self.lr = learningrate
        self.optimizer = optimizer
        self.dropout = dropout
        self.batch = batchsize
        self.PATH = path
        self.NAME = name

        self.features = self.numfeatures * self.featuresize
        self.keep_prob = 1 - self.dropout

        self.x_placeholder = tf.placeholder('float', [None, self.features], name='x_placeholder')
        self.y_placeholder = tf.placeholder('float', name='y_placeholder')
        self.keep_prob_placeholder = tf.placeholder('float', name='keep_prob_placeholder')

        self.X = np.array(X).reshape([-1, self.features])
        self.y = np.array(y)

        self.test_X = np.array(test_X).reshape([-1, self.features])
        self.test_y = np.array(test_y)

    def __conv2d(self,x, W):
        return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

    def __maxpool2d(self,x):
        return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding="SAME")

    def __build(self):
        weights_keys = []
        weights_values = []

        for i in range(self.conv):
            power = math.pow(2,i)
            weights_keys.append("w_conv%i" % i)
            weights_values.append(tf.get_variable("w_conv%i" % i,
                                    [self.features, self.features, power, power * 2],
                                    initializer=tf.random_normal_initializer()))

        for i in range(self.fc):
            weights_keys.append("w_fc%i" % i)
            weights_values.append(
                tf.get_variable("w_fc%i" % i,
                                    [math.pow(2,self.conv + i), math.pow(2,self.conv + i) * 2],
                                    initializer=tf.random_normal_initializer()))

        biases_keys = []
        biases_values = []

        for i in range(self.conv):
            power = math.pow(2, i+1)
            weights_keys.append("b_conv%i" % i)
            weights_values.append(tf.get_variable("b_conv%i" % i,
                                                  [power],
                                                  initializer=tf.random_normal_initializer()))

        for i in range(self.fc):
            weights_keys.append("b_fc%i" % i)
            weights_values.append(
                tf.get_variable("b_fc%i" % i,
                                    [math.pow(2,self.conv + i) * 2],
                                    initializer=tf.random_normal_initializer()))

        weights = dict(zip(weights_keys, weights_values))
        biases = dict(zip(biases_keys, biases_values))
        weights['out'] = tf.get_variable('w_out', [int(math.pow(2, self.conv)), int(self.labels)], initializer=tf.random_normal_initializer())
        biases['out'] = tf.get_variable('b_out', [self.labels],
                                        initializer=tf.random_normal_initializer())

        self.x_placeholder = tf.reshape(self.x_placeholder, shape=[-1, self.featuresize, 1])

        if self.activation == 'relu':
            conv0 = tf.nn.relu(self.__conv2d(self.x_placeholder, weights['w_conv0']) + biases['b_conv0'])

        elif self.activation == 'sigmoid':
            conv0 = tf.nn.sigmoid(self.__conv2d(self.x_placeholder, weights['w_conv0']) + biases['b_conv0'])
        conv0 = self.__maxpool2d(conv0)

        matrix = [conv0]

        for i in range(1, self.conv):
            if self.activation == 'relu':
                c = tf.nn.relu(self.__conv2d(matrix[i-1], weights['w_conv%i' %i]) + biases['b_conv%i' %i])
                c = self.__maxpool2d(c)
                matrix.append(c)

            elif self.activation == 'sigmoid':
                c = tf.nn.sigmoid(self.__conv2d(matrix[i - 1], weights['w_conv%i' % i]) + biases['b_conv%i' % i])
                c = self.__maxpool2d(c)
                matrix.append(c)

        fc0 = tf.reshape(matrix[-1], [-1, math.pow(2, self.conv)])
        if self.activation == 'relu':
            fc0 = tf.nn.relu(tf.add(tf.matmul(fc0,weights['w_fc0']),biases['b_fc0']))

        elif self.activation == 'sigmoid':
            fc0 = tf.nn.sigmoid(tf.add(tf.matmul(fc0,weights['w_fc0']),biases['b_fc0']))

        matrix.append(fc0)

        for i in range(1, self.fc):
            if self.activation == 'relu':
                f = tf.nn.relu(tf.add(tf.matmul(matrix[i-1],weights['w_fc%i'%i]),biases['b_fc%i'%i]))
                matrix.append(f)

            elif self.activation == 'sigmoid':
                f = tf.nn.sigmoid(tf.add(tf.matmul(matrix[i - 1], weights['w_fc%i' % i]), biases['b_fc%i' % i]))
                matrix.append(f)

        last = tf.nn.dropout(matrix[-1], self.keep_prob)
        output = tf.add(tf.matmul(last, weights['out']), biases['out'], name='final')

        return output

    def train(self):
        """
        Trains the CNN
        :return: A trained and saved model
        """

        prediction = self.__build()

        with tf.name_scope('cross_entropy'):
            cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=prediction, labels=y))
            tf.summary.scalar('cross_entropy', cost)

        with tf.name_scope('train'):
            optimizer = tf.train.AdamOptimizer(self.lr).minimize(cost)  # learning rate = 0.001

        with tf.name_scope('accuracy'):
            correct = tf.equal(tf.argmax(prediction, 1), tf.argmax(y, 1))
            accuracy = tf.reduce_mean(tf.cast(correct, 'float'))
            tf.summary.scalar('accuracy', accuracy)

        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())
            saver = tf.train.Saver()
            merged_summary = tf.summary.merge_all()

            for epoch in range(self.epochs):
                epoch_loss = 0
                for i in range(int(self.X.shape[0])/self.batch):
                    randidx = np.random.choice(self.X.shape[0], self.batch, replace=False)
                    epoch_x, epoch_y = self.X[randidx, :], self.y[randidx,:]
                    j, c = sess.run([optimizer, cost],
                                    feed_dict={self.x_placeholder: epoch_x,
                                               self.y_placeholder: epoch_y,
                                               self.keep_prob_placeholder: self.keep_prob})
                    if i == 0:
                        [ta] = sess.run([accuracy],
                                        feed_dict={self.x_placeholder: epoch_x,
                                                   self.y_placeholder: epoch_y,
                                                   self.keep_prob_placeholder: self.keep_prob})
                        print 'Train Accuracy', ta

                    epoch_loss += c

                print('\nEpoch', epoch+1, 'completed out of', self.epochs, '\nLoss', epoch_loss)

            saver.save(sess, self.PATH + self.NAME)
            saver.export_meta_graph(self.PATH + self.NAME + '.meta')
            print "Model Saved."

            print '\n', 'Train Accuracy', accuracy.eval(
                feed_dict={self.x_placeholder: self.X,
                           self.y_placeholder: self.y,
                           self.keep_prob_placeholder: self.keep_prob})
            print '\n', 'Test Accuracy', accuracy.eval(
                feed_dict={self.x_placeholder: self.test_X,
                           self.y_placeholder: self.test_y,
                           self.keep_prob_placeholder: 1.0})


