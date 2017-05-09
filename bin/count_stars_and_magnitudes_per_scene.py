import csv
import matplotlib.pyplot as plt
from parse_scene import SceneParser

csv_fp = '../data/input.csv'
#with open(csv_fp, 'r') as csv_f:
    #reader = csv.reader(csv_f)
    #scenes = [SceneParser.parse_csv_row(row)
                #.cut_high_magnitudes(5.3)
                #for row in reader]

scenes = [scene.cut_high_magnitudes(5.3) 
            for scene in SceneParser.parse_csv(csv_fp)]

num_stars = []
magnitudes = []
magnitudes_scene_nums = []
for i, scene in enumerate(scenes):
    num_stars.append(len(scene.stars))
    magnitudes += [star.magnitude for star in scene.stars]
    magnitudes_scene_nums += [i for star in scene.stars]

print len([num for num in num_stars if num < 3])
plt.scatter(magnitudes_scene_nums, magnitudes)
plt.show()

plt.clf()
plt.scatter(range(len(scenes)), num_stars)
plt.show()

