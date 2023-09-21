import os
import random
import uuid
from ultralytics import YOLO
import cv2
import winsound

def random_hex_name():
    if not hasattr(random_hex_name, "first_call"):
        random_hex_name.first_call = int(uuid.uuid4().hex[:8], 16)
        random_hex_name.counter = 1
        return hex(random_hex_name.first_call)[2:]
    else:
        random_hex_name.counter += 1
        return hex(random_hex_name.first_call + random_hex_name.counter)[2:]

def is_blurred(image, threshold=100):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Calculate the Laplacian of the grayscale image
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)

    # Calculate the variance of the Laplacian
    variance = laplacian.var()

    # Determine if the image is blurred or not based on the variance
    blurred = variance < threshold

    return blurred, variance


    
def main():
    cap = cv2.VideoCapture(0)
    model_path = os.path.join('.', 'runs', 'detect', '1000images2', 'weights', 'best.pt')
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Load a model
    model = YOLO(model_path)  # load a custom model
    threshold = 0.5
    while True:
        ret, frame = cap.read()
 
        if not ret:
            break
            
        resized_frame = cv2.resize(frame, (width//1, height//1))
        frame2 = resized_frame.copy()
        results = model(resized_frame)[0]
        print(results.orig_shape)
        # results.save_txt()


        for result in results.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = result
            if score > threshold:
                name = model.names[int(class_id)].upper()
                cv2.rectangle(resized_frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
                cv2.putText(resized_frame, "{} {:.2f}".format(name, score), (int(x1), int(y1 - 10)),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)
                
        blurred, variance = is_blurred(frame2)
        variance_str = f"{variance:.2f}"
        text = f"Blurry: {blurred}, Variance: {variance_str}"
        color = (0, 0, 255) if blurred else (0, 255, 0)

        # Put the text on the image
        font = cv2.FONT_HERSHEY_SIMPLEX
        # cv2.putText(resized_frame, text, (10, 30), font, 1, color, 2, cv2.LINE_AA)

        cv2.imshow('Video', resized_frame)

        # Exit when 'q' is pressed
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('m') or key == ord(' '):
            random_name = random_hex_name()
            save_path = os.path.join("prateleiras", f"{random_name}.png")
            cv2.imwrite(save_path, frame2)
            print(f"Image saved as {save_path}")
            winsound.Beep(800, 500)

    cap.release()
    cv2.destroyAllWindows()

def main2():
    cap = cv2.VideoCapture(1)
    cap2 = cv2.VideoCapture(2)
    model_path = os.path.join('.', 'runs', 'detect', 'extralarge', 'weights', 'last.pt')
    
    # Load a model
    model = YOLO(model_path)  # load a custom model
    threshold = 0.5
    while True:
        ret, frame = cap.read()
        _, frame_2 = cap2.read()
 
        if not ret:
            break

        frame2 = frame.copy()
        results = model(frame)[0]
        results2 = model(frame_2)[0]


        for result in results.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = result
            if score > threshold:
                name = model.names[int(class_id)].upper()
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
                cv2.putText(frame, "{} {:.2f}".format(name, score), (int(x1), int(y1 - 10)),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)
        
        for result in results2.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = result
            if score > threshold:
                name = model.names[int(class_id)].upper()
                cv2.rectangle(frame_2, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
                cv2.putText(frame_2, "{} {:.2f}".format(name, score), (int(x1), int(y1 - 10)),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)

        cv2.imshow('Logitech', frame)
        cv2.imshow("Lifecam", frame_2)

        # Exit when 'q' is pressed
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('m') or key == ord(' '):
            random_name = random_hex_name()
            save_path = os.path.join("notlabeledimages", f"{random_name}.png")
            cv2.imwrite(save_path, frame2)
            print(f"Image saved as {save_path}")
            winsound.Beep(800, 500)

    cap.release()
    cv2.destroyAllWindows()


def show_video():
    webcam = cv2.VideoCapture(0)
    logitech = cv2.VideoCapture(1)
    lifecam = cv2.VideoCapture(2)

    while True:
        print("oi")
        ret, frame = webcam.read()
        _, frame2 = logitech.read()
        _, frame3 = lifecam.read()
 
        if not ret:
            break


        cv2.imshow('Webcam', frame)
        cv2.imshow('Logitech', frame2)
        cv2.imshow('Lifecam', frame3)

        # Exit when 'q' is pressed
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('m') or key == ord(' '):
            random_name = random_hex_name()
            save_path = os.path.join("notlabeledimages", f"{random_name}.png")
            cv2.imwrite(save_path, frame2)
            print(f"Image saved as {save_path}")
            winsound.Beep(800, 500)

    lifecam.release()
    logitech.release()
    webcam.release()
    cv2.destroyAllWindows()

main()
# show_video()
#record_video()
# main2()