""" Test module for Dozy. """
import os
import sys
import unittest
from unittest import TestCase

import cv2
import numpy as np

test_dir = os.path.dirname(__file__)
src_dir = os.path.join(test_dir, '..', 'dozy')
sys.path.insert(0, src_dir)

import image
import eval


class TestImage(TestCase):
	def test_image_save(self):
		img = cv2.imread('imgs/cat.jpg')
		save_path1 = './cat1.jpg'
		save_path2 = './none/cat2.jpg'
		self.assertTrue(image.save(save_path1, img))
		self.assertFalse(image.save(save_path2, img))

	def test_image_load(self):
		img_path1 = 'imgs/cat.jpg'
		img_path2 = 'imgs/dog.jpg'
		img1 = cv2.imread(img_path1)
		img2 = cv2.imread(img_path2)
		self.assertEqual(img1, image.load(img_path1))
		self.assertFalse(img1, image.load(img_path2))

	def test_image_show(self):
		pass
	
	def test_image_crop(self):
		img = cv2.imread('imgs/cat.jpg')
		x0, y0, x1, y1 = 10, 10, 20, 20
		self.assertEqual(img, image.crop(img))
		self.assertEqual(img[y0:, :], image.crop(img, y0=y0))
		self.assertEqual(img[:y1, :], image.crop(img, y1=y1))
		self.assertEqual(img[:, x0:], image.crop(img, x0=x0))
		self.assertEqual(img[:, :x1], image.crop(img, x1=x1))

	def test_image_combine(self):
		pass

	def test_image_resize(self):
		pass


if __name__ == '__main__':
	unittest.main()
