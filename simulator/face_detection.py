import cv2
import os


MODEL_PATH = os.path.join(
    "face_verification",
    "models",
    "face_detection_yunet_2026may.onnx"
)


def main():

    print("================================")
    print("        Q-SENTINEL")
    print("     Face Detection")
    print("================================")

    # Check model
    if not os.path.exists(MODEL_PATH):
        print("\n❌ Face detection model not found!")
        print("\nExpected location:")
        print(MODEL_PATH)
        print("\nPlease place the YuNet ONNX model there.")
        return

    print("\nModel: FOUND ✅")

    # Open camera
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("❌ Camera could not be opened.")
        return

    print("Camera: CONNECTED ✅")
    print("\nStarting face detection...")
    print("Press Q to exit.")

    # Create YuNet face detector
    detector = cv2.FaceDetectorYN.create(
        MODEL_PATH,
        "",
        (640, 480),
        0.9,
        0.3,
        5000
    )

    while True:

        success, frame = camera.read()

        if not success:
            print("❌ Failed to read camera frame.")
            break

        # Mirror camera
        frame = cv2.flip(frame, 1)

        height, width = frame.shape[:2]

        # Set current frame size
        detector.setInputSize((width, height))

        # Detect faces
        _, faces = detector.detect(frame)

        face_count = 0

        if faces is not None:

            face_count = len(faces)

            for face in faces:

                # First 4 values = x, y, width, height
                x, y, w, h = face[:4].astype(int)

                # Draw face rectangle
                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + w, y + h),
                    (0, 255, 0),
                    2
                )

                # Detection confidence
                confidence = face[-1]

                label = f"FACE {confidence:.2f}"

                cv2.putText(
                    frame,
                    label,
                    (x, max(y - 10, 20)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2
                )

        # Status
        if face_count == 0:

            status = "NO FACE DETECTED"

        elif face_count == 1:

            status = "FACE DETECTED"

        else:

            status = f"{face_count} FACES DETECTED"

        cv2.putText(
            frame,
            status,
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (255, 255, 255),
            2
        )

        # Show window
        cv2.imshow(
            "Q-SENTINEL - Face Detection",
            frame
        )

        # Press Q to exit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Release camera
    camera.release()

    # Close windows
    cv2.destroyAllWindows()

    print("\nCamera stopped.")
    print("Q-SENTINEL face detection test completed.")


if __name__ == "__main__":
    main()