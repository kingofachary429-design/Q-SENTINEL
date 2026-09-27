import cv2
import os
import numpy as np


DETECTION_MODEL = os.path.join(
    "face_verification",
    "models",
    "face_detection_yunet_2026may.onnx"
)

RECOGNITION_MODEL = os.path.join(
    "face_verification",
    "models",
    "face_recognition_sface_2021dec.onnx"
)

AUTHORIZED_FACE = os.path.join(
    "face_verification",
    "data",
    "authorized_face.jpg"
)


def main():

    print("================================")
    print("        Q-SENTINEL")
    print("    Face Verification")
    print("================================")

    # Check files
    for path, name in [
        (DETECTION_MODEL, "YuNet model"),
        (RECOGNITION_MODEL, "SFace model"),
        (AUTHORIZED_FACE, "Authorized face")
    ]:

        if not os.path.exists(path):
            print(f"\n❌ {name} not found:")
            print(path)
            return

    print("\nModels and authorized face: READY ✅")

    # Create detector
    detector = cv2.FaceDetectorYN.create(
        DETECTION_MODEL,
        "",
        (640, 480),
        0.9,
        0.3,
        5000
    )

    # Create SFace recognizer
    recognizer = cv2.FaceRecognizerSF.create(
        RECOGNITION_MODEL,
        ""
    )

    # Load authorized face
    authorized_image = cv2.imread(
        AUTHORIZED_FACE
    )

    if authorized_image is None:
        print("\n❌ Could not load authorized face.")
        return

    # Detect authorized face
    detector.setInputSize(
        (
            authorized_image.shape[1],
            authorized_image.shape[0]
        )
    )

    _, authorized_faces = detector.detect(
        authorized_image
    )

    if authorized_faces is None or len(authorized_faces) == 0:
        print("\n❌ No face found in authorized image.")
        return

    if len(authorized_faces) > 1:
        print("\n❌ Multiple faces found in authorized image.")
        return

    # Align and crop authorized face
    authorized_aligned = recognizer.alignCrop(
        authorized_image,
        authorized_faces[0]
    )

    # Generate authorized face feature
    authorized_feature = recognizer.feature(
        authorized_aligned
    )

    print("Authorized face feature: READY ✅")

    # Open camera
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("\n❌ Camera could not be opened.")
        return

    print("\nCamera: CONNECTED ✅")
    print("Look at the camera.")
    print("Press Q to exit.")

    while True:

        success, frame = camera.read()

        if not success:
            print("❌ Camera frame error.")
            break

        frame = cv2.flip(frame, 1)

        height, width = frame.shape[:2]

        detector.setInputSize(
            (width, height)
        )

        _, faces = detector.detect(frame)

        if faces is not None:

            for face in faces:

                x, y, w, h = face[:4].astype(int)

                # Align detected face
                aligned_face = recognizer.alignCrop(
                    frame,
                    face
                )

                # Generate current face feature
                current_feature = recognizer.feature(
                    aligned_face
                )

                # Cosine similarity
                score = recognizer.match(
                    authorized_feature,
                    current_feature,
                    cv2.FaceRecognizerSF_FR_COSINE
                )

                # SFace example threshold
                if score >= 0.363:

                    status = "AUTHORIZED ✅"
                    text_color = (0, 255, 0)

                else:

                    status = "UNAUTHORIZED ❌"
                    text_color = (0, 0, 255)

                # Draw face box
                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + w, y + h),
                    text_color,
                    2
                )

                # Display score
                cv2.putText(
                    frame,
                    f"Score: {score:.3f}",
                    (x, max(y - 35, 20)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    text_color,
                    2
                )

                # Display authorization
                cv2.putText(
                    frame,
                    status,
                    (x, max(y - 10, 45)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    text_color,
                    2
                )

        else:

            cv2.putText(
                frame,
                "NO FACE DETECTED",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (0, 0, 255),
                2
            )

        cv2.imshow(
            "Q-SENTINEL - Face Verification",
            frame
        )

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()

    print("\nFace verification stopped.")


if __name__ == "__main__":
    main()