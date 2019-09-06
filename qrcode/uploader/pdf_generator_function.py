from fpdf import FPDF
import numpy as nm
from PIL import Image
from shutil import rmtree
from os import listdir, remove, mkdir
from os.path import isfile, join
from zipfile import ZipFile
from django.conf import settings

# TOTAL IMAGES IN THE DIRECTORY
TOTAL_IMAGES = 0
# PDF FILES WITH PREFIX
FILE_NAME_PREFIX = 'qrcodes'
BASE_DIR = settings.BASE_DIR

# Directory where the images are present or images are extracted
def image_adder(no_of_pages = 0, page_dimension = (0,0), big_frame_dimension = (0, 0), frame_dimension = (0,0), padding_btw_frames = (1,1), image_resize = (0,0), circle_required = False, repetition = 1):

	dimensions_page = (px_to_pt_converter(page_dimension[0]), px_to_pt_converter(page_dimension[1]))
	
	if image_resize[0] == 0 or image_resize[1] == 0:
		image_resize = frame_dimension

	# Creating a directory where all the images will be saved
	directory = BASE_DIR + "/uploader/qrcodes/"
	try:
		mkdir(directory)
	
	except FileExistsError:
		print("Directory already exists! Need to delete it.")
		rmtree(directory)
		mkdir(directory)
	except OSError:
		print("Error creating a directory with name \'qrcodes\'")
		raise OSError
	else:
		print("Successfully created a directory with name \'qrcodes\'")

	try:
		# Extract zip files to a folder
		extractZip(directory)
	except FileNotFoundError:
		print("Error occurred not able to find the directory!")
		raise FileNotFoundError
	except RuntimeError:
		print("Runtime error while processing zipfiles!")
		raise RuntimeError

	try:
		# Directory of the images are required.
		images = resize_images_replicate_and_fetch(directory, image_resize, repetition)
	except IOError:
		print("Either file doesn't exist or image cannot be opened and identified!")
		rmtree(directory)
		raise IOError

	# print(images)
	TOTAL_IMAGES = len(images)
	index_images = 0

	# Incrementing this value for the filename.
	suffix_filename = 1

	while index_images < TOTAL_IMAGES:
		# Initialize pdf variable.
		pdf = FPDF('P', 'pt', dimensions_page)

		# Add a page to the pdf
		pdf.add_page()
		# print(pdf.get_x(), pdf.get_y())
		pdf.set_font('Arial', 'B', 10)
		# Big frame 
		dimensions_bigframe = (px_to_pt_converter(page_dimension[0]-50), px_to_pt_converter(page_dimension[1]-50))
		default_current_pos_x = pdf.get_x()
		default_current_pos_y = pdf.get_y()
		pdf.rect(pdf.get_x(), pdf.get_y(), dimensions_bigframe[0], dimensions_bigframe[1], style = 'D')

		# Frame
		pdf.set_x(default_current_pos_x) 
		pdf.set_y(default_current_pos_y)
		dimensions_frame = (int(px_to_pt_converter(frame_dimension[0])),int(px_to_pt_converter(frame_dimension[1])))

		current_pos_x = default_current_pos_x
		current_pos_y = default_current_pos_y

		
		for row in nm.arange(current_pos_y, dimensions_bigframe[1], dimensions_frame[1]+padding_btw_frames[1]):
			for col in nm.arange(current_pos_x, dimensions_bigframe[0], dimensions_frame[0]+padding_btw_frames[0]):
				if ((col + dimensions_frame[0]) > dimensions_bigframe[0]) or ((row + dimensions_frame[1]) > dimensions_bigframe[1]):
					break
				position_in_x_direction = col+px_to_pt_converter(padding_btw_frames[0])
				position_in_y_direction = row+px_to_pt_converter(padding_btw_frames[1])
				pdf.rect(position_in_x_direction, position_in_y_direction, dimensions_frame[0], dimensions_frame[1], style = 'D')
				if index_images < TOTAL_IMAGES:
					try:
						load_image_to_pdf(pdf, directory + images[index_images], position_in_x_direction, position_in_y_direction, dimensions_frame[0], dimensions_frame[1], circle_required)
					except FileNotFoundError:
						rmtree(directory)
						raise FileNotFoundError
					# processed images are removed
					remove(directory + images[index_images])
					pdf.set_x(col+dimensions_frame[0])
					pdf.set_y(row)
				index_images += 1

			pdf.set_y(row)
			pdf.set_x(current_pos_x)

		# output the pdf to a file. FILENAME = qrcodes(1...n).pdf
		FILE_NAME = BASE_DIR + "/uploader/" + FILE_NAME_PREFIX + str(suffix_filename) + ".pdf"
		pdf.output(FILE_NAME, 'F')
		suffix_filename = suffix_filename + 1
		pdf.close()
		
		
	
	# Removing the directory after processing
	print("Removing the images directory after processing")	
	rmtree(directory)
	print("Removing the zip files after processing")
	rmtree(BASE_DIR + "/uploader/zipfiles")
	


# Values in pixels to be converted into points
def px_to_pt_converter(val):
	return val*1
	
def pt_to_px_converter(val):
	return val*1

# qrcodes filename in a list
def resize_images_replicate_and_fetch(directory, image_resize, repetition):

	# directory = "/uploader/qrcodes/"
	onlyfiles = [f for f in listdir(directory) if isfile(join(directory, f))]
	onlyimages = list(filter(lambda x: (x.split(".")[1] in ["png", "jpg", "jpeg"]), onlyfiles))

	# Resize images and save them in the same folder
	newimages = []
	for i in onlyimages:
		outputfile = []
		img = Image.open(directory + i)
		if image_resize[0] == img.size[0] and image_resize[1] == img.size[1]:
			newimages = onlyimages
			break
		img = img.resize((int(pt_to_px_converter(image_resize[0])),int(pt_to_px_converter(image_resize[1]))), Image.LANCZOS)
		for j in range(repetition):
			file_name = i.split(".")[0]+ str(j+1)+".png"
			outputfile.append(file_name)
			img.save(directory + file_name, quality = 90)

		# outputfile = i.split(".")[0]+"1"+".png"
		# img.save(directory + outputfile)
		# Removing the extracted files from the folder
		remove(directory + i)
		newimages.extend(outputfile)

	# print(newimages)
	return newimages

def load_image_to_pdf(pdf, directory, current_pos_x, current_pos_y, dimensions_frame_x, dimensions_frame_y, circle_required):
	img = Image.open(directory)
	
	# img_w, img_h = img.size
	img_w, img_h = img.size


	# Frame size should be greater than size of image
	img_w_to_pt = px_to_pt_converter(img_w)
	img_h_to_pt = px_to_pt_converter(img_h)

	if dimensions_frame_x >= img_w_to_pt and dimensions_frame_y >= img_h_to_pt:
		pos_x = current_pos_x + (dimensions_frame_x - img_w_to_pt)/2
		pos_y = current_pos_y + (dimensions_frame_y - img_h_to_pt)/2
		# print("positions :" , pos_x, pos_y)
		# print("current x and y", pos_x, " ", pos_y)
		pdf.image(directory, pos_x, pos_y)
		radius = pt_to_px_converter(4)

		'''Circle drawing logic around the qrcode image'''

		if circle_required == True:
		# Top Left corner circle of the frame.
			pdf.ellipse(pos_x-radius, pos_y-radius, radius*2, radius*2)

		# Top Right corner circle of the frame.
			pdf.ellipse(pos_x + img_w - radius, pos_y - radius, radius*2, radius*2)

		# Bottom left corner circle of the frame
			pdf.ellipse(pos_x-radius, pos_y+ img_h -radius, radius*2, radius*2)

		# Bottom right corner circle of the frame
			pdf.ellipse(pos_x+ img_w -radius, pos_y+ img_h -radius, radius*2, radius*2)
	else:
		print("dimensions of frame is less than image dimensions, Cannot fit!")

# Extract from zip files
def extractZip(directory):
	
	
	# Get all the zip files from the folder
	folder = BASE_DIR + "/uploader/zipfiles/"
	onlyfiles = [f for f in listdir(folder) if isfile(join(folder, f))]
	zipfiles = [f for f in onlyfiles if f.split('.')[1] == "zip"]
	# print("temp files", temp)
	# zipfiles = list(filter(lambda x: x.split(".")[1] == "zip", onlyfiles))
	for f in zipfiles:
		# print(f)
		zf = ZipFile(folder+f, 'r')
		zf.extractall(directory)
		zf.close()
	


# Give the page dimensions and frame dimensions, Also change the folder in extractZip() function.
''' All dimensions are in width X height'''
# image_adder(page_dimension =  (5760, 47700), frame_dimension = (113.3858267717, 113.3858267717))
# image_adder(page_dimension =  (3508, 4961), frame_dimension = (200, 120), image_resize=(198, 118))

 
