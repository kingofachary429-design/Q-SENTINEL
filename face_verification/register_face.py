import cv2
import os
import time


MODEL_PATH = os.path.join(
    "face_verification",
    "models",
    "face_detection_yunet_2026may.onnx"
)

DATA_DIR = os.path.join(
    "face_verification",
    "data"
)

FACE_IMAGE = os.path.join(
    DATA_DIR,
    "authorized_face.jpg"
)


def main():

    print("================================")
    print("        Q-SENTINEL")
    print("   Authorized Face Setup")
    print("================================")

    # Check model
    if not os.path.exists(MODEL_PATH):
        print("\n❌ YuNet model not found.")
        print("Expected:")
        print(MODEL_PATH)
        return

    # Create data directory
    os.makedirs(DATA_DIR, exist_ok=True)

    # Open camera
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("\n❌ Camera could not be opened.")
        return

    detector = cv2.FaceDetectorYN.create(
        MODEL_PATH,
        "",
        (640, 480),
        0.9,
        0.3,
        5000
    )

    print("\nCamera ready ✅")
    print("Look directly at the camera.")
    print("Keep your face clearly visible.")
    print("\nCapturing in:")

    for number in [3, 2, 1]:
        print(number)
        time.sleep(1)

    captured = False

    while True:

        success, frame = camera.read()

        if not success:
            print("❌ Camera frame error.")
            break

        frame = cv2.flip(frame, 1)

        height, width = frame.shape[:2]

        detector.setInputSize((width, height))

        _, faces = detector.detect(frame)

        face_count = 0

        if faces is not None:
            face_count = len(faces)

        cv2.putText(
            frame,
            f"Faces detected: {face_count}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (255, 255, 255),
            2
        )

        if face_count == 1:

            face = faces[0]

            x, y, w, h = face[:4].astype(int)

            # Add small margin around face
            margin = 30

            x1 = max(0, x - margin)
            y1 = max(0, y - margin)

            x2 = min(width, x + w + margin)
            y2 = min(height, y + h + margin)

            face_crop = frame[y1:y2, x1:x2]

            if face_crop.size > 0:

                cv2.imwrite(
                    FACE_IMAGE,
                    face_crop
                )

                captured = True

                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + w, y + h),
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    frame,
                    "FACE CAPTURED",
                    (x, max(y - 10, 20)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                    2
                )

        cv2.imshow(
            "Q-SENTINEL - Face Registration",
            frame
        )

        if captured:
            cv2.waitKey(1500)
            break

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()

    if captured:

        print("\n================================")
        print("AUTHORIZED FACE REGISTERED ✅")
        print("================================")

        print("\nSaved locally:")
        print(FACE_IMAGE)

        print("\n⚠ Do NOT upload this file to GitHub.")

    else:

        print("\n❌ Face registration cancelled.")


if __name__ == "__main__":
    main()