import argparse
import os
import find_diff_img as diff
import csv


def export_csv(results, to_test):
	"""Function that create csv of similarity between images
    ----------
    image : cv2.image
		image to save
    Returns
    -------
	nothing
	"""
	with open('results.csv', 'w') as csvfile:
		filewriter = csv.writer(csvfile, delimiter=',',
								quotechar='|', quoting=csv.QUOTE_MINIMAL)
		title = str('Images comparison' + to_test)
		filewriter.writerow([title , str('SSIM (Similarity)')])
		for res in results:
			filewriter.writerow([res[0], res[1]])

if __name__ == "__main__":
	ap = argparse.ArgumentParser()
	ap.add_argument("-f", "--first", required=True,
		help="\"sane\" input image folder")
	ap.add_argument("-s", "--second", required=True,
		help="image to highlight differences")
	
	args = vars(ap.parse_args())

	filelist = [f for f in os.listdir(args['first']) if f.endswith('.png')]

	scores = []
	for f in filelist:
		images = diff.load_images(args['first'] + '/' + f, args['second'])
		result = diff.generate_diffs(images[0], images[1])
		scores.append((args['first'] + f, result[4]))

	export_csv(scores, args['second'])