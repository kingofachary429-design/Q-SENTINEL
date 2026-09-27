import cv2
import os


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

THRESHOLD = 0.363


def verify_face(show_camera=True):

    # Check required files
    required_files = [
        DETECTION_MODEL,
        RECOGNITION_MODEL,
        AUTHORIZED_FACE
    ]

    for file_path in required_files:
        if not os.path.exists(file_path):
            print("❌ Missing:", file_path)
            return False

    # Create models
    detector = cv2.FaceDetectorYN.create(
        DETECTION_MODEL,
        "",
        (640, 480),
        0.9,
        0.3,
        5000
    )

    recognizer = cv2.FaceRecognizerSF.create(
        RECOGNITION_MODEL,
        ""
    )

    # Load authorized face
    authorized_image = cv2.imread(
        AUTHORIZED_FACE
    )

    if authorized_image is None:
        print("❌ Authorized face could not be loaded.")
        return False

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

    if authorized_faces is None:
        print("❌ No face in authorized image.")
        return False

    if len(authorized_faces) != 1:
        print("❌ Authorized image must contain exactly one face.")
        return False

    # Create authorized feature
    aligned_authorized = recognizer.alignCrop(
        authorized_image,
        authorized_faces[0]
    )

    authorized_feature = recognizer.feature(
        aligned_authorized
    )

    # Camera
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("❌ Camera could not be opened.")
        return False

    print("\n📷 Face authentication started.")
    print("Look at the camera.")
    print("Press Q to cancel.")

    authenticated = False

    while True:

        success, frame = camera.read()

        if not success:
            break

        frame = cv2.flip(frame, 1)

        height, width = frame.shape[:2]

        detector.setInputSize(
            (width, height)
        )

        _, faces = detector.detect(frame)

        if faces is not None and len(faces) > 0:

            # Use first detected face
            face = faces[0]

            x, y, w, h = face[:4].astype(int)

            aligned_face = recognizer.alignCrop(
                frame,
                face
            )

            current_feature = recognizer.feature(
                aligned_face
            )

            score = recognizer.match(
                authorized_feature,
                current_feature,
                cv2.FaceRecognizerSF_FR_COSINE
            )

            if score >= THRESHOLD:

                authenticated = True
                status = "AUTHORIZED"

                print(
                    f"\nFace Score: {score:.3f}"
                )

                print("Face Authentication: PASSED ✅")

            else:

                status = "UNAUTHORIZED"

                print(
                    f"\nFace Score: {score:.3f}"
                )

                print("Face Authentication: FAILED ❌")

            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 0) if authenticated else (0, 0, 255),
                2
            )

            cv2.putText(
                frame,
                status,
                (x, max(y - 10, 30)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0) if authenticated else (0, 0, 255),
                2
            )

        else:

            cv2.putText(
                frame,
                "NO FACE DETECTED",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2
            )

        if show_camera:

            cv2.imshow(
                "Q-SENTINEL - Authentication",
                frame
            )

        # Authorized → finish
        if authenticated:
            cv2.waitKey(1000)
            break

        # Q → cancel
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()

    return authenticated