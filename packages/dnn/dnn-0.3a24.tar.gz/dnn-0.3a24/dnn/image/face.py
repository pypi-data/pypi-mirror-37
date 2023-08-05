import cv2
from mtcnn.mtcnn import MTCNN
import os
from . import measure
from ..video import vtool

DETECTOR = None

def create_detector ():
    global DETECTOR    
    if DETECTOR is None:
        DETECTOR = MTCNN ()
    
def load (pixels, name):
    create_detector ()
    if pixels.shape [-1] != 3:
        assert name, "Parameter name is required"
        temp = ".{}-temp.bmp".format (name)
        try:
            cv2.imwrite (temp, pixels)
            pixels = cv2.imread (temp)
        finally:    
            os.remove (temp)
    return pixels
    
def  detect (pixels, name = None, resize = (48, 48)):
    image = load (pixels, name)    
    result = DETECTOR.detect_faces (image)
    img = None
    if result:
        bb = result [0]['box']
        x = max (0, bb [0])
        y = max (0, bb [1])
        crop_img = image [y:y + bb [3], x:x + bb [2]]
        if resize [0] == -1:
            resize = (int (bb [2] / (bb [3] / resize [1])), resize [1])
        elif resize [1] == -1:
            resize = (resize [0], int (bb [3] / (bb [2] / resize [0])))
        img = cv2.resize (crop_img, resize)
    return result, img

def mark (pixels, name = None):
    image = load (pixels, name)    
    result = DETECTOR.detect_faces (image)
    if not result:
        return
    else:
        bounding_box = result [0]['box']
        keypoints = result[0]['keypoints']
        cv2.rectangle (image,
                      (bounding_box[0], bounding_box[1]),
                      (bounding_box[0]+bounding_box[2], bounding_box[1] + bounding_box[3]),
                      (0,155,255),
                      2)
        cv2.circle (image, (keypoints['left_eye']), 2, (0,155,255), 2)
        cv2.circle (image, (keypoints['right_eye']), 2, (0,155,255), 2)
        cv2.circle (image, (keypoints['nose']), 2, (0,155,255), 2)
        cv2.circle (image, (keypoints['mouth_left']), 2, (0,155,255), 2)
        cv2.circle (image, (keypoints['mouth_right']), 2, (0,155,255), 2)    
    return image

def from_video (video, frame_skip = 10, min_width = 48, min_dist = 0.1, resize = (48, 48), with_marked = False, choice = 'maxdistance'):
    hashes = []
    faces = []
    hashmap = {}
    markeds = []
    cluster = []
    for idx, pixels in enumerate (vtool.capture (video, frame_skip)):
        result, img = detect (pixels, resize = (96, -1))
        if not result:
            continue
        bb = result [0]['box']
        if bb [2] < min_width:        
            continue        
        h = measure.average_hash (img)
        hashmap [id (h)] = (img, pixels)
        if choice == "maxdistance":
            dup = False
            for h_ in hashes:
                dist = measure.hamming_dist (h, h_)
                if dist < min_dist:
                    #print ("threshold", dist)
                    dup = True
                    break
    
            hashes.append (h)
            if not dup:
                faces.append (img)
                if with_marked:
                    markeds.append (mark (pixels))
        
        elif choice == "all":
            faces.append (img)
            if with_marked:
                markeds.append (mark (pixels))
            
        elif choice == "single":
            if len (cluster) == 0:
                cluster.append ([h])
                continue
            
            clustered = False
            for hashes in cluster:                
                for h_ in hashes:
                    dist = measure.hamming_dist (h, h_)
                    if dist < min_dist:
                        hashes.append (h)
                        clustered = True                        
                        break
            
            if not clustered: # new cluster
                cluster.append ([h])
        
    if choice == "single" and cluster:        
        for h in sorted (cluster, key = lambda x: len (x))[-1]:
            img, pixels = hashmap [id (h)]
            faces.append (img)            
            if with_marked:
                markeds.append (mark (pixels))
                    
    if with_marked:
        return faces, markeds
    
    return faces
    