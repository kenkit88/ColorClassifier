import os
import cv2
import sys
import dlib
import numpy as np
import argparse
import tensorflow as tf


image_path = sys.argv[1]


def colorClass():
    tf.reset_default_graph()
    with tf.gfile.FastGFile("retrained_graph.pb", 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        tf.import_graph_def(graph_def, name='')
    label_lines = [line.rstrip() for line in tf.gfile.GFile("retrained_labels.txt")]
    image_data = tf.gfile.FastGFile(image_path, 'rb').read()

    with tf.Session() as sess:
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
        predictions = sess.run(softmax_tensor,
                 {'DecodeJpeg/contents:0': image_data})
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]

        for node_id in top_k:
            human_string = label_lines[node_id]
            score = predictions[0][node_id]
            print('%s (score = %.5f)' % (human_string, score))

        maxs = 0
        for i in range(0, len(predictions[0]),1):
            if predictions[0][i] > maxs:
                maxs = predictions[0][i]
                color = label_lines[i]

        sess.close()

    return color


image = cv2.imread(image_path)
height, width, channels = image.shape

color = colorClass()
font = cv2.FONT_HERSHEY_SIMPLEX
#cv2.putText(image, color, 50, 50, font, 8, (255, 255, 255), 2)
cv2.putText(image, color, (20,int(height/2)), font, 2, (255, 255, 255), 2, cv2.LINE_AA)


cv2.imshow("Color", image)

cv2.waitKey(0)

cv2.destroyAllWindows()

