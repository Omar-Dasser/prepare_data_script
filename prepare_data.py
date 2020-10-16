from xml.dom import minidom
import os
import cv2
import json 
import xmltodict 
import pandas as pd 

cwd = os.getcwd()

orig_img_path = os.path.join(cwd,'orig_images')
new_img_path = os.path.join(cwd,'new_images')
XML_path = os.path.join(cwd,'XMLs')


def to_json(XML_file):

	with open(XML_file) as xml_file: 
		data_dict = xmltodict.parse(xml_file.read()) 
		xml_file.close()
		# with open('Data2.json','w') as out_file: 
		# 	json_data = json.dump(data_dict,out_file,indent=4)
		return data_dict

json_data = to_json('test2.xml')


def get_obj(json_data,target):
	obj = json_data['annotation']['object']
	if isinstance(obj,list):
		for ob in obj:
			if ob['name'] == target:
				return obj
	else:
		if obj['name'] == target:
			return obj
	return -1


# obj = json_data['annotation']['object']
def get_coords(obj):

	X = [int(obj['bndbox']['xmin']),int(obj['bndbox']['xmax'])]
	Y = [int(obj['bndbox']['ymin']),int(obj['bndbox']['ymax'])]
	return X,Y

# box =[ [X[0],Y[0]], [X[0],Y[1]] , [X[1],Y[0]], [X[1],Y[1]] ]

target_dict = {'secured outlet':[],'unsecured outlet':[],'cap':[]}

def crop_save_img(json_data,X,Y,target):
	filename = json_data['annotation']['filename']
	img_path = os.path.join(orig_img_path,filename)
	new_path = os.path.join(new_img_path,filename)
	img = cv2.imread(img_path)
	crop_img = img[Y[0]:Y[1], X[0]:X[1]]
	# cv2.imshow("croped",crop_img)
	# cv2.waitKey(0)
	cv2.imwrite(new_path, img)
	target_dict[target].append(filename)


if __name__ == '__main__':

for target in target_dict: 

	for xml_file in os.listdir(XML_path):
		json_data = to_json(xml_file)
		obj = get_obj(json_data,target)
		if obj == -1:
			continue
		X,Y = get_coords(obj)
		crop_save_img(json_data,X,Y,target)
		

df = pd.DataFrame(target_dict)

df.to_csv('out.csv')




