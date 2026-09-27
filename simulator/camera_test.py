import cv2


def main():
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("❌ Camera could not be opened")
        return

    print("✅ Camera connected")
    print("Press Q to close the camera.")

    while True:
        success, frame = camera.read()

        if not success:
            print("❌ Failed to read camera")
            break

        cv2.imshow("Q-SENTINEL Camera Test", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()