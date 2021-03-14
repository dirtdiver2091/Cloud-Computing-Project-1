import config
import os
import uuid

from s3_handeling import list_content, upload
from flask import Flask, request, render_template, redirect
from PIL import Image, ImageOps, ImageFilter

views = Flask(__name__)

@views.route("/home", methods=["GET", "POST"])
@views.route("/", methods=["GET", "POST"])
def home():

	if request.method == "POST":

		image_transformation = request.form.get("transformation")

		if request.files:

			# after receiving image, error check it

			img = request.files["image"]
			# save to a temp diretory
			img.filename = str(uuid.uuid4()) + ".jpg"
			img.save(os.path.join(config.temp_storage, img.filename))

		# transform image
		new_image = image_transform(img.filename, image_transformation)

		# upload to s3
		upload(os.path.join(config.temp_storage, new_image), new_image)

		# erase temp images, reset form

		# redirect to content page
		return redirect("content")

	return render_template('home.html')

@views.route("/content")
def get_images_from_s3():

	# make request to s3 that gets list of all files in bucket
	response = list_content()

	# get the url for every file
	photos = []
	for item in response:
		photos.append(config.base_s3_url + item["Key"])

	# inject that url into html img tag
	return render_template('content.html', photo_urls=photos)


def applyFilter(filename, filter):

    # Retrieve image here
    image = 'C:\Users\Andrew Pidhajny\Temple Classes\Senior Year\Spring Semester\Cloud Computing\Project 1\Code\Cloud-Computing-Project-1\Images' + filename

    i = image.split('.')
    changedImageName = i[0] + '-changed.jpg'

    # The edited image
    changedImage = 'C:\Users\Andrew Pidhajny\Temple Classes\Senior Year\Spring Semester\Cloud Computing\Project 1\Code\Cloud-Computing-Project-1\Changed Images' + changedImageName

    # Save image here
    im = Image.open(image)

    if filter == 'gray':
        im = ImageOps.grayscale(image)
    elif filter == 'blur':
        im = ImageOps.filter(ImageFilter.BLUR)
    elif filter == 'solar':
        im = ImageOps.solarize(image, threshold=80)

    im.save(changedImage)

    return changedImageName

if __name__ == "__main__":
	views.run(debug=True)