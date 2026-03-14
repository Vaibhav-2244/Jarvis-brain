import face_recognition
import cv2
import os
import numpy as np

FACES_DIR = "data/faces"


class FaceRecognizer:

    def __init__(self):

        self.known_encodings = []
        self.known_names = []

        if not os.path.exists(FACES_DIR):
            os.makedirs(FACES_DIR)

        for file in os.listdir(FACES_DIR):

            path = os.path.join(FACES_DIR, file)

            image = face_recognition.load_image_file(path)
            encodings = face_recognition.face_encodings(image)

            if len(encodings) == 0:
                print(f"No face found in {file}")
                continue

            encoding = encodings[0]
            name = file.split(".")[0]

            self.known_encodings.append(encoding)
            self.known_names.append(name)

        print(f"Loaded {len(self.known_names)} known faces.")

    def recognize(self):

        cam = cv2.VideoCapture(0)

        print("Scanning face for 3 seconds...")

        frame_count = 0

        while frame_count < 30:

            ret, frame = cam.read()
            if not ret:
                continue

            frame_count += 1   # IMPORTANT: increment every frame

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            faces = face_recognition.face_locations(rgb)
            encodings = face_recognition.face_encodings(rgb, faces)

            for encoding in encodings:

                if len(self.known_encodings) == 0:
                    break

                distances = face_recognition.face_distance(
                    self.known_encodings, encoding
                )

                best_match_index = np.argmin(distances)

                if distances[best_match_index] < 0.5:

                    name = self.known_names[best_match_index]

                    cam.release()
                    cv2.destroyAllWindows()

                    return name

        cam.release()
        cv2.destroyAllWindows()

        return "unknown"

    def register_new_user(self, name):

        if len(self.known_names) >= 10:
            print("Memory full. Cannot register more users.")
            return False

        print("Please look at the camera...")

        cam = cv2.VideoCapture(0)

        encodings_list = []
        frames_captured = 0

        while frames_captured < 5:

            ret, frame = cam.read()
            if not ret:
                continue

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            faces = face_recognition.face_locations(rgb)

            if len(faces) == 0:
                continue

            encodings = face_recognition.face_encodings(rgb)

            if len(encodings) > 0:
                encodings_list.append(encodings[0])
                frames_captured += 1
                print(f"Capturing face sample {frames_captured}/5")

        cam.release()

        avg_encoding = np.mean(encodings_list, axis=0)

        self.known_encodings.append(avg_encoding)
        self.known_names.append(name)

        os.makedirs(FACES_DIR, exist_ok=True)

        image_path = os.path.join(FACES_DIR, f"{name}.jpg")

        cv2.imwrite(image_path, frame)

        print("User registered successfully.")

        return True