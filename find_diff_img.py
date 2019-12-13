#! /bin/python3

# import the necessary packages
from skimage.metrics import structural_similarity
import argparse
import imutils
import cv2

LOW_FILTER = 10
HIGH_FILTER = (None, None)

def load_images(first, second):
	"""A function loading images with their path returning opencv images
	Parameters
    ----------
	first: str
		first image to load
	second: str
		second image to load
    Returns
    -------
	tuple
		This tuple will contain the two cv2.images loaded (first, second)
	"""
	# load the two input images
	imageA = cv2.imread(first)
	imageB = cv2.imread(second)

	# Set Settings
	
	global HIGH_FILTER
	HIGH_FILTER = (0.5 * imageA.shape[0], 0.5 * imageA.shape[1])

	return (imageA, imageB)

# for application case second image (imageB) will be the one we want to edit so the one the doctor is comparing with the "sane ones" (imageA) (folder)
def generate_diffs(imageA, imageB):
	"""A function that highlight differences between two openCV images.
	Parameters
    ----------
    imageA : cv2.image
		input Image.
    imageB : cv2.image
		destination Image.

    Returns
    -------
	tuple 
		cv2.image
			imageA, the original image.
		cv2.image
			imageB, the modified image with differences highlighted with openCV.
		cv2.image
			diff, the differences of the two images
		cv2.image
			thresh, the regions of the two input images that differ
		float
			score, structural Similarity Index (SSIM)
	"""
	# convert the images to grayscale
	grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
	grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

	# compute the Structural Similarity Index (SSIM) between the two
	# images, ensuring that the difference image is returned
	(score, diff) = structural_similarity(grayA, grayB, full=True)
	diff = (diff * 255).astype("uint8")
	print("SSIM (Similarity): {}%".format(score * 100))

	# threshold the difference image, followed by finding contours to
	# obtain the regions of the two input images that differ
	thresh = cv2.threshold(diff, 0, 255,
		cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)

	# loop over the contours
	for c in cnts:
		# compute the bounding box of the contour and then draw the
		# bounding box on both input images to represent where the two
		# images differ
		(x, y, w, h) = cv2.boundingRect(c)
		if w > LOW_FILTER and h > LOW_FILTER and not w > HIGH_FILTER[0] and not h > HIGH_FILTER[1]:
			# cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 0, 255), 2)
			cv2.rectangle(imageB, (x, y), (x + w, y + h), (0, 0, 255), 2)
	
	return imageA, imageB, diff, thresh, score

def show_results(image, mode="all"):	
	"""Function that show an image using cv2.imshow
    ----------
    image : cv2.image
		image to show
	mode : str
		mode of display can be :
			"all" : it'll display everything.
			"partial" : it'll display only the original and the modified.
			"modified_only" : it'll display only the modified image.
    Returns
    -------
	nothing
	"""
	# show the output images
	if mode == "all":
		cv2.imshow("Original", image[0])
		cv2.imshow("Diff", image[2])
		cv2.imshow("Thresh", image[3])
		cv2.imshow("Modified", image[1])
	elif mode == "partial":
		cv2.imshow("Original", image[0])
		cv2.imshow("Modified", image[1])
	elif mode == "modified_only":
		cv2.imshow("Modified", image[0])

	while 1:
		k = cv2.waitKey(0)
		if k==27: # if press esc
			break

def save_results(image, path):
	"""Function that save an image using cv2.imshow
    ----------
    image : cv2.image
		image to save
    Returns
    -------
	nothing
	"""
	cv2.imwrite(path, image)

if __name__ == "__main__":
	# construct the argument parse and parse the arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-f", "--first", required=True,
		help="first input image")
	ap.add_argument("-s", "--second", required=True,
		help="second")
	ap.add_argument("-m", "--mode", required=False, 
		help="mode to use, all, partial or modified_only")
	args = vars(ap.parse_args())

	imageA, imageB = load_images(args['first'], args['second'])

	result = generate_diffs(imageA, imageB)

	save_results(result[0], 'results.png')

	mode = args['mode']
	if mode:
		show_results(result, mode)
	else:
		show_results(result)

