
import requests
import os
from requests import exceptions
import face_recognition
import cv2
import matplotlib.pyplot as plt
import math


def detect_faces(image_name):
    '''
    Detect the faces in the image and get the rows and column values from the image grid
    Face recognition module in opencv is used to detect the faces which uses HOG detector as the model
    :param image_name:
    :return:
    '''
    result_name = 'result.jpg'
    num_cols = 8
    num_rows = 8

    face_grid_list = []

    # read image and convert it to RGB
    img = cv2.imread(image_name)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    orig=img.copy()
    print('Shape of the image :{}' .format(img.shape[0:2]))
    img_height = img.shape[0]
    img_width = img.shape[1]

    #find the width and height of each tile

    tile_width = img_width//num_cols
    tile_height = img_height//num_rows

    #create list of tiles (64 tiles in this case)

    tile_list = [[i, j] for i in range(math.ceil(img_width / tile_width)) for j in
            range(math.ceil(img_height / tile_height))]


    print("Detecting faces in the image...")
    #As the image is divided into 8*8 grids ,we will loop through each tile to detect faces

    #Initialise tile count,xmin and ymin value to slide through the image
#     tile_count =0
#     xmin=0
#     ymin=0
#     while tile_count < len(tile_list):

#         #set the width and height of each tile
#         ymax=ymin + tile_height
#         xmax=xmin + tile_width

#         #Extract tile portion from original image
#         img_tile = img[ymin:ymax, xmin:xmax]

#         #Pass the extracted image to the opencv face_recognition module.This module uses HOG detector to detect faces
#         boxes = face_recognition.face_locations(img_tile, model='hog')

#         #if face is detected append the row,column values to a list
#         if len(boxes) > 0:
#             face_grid_list.append(tile_list[tile_count])

#         #set ymin and xmin to new values
#         if ymax > img_height:
#             ymax=0
#         if xmax > img_width:
#             xmax=0
#         ymin=ymax
#         xmin=xmax

#         tile_count += 1

#     print("Output : ",face_grid_list)
    tile_count = 0
    for y in range(0, img_height, tile_height):
        for x in range(0, img_width, tile_width):
            image_tile = img[y:y + tile_height, x:x + tile_width]
            boxes = face_recognition.face_locations(image_tile, model='hog')
            if len(boxes) > 0:
                print('boxes1', boxes)
                print('tile_no',tile_list[tile_count])
                face_grid_list.append(tile_list[tile_count])
            tile_count += 1

    json_results = json.dumps(face_grid_list)

    print("Output : ",json_results)

    #delete existing output image
    delete_oldimages(result_name)
    # save and show the output image with detected faces
    boxes = face_recognition.face_locations(orig, model='hog')
    for (top, right, bottom, left) in boxes:
        cv2.rectangle(orig, (left, top), (right, bottom), (0, 255, 0), 2)
    cv2.imwrite('result.jpg',orig)
    plt.imshow(orig)
    plt.show()

def delete_oldimages(file_name):
    '''
    delete existing input image
    :param file_name:
    :return:
    '''
    if os.path.exists(file_name):
        os.remove(file_name)

def download_image(image_name,access_code):

    '''
    Download the image from hackattic website using access code
    :return:
    '''
    param = {'access_token': access_code}
    response = requests.get('https://hackattic.com/challenges/basic_face_detection/problem?', params=param)
    response.raise_for_status()

    image_link = response.json()
    print(image_link)
    # try to download the image
    try:
        # delect existing images
        delete_oldimages(image_name)

        # make a request to download the image
        image_url = image_link["image_url"]
        print("Fetching: {}".format(image_url))
        image = requests.get(image_url, timeout=30)

        image_path = os.path.sep.join([image_name])
        # write the image to disk
        f = open(image_path, "wb")
        f.write(image.content)
        f.close()

    # catch any errors that would not unable us to download the
    # image
    except Exception as e:
        print(e)

if __name__ == '__main__':
    #8eeb6ee46c7cfeb7
    access_code = (input("Enter the access code "))
    image_name = 'image.jpg'

    download_image(image_name,access_code)

    detect_faces(image_name)




