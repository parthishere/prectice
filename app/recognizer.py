import cv2
import face_recognition
import os
import numpy as np
from imutils.video import VideoStream 


class RecognizerClass(object):
    
    def __init__(self, details=None, username=None, unique_id=None):
        self.threshold = 0
        self.threshold_for_unknown = 0
        
        self.username = username
 
        self.unique_id = unique_id
        self.details = details
        self.proceed_login = False
        
        
        ###################################
        


        self.known_face_encodings = []
        self.known_face_names = []

        # base_dir = os.path.dirname(os.path.abspath(__file__))
        # image_dir = os.path.join(base_dir, "static")
        # image_dir = os.path.join(image_dir, "profile_pics")

        # base_dir = os.getcwd()
        base_dir = os.path.dirname(os.path.abspath(__file__))
        # os.chdir("..")
        base_dir = os.getcwd()
        image_dir = os.path.join(base_dir,"{}\{}".format('media','User_images'))
        # print(image_dir)
        self.names = []
        self.proceed_login = False


        for root,dirs,files in os.walk(image_dir):
            for file in files:
                if file.endswith('jpeg') or file.endswith('jpg') or file.endswith('png'):
                    path = os.path.join(root, file)
                    img = face_recognition.load_image_file(path)
                    label = file[:len(file)-4]
                    img_encoding = face_recognition.face_encodings(img)[0]
                    self.known_face_names.append(label)
                    self.known_face_encodings.append(img_encoding)

        self.face_locations = []
        self.face_encodings = []
        
        self.video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        # self.vs = VideoStream(src=0).start()

    def __del__(self):
        self.video.release()
        cv2.destroyAllWindows()
        # self.check_login_proceed()
        

    def get_frame(self):
        
        # self.frame = self.vs.read()\
        self.ret , self.frame = self.video.read()
        try:
            small_frame = cv2.resize(self.frame, (0,0), fx=0.5, fy= 0.5, interpolation=cv2.INTER_AREA)
        except:
            pass

        rgb_small_frame = small_frame[:,:,::-1]

        self.face_locations = face_recognition.face_locations(rgb_small_frame)
        self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)
        self.face_names = []


        for face_encoding in self.face_encodings:

            matches = face_recognition.compare_faces(self.known_face_encodings, np.array(face_encoding), tolerance = 0.6)

            face_distances = face_recognition.face_distance(self.known_face_encodings,face_encoding)	
            
            try:
                matches = face_recognition.compare_faces(self.known_face_encodings, np.array(face_encoding), tolerance = 0.6)

                face_distances = face_recognition.face_distance(self.known_face_encodings,face_encoding)
                best_match_index = np.argmin(face_distances)

                if matches[best_match_index]:
                    name = self.known_face_names[best_match_index]
                    self.face_names.append(name)
                    if name not in self.names:
                        self.names.append(name)
            except:
                pass

        if len(self.face_names) == 0:
            for (top,right,bottom,left) in self.face_locations:
                top*=2
                right*=2
                bottom*=2
                left*=2

                cv2.rectangle(self.frame, (left,top),(right,bottom), (0,0,255), 2)

                # cv2.rectangle(frame, (left, bottom - 30), (right,bottom - 30), (0,255,0), -1)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(self.frame, 'Unknown', (left, top), font, 0.8, (255,255,255),1)
                self.proceed_login = False
        else:
            for (top,right,bottom,left), name in zip(self.face_locations, self.face_names):
                top*=2
                right*=2
                bottom*=2
                left*=2

                cv2.rectangle(self.frame, (left,top),(right,bottom), (0,255,0), 2)

                # cv2.rectangle(frame, (left, bottom - 30), (right,bottom - 30), (0,255,0), -1)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(self.frame, name, (left, top), font, 0.8, (255,255,255),1)
                if (self.username+self.unique_id) in name:
                    self.proceed_login = True
                else:
                    self.proceed_login = False
                    
        # user = self.details['user']

        # if str(self.username + self.unique_id) in self.names:
        #     user.login_proceed = self.proceed_login
        #     user.save()
        
            

        # cv2.imshow('frame', self.frame)
        ret, jpeg = cv2.imencode('.jpg', self.frame)
        
        # if cv2.waitKey(0) & 0xFF == ord('q'):
            
            
        
        # return (self.names, self.known_face_names, self.proceed_login, jpeg.tobytes())
        print("str :"+str(jpeg))
        print("naems :"+str(self.names))
        print("known names :"+str(self.known_face_names))
        print("proceed login :"+str(self.proceed_login))
        
        return jpeg.tobytes()