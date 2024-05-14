# Script to create CSV data file from Pascal VOC annotation files
# Based off code from GitHub user datitran: https://github.com/datitran/raccoon_dataset/blob/master/xml_to_csv.py

import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET

def xml_to_csv(path):
    xml_list = []
    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            x_y_list = []
            for m in member[5]:
                divided = int(m.text) / 640
                print(divided)
                if divided < 0.0:
                    x_y_list.append(0.0)
                elif divided > 1.0:
                    x_y_list.append(1.0)
                else:
                    x_y_list.append(divided)
            value = (root.find('filename').text,
                     int(root.find('size')[0].text),
                     int(root.find('size')[1].text),
                     member[0].text,
                     x_y_list[0],
                     x_y_list[1],
                     x_y_list[2],
                     x_y_list[3]
                     )
            xml_list.append(value)
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'xmax', 'ymin', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df

def main():
    for folder in ['train','validation']:
          image_path = os.path.join(os.getcwd(), ('images/' + folder))
          xml_df = xml_to_csv(image_path)
          xml_df.to_csv(('images/' + folder + '_labels.csv'), index=None)
          print('Successfully converted xml to csv.')


main()
