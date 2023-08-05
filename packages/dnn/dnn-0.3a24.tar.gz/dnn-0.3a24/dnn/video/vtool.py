import cv2

def capture (path, interval = 10):
    count = 0
    vidcap = cv2.VideoCapture (path)
    latest = 0
    frames = []
    while(vidcap.isOpened ()):
        ret, image = vidcap.read ()
        frame_no =  int (vidcap.get(1))
        if latest == frame_no:
            break
        latest = frame_no         
        if frame_no % interval == 0:
            #print('Saved frame number : ' + str(int(vidcap.get(1))))
            frames.append (image)
            #cv2.imwrite("./images/frame%d.jpg" % count, image)
            #print('Saved frame%d.jpg' % count)
            count += 1
    vidcap.release ()
    return frames