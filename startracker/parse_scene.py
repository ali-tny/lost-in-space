import csv
import numpy as np
from scene import Scene
from star import Star

class SceneParser:
    @staticmethod
    def parse_csv(csv_path):
        scenes = []
        fails = []
        with open(csv_path, 'r') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                scene, fail = SceneParser.parse_csv_row(row)
                if scene.stars: scenes.append(scene)
                if fail: fails.append(fail)
        return scenes, fails

    @staticmethod
    def parse_csv_row(row):
        if len(row)%3 !=0: 
            failed = row
            return Scene([]), failed
        star_list = [row[i:i+3] for i in range(0, len(row), 3)]
        stars = []
        failed = []
        for i, s in enumerate(star_list):
            try:
                stars.append(Star(i,s[2],s[0],s[1]))
            except ValueError:
                failed.append(s)
        return Scene(stars), failed

    @staticmethod
    def parse_hip_data(data_path):
        with open(data_path, 'r') as data:
            reader = csv.reader(data, delimiter='|')
            stars = []
            failed = []
            for r in reader:
                try:
                    idnum = r[1]
                    deg_to_rad = np.pi/180
                    mag = r[5]
                    theta = float(r[8])*deg_to_rad
                    psi = float(r[9])*deg_to_rad
                    stars.append(Star(idnum, mag, None, None, theta, psi))
                except ValueError:
                    failed.append(r)
            return Scene(stars), failed
                
        
