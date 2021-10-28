import cv2
import numpy as np
import face_recognition
import os
from _datetime import datetime

path = r'C:\Users\HP\Desktop\AttendeeFaces'
images = []
attendeeNames = []
myList = os.listdir(path)

for i in myList:
    pImg = cv2.imread(f'{path}/{i}')
    images.append(pImg)
    # Adding all the images names to a attendeeNames list
    attendeeNames.append(os.path.splitext(i)[0])
print("Total attendee names:")
for i in attendeeNames:
    print(i)

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # face_encodings gives 128 measurements to face to uniquely identify it
        # it generates nearly the same numbers (measurement) when looking at two different pictures of the same person.
        enMy = face_recognition.face_encodings(img)[0]
        # in case you want to see 128 measurements uncomment below print
        # print(enMy)
        encodeList.append(enMy)
    return encodeList

def markAttendance(name):
    # Just to keep it simple we store present attendees names in CSV file
    # if you want, can connect it with database with use of MongoDB, phpMyAdmin
    with open('Attendance.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        print(myDataList)
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name}, {dtString}')
            markAttendance(name)


encodeList = findEncodings(images)
print('Ready To Start')
# Opening the default camera
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    # # resizing image for computational purpose (1/4 size)
    # imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Will output a tuple with 4 different points (location of face)
    facesCurFrame = face_recognition.face_locations(imgS)
    # To determine 128 measurements on face
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        # face_distance simply gives the difference between the known_face_encodings & face_encoding_to_check
        # compare_faces gives True/False values indicating which known_face_encodings match the face encoding to check
        matches = face_recognition.compare_faces(encodeList, encodeFace)
        faceDis = face_recognition.face_distance(encodeList, encodeFace)
        # print(faceDis)
        # Gives the index number from list(faceDis) of minimum value
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = attendeeNames[matchIndex].upper()
            if faceDis[matchIndex] > 0.55:
                name = "Unknown"
            # print(name)
            list1 = []
            # as we have resized the image before, now to change it in it's original form
            for i in faceLoc:
                list1.append(i*4)
            y1, x1, y2, x2 = faceLoc
            # for bounding the face with rectangle box
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2-15), (x2, y2), (0, 255, 0), cv2.FILLED)
            # for putting the name below
            cv2.putText(img, name, (x2, y2+30), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)

    cv2.imshow('webcam', img)
    cv2.waitKey(1)

