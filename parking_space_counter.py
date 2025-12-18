import cv2
import pickle


cap = cv2.VideoCapture('video_input/parking.mp4') # Load the video

with open('park_positions','rb') as f: # read binary
    park_positions = pickle.load(f)    # restore object was saved 

font = cv2.FONT_HERSHEY_COMPLEX_SMALL


#Parking space parameters

width,height = 40,23
full = width * height # rectangle
empty = 0.22



def parking_space_counter(img_processed):
    global counter #global variable


    counter = 0

    for position in park_positions:
        x,y  = position


        img_crop = img_processed[y:y + height,x:x + width]
#(x, y)  ┌──────────────┐
#        │              │
#        │   Parkinglot │
#        │              │
#        └──────────────┘
#                        (x+width, y+height)        
        count = cv2.countNonZero(img_crop)  # count pixel white which is not equal to zero


        ratio = count/full

        if ratio< empty:
            color = (0, 255, 0)  # If parking lot is empty , make it green colour
            counter += 1
        else:
            color = (0, 0, 255) # else make it red

        cv2.rectangle(overlay, position, (position[0] + width, position[1] + height), color, -1)
        cv2.putText(overlay, "{:.2f}".format(ratio), (x + 4, y + height - 4), font, 0.7, (255, 255, 255), 1, cv2.LINE_AA)


while True:

    #video looping
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)

    _,frame = cap.read()
    overlay = frame.copy()


    # image processing
    img_gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) # make the image into gray colour
    img_blur = cv2.GaussianBlur(img_gray,(3,3),1) # blur the image
    img_thresh = cv2.adaptiveThreshold(img_blur,255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,25,16) # make image into binary , only has dark(0) and white(255) colours

    parking_space_counter(img_thresh)

    alpha = 0.7
    frame_new = cv2.addWeighted(overlay,alpha,frame,1-alpha,0)


    #create counter
    w, h = 220, 60
    cv2.rectangle(frame_new, (0, 0), (w, h), (255, 0, 255),-1)
    cv2.putText(frame_new, f"{counter}/{len(park_positions)}", (int(w / 10), int(h * 3 / 4)), font, 2, (255, 255, 255), 2, cv2.LINE_AA)

    cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
    #cv2.setWindowProperty('frame', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    cv2.imshow('frame', frame_new)
    #cv2.imshow('image_blur', img_blur)
    #cv2.imshow('image_thresh', img_thresh)

    if cv2.waitKey(1) & 0xFF == 27: # exit by clicking esc
        break

cap.release()
cv2.destroyAllWindows()
