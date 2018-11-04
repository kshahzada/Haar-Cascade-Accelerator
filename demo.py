import cv2
import os

font = cv2.FONT_HERSHEY_SIMPLEX

general_cascade = cv2.CascadeClassifier(
    # '/Users/kshahzada/OneDrive - Deloitte (O365D)/Projects/Enbridge/Enbridge OCR/Enbridge-OCR/cascades/3/cascade.xml'
    '/Users/kshahzada/OneDrive - Deloitte (O365D)/Projects/Enbridge/Enbridge OCR/Enbridge-OCR/cascades/general/cascade.xml'
    )

# initialize number cascades
number_cascades = []
for i in range(10):
    cascade_path = os.path.join(
        './cascades',
        str(i) + '/',
        'cascade.xml'
    )
    number_cascades += [cv2.CascadeClassifier(cascade_path)]

cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

while True:
    r_val, frame = vc.read()
    if frame is not None:

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        detected_numbers = general_cascade.detectMultiScale(gray, 1.3, 10)
        for (x, y, w, h) in detected_numbers:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)

        for i in range(10):
            detected_numbers = number_cascades[i].detectMultiScale(gray, 1.3, 10)

            for (x, y, w, h) in detected_numbers:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(frame, str(i), (x, y), font, 4, (255, 0, 0), 2, cv2.LINE_AA)

        cv2.imshow("preview", frame)

    if cv2.waitKey(50) & 0xFF == ord('q'):
        break


# while True:
#     r_val, frame = vc.read()
#     if frame is not None:
#
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#
#         detected_numbers = []
#         for i in range(9):
#             detected = number_cascades[i].detectMultiScale(gray, 1.3, 5)
#             detected_numbers += [i, detected]
#
#         for (x, y, w, h) in detected_numbers:
#             cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
#
#         cv2.imshow("preview", frame)
#
#     if cv2.waitKey(50) & 0xFF == ord('q'):
#         break
