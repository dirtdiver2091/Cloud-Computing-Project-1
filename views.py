import config
import os
import uuid

from s3_handeling import list_content, upload
from flask import Flask, request, render_template, redirect
from PIL import Image, ImageOps, ImageFilter

views = Flask(__name__)

@views.route("/index", methods=["GET", "POST"])
@views.route("/", methods=["GET", "POST"])
def index():

	if request.method == "POST":

		image_change = request.form.get("edited")

		if request.files:

			# Check to see if there are any errors with the image
			img = request.files["image"]
			# Save the image to the Changed Images folder (Directory)
			img.filename = str(uuid.uuid4()) + ".jpg"
			img.save(os.path.join(config.Changed_Images, img.filename))

		# Change the image
		changedImage = applyFilter(img.filename, applyFilter())

		# Uploading to s3
		upload(os.path.join(config.Changed_Images, changedImage), changedImage)

		# erase temp images, reset form

		# Load all saved and edited images from s3
		get_images_from_s3()

	return render_template('index.html')

def get_images_from_s3():

	# Make a request to the s3, which will get a list of all files in the bucket
	response = list_content()

	# Get the url for each file pulled
	images = []
	for item in response:
		images.append(config.base_s3_url + item["Key"])

	# Inject that specific url into the html img tag
	return render_template('index.html', photo_urls=images)


def applyFilter(filename, filter):

    # Retrieve image here
    image = Image.open(os.path.join(config.Changed_Images, filename))

    if filter == 'gray':
        im = ImageOps.grayscale(image)
    elif filter == 'blur':
        im = ImageOps.filter(ImageFilter.BLUR)
    elif filter == 'solar':
        im = ImageOps.solarize(image, threshold=80)

	filtered_image = "filtered_" + filename

	im.save(os.path.join(config.Changed_Images, filtered_image))
	return filtered_image

if __name__ == "__main__":
	views.run(debug=True)