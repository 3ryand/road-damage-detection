import cv2
import threading
stop_threads = False
class autoUpload(threading.Thread):
    def run(self):
        import time
        global stop_threads
        while True:
            if stop_threads == True:
                print("Done!")
                break
autoUpload().start()
cap = cv2.VideoCapture(0)
while True:
    success, img = cap.read()

    cv2.imshow('Preview Posisi Kamera', cv2.resize(img, (1024,600)))

    if cv2.waitKey(25) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break

stop_threads = True