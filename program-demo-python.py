import numpy as np
import cv2
import time
import os
import serial
import threading
import tensorflow as tf
from firebase import firebase
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util
stop_threads = False
sukses_upload = 0
class autoUpload (threading.Thread):
  def run(self):
    import mysql.connector
    import os
    import time
    import shutil
    from datetime import datetime
    from urllib.request import urlopen
    from ftplib import FTP
    def internet_on():
      try:
        urlopen('https://google.com', timeout=1)
        return True
      except:
        return False
    global stop_threads
    #def while1():
    #while:
    global sukses_upload
    HOSTNAME = "ftp.automata.masuk.id"
    USERNAME = "autoupload@automata.masuk.id"
    PASSWORD = "PuS+B#d2ZM}Q"
    ftp_server = FTP(HOSTNAME, USERNAME, PASSWORD)
    ftp_server.encoding = "utf-8"
    print("sukses konek ftp")
    conn = mysql.connector.connect(
      host="103.55.39.44", 
      user="automat1_admin", 
      passwd="92ZG+fkg(cNs",
      db="automat1_web_pemetaan")
    mycursor = conn.cursor()
    print("sukses konek db")
    frameList = []
    now = datetime.now()
    dt_string = now.strftime("%d%m%Y%H%M%S")
    folder_pindah = dt_string
    os.mkdir("" + folder_pindah)
    global stop_threads
    while True:
      files = os.listdir("hasil_deteksi")
      for f in files:
        localpath = os.path.join("hasil_deteksi/", f)
        if os.path.isfile(localpath):
          x = f.split("_", )
          y = x[2].split(".jpg", )
          frameTimeNow = x[0]
          ket = x[1]
          koor = y[0]
          val = (f, koor, ket)
          #for list in frameList:
          if frameTimeNow not in frameList:
            with open(localpath, "rb") as file:
              print("Kerusakan terdeteksi, mengupload foto " + f)
              ftp_server.storbinary(f"STOR {f}", file)
            query = "INSERT INTO gambar_data (nama_gambar,lokasi,keterangan) VALUES (%s, %s, %s)"
            mycursor.execute(query, val)
            conn.commit()
            shutil.move(localpath, "" + folder_pindah)
            sukses_upload +=1
            frameList.append(frameTimeNow)
      if stop_threads == True:
        break
    #while1()
    #while (internet_on()==False):
      #internet_on()
      #print(internet_on())
      #if internet_on():
        #while1()
        #break

#FirebaseURL = "https://projectkuliah-b0f85-default-rtdb.firebaseio.com/"
#firebase = firebase.FirebaseApplication(FirebaseURL, None)
#print("konekfb")
config = ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.60
config.gpu_options.allow_growth = True
session = InteractiveSession(config=config)

#cap = cv2.VideoCapture('../percobaan1/test_video2cut4.mp4')
cap = cv2.VideoCapture(0)
MODEL_NAME = 'ssdlite_1'
PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'
PATH_TO_LABELS = MODEL_NAME + '/label_map.pbtxt'
NUM_CLASSES = 3

detection_graph = tf.Graph()
with detection_graph.as_default():
  od_graph_def = tf.compat.v1.GraphDef()
  with tf.compat.v2.io.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
    serialized_graph = fid.read()
    od_graph_def.ParseFromString(serialized_graph)
    tf.import_graph_def(od_graph_def, name='')

label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)
prev_frame_time = 0
new_frame_time = 0
jeda = 0
counter = 0
currentFrame = 0
ser = serial.Serial('COM3', 9800, timeout=0)
autoUpload().start()
lokList = []
with detection_graph.as_default():
  with tf.compat.v1.Session(graph=detection_graph) as sess:
    while True:
      ret, image_np = cap.read()
      new_frame_time = time.time()
      fps = 1/(new_frame_time-prev_frame_time)
      prev_frame_time = new_frame_time
      fps = str(int(fps))
      cv2.putText(image_np, 'fps : ' + fps, (7, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 255, 0), 2, cv2.LINE_AA)
      image_np_expanded = np.expand_dims(image_np, axis=0)
      image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
      boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
      scores = detection_graph.get_tensor_by_name('detection_scores:0')
      classes = detection_graph.get_tensor_by_name('detection_classes:0')
      num_detections = detection_graph.get_tensor_by_name('num_detections:0')
      # Actual detection.
      (boxes, scores, classes, num_detections) = sess.run(
          [boxes, scores, classes, num_detections],
          feed_dict={image_tensor: image_np_expanded})
      # Visualization of the results of a detection.
      vis_util.visualize_boxes_and_labels_on_image_array(
          image_np,
          np.squeeze(boxes),
          np.squeeze(classes).astype(np.int32),
          np.squeeze(scores),
          category_index,
          use_normalized_coordinates=True,
          max_boxes_to_draw=1,
          line_thickness=4)
      lokasi = ser.readline().decode().strip()
      #result = firebase.get('/gpsdarihp', '')
      cv2.putText(image_np, 'Lokasi: ' + lokasi, (700, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 255, 0), 2, cv2.LINE_AA)
      cv2.putText(image_np, 'Kerusakan Tersimpan: ' + str(currentFrame), (700, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 255, 0), 2, cv2.LINE_AA)
      cv2.putText(image_np, 'Data Upload: ' + str(sukses_upload), (700, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 255, 0), 2, cv2.LINE_AA)
      for kelas in classes[0]:
        if jeda == 0 and scores[0][0] >= 0.8 and kelas == 2.0:
          #result = firebase.get('/gpsdarihp', '')
          kerusakan = "Retak"
          jeda = 1
          currentFrame += 1
          namaFileCapture = 'hasil_deteksi/' + str(currentFrame) + '_' + kerusakan +'_'+ lokasi + '.jpg'
          #namaFileCapture2 = 'hasil_deteksi/' + str(currentFrame) + '_' + kerusakan +'_'+ result.strip('\"') + '.jpg'
          cv2.imwrite(namaFileCapture, image_np)
          #cv2.imwrite(namaFileCapture2, image_np)
          #lokList.append(lokasi)
        if jeda == 0 and scores[0][0] >= 0.7 and kelas == 3.0:
          #result = firebase.get('/gpsdarihp', '')
          kerusakan = "Lubang"
          jeda = 1
          currentFrame += 1
          namaFileCapture = 'hasil_deteksi/' + str(currentFrame) + '_' + kerusakan +'_'+ lokasi + '.jpg'
          #namaFileCapture2 = 'hasil_deteksi/' + str(currentFrame) + '_' + kerusakan +'_'+ result.strip('\"') + '.jpg'
          cv2.imwrite(namaFileCapture, image_np)
          #cv2.imwrite(namaFileCapture2, image_np)
          #lokList.append(lokasi)
      if jeda == 1:
        counter = counter + 1
        if counter == 20:
          jeda = 0
          counter = 0
        
      cv2.imshow('Pengujian Keseluruhan Sistem', cv2.resize(image_np, (1024,600)))
      if cv2.waitKey(1) & 0xFF == ord('q'):
        stop_threads = 1
        cv2.destroyAllWindows()
        break
stop_threads = True