from deepface import DeepFace
import cv2

class Emotions:
    def __init__(self, model_name='Emotion'):
        """
        Initializes the ImageSentiment class.

        Parameters:
        - model_name (str): The analysis action to perform. 'emotion' is used for emotion recognition.
        """
        self.model_name = model_name.lower()
        # Validate the action
        if self.model_name not in ['emotion']:
            raise ValueError("Currently, only 'emotion' analysis is supported.")
        
    def predict(self, img):
        """
        Predicts the dominant emotion in the given image.

        Parameters:
        - img (numpy.ndarray): The input image in BGR format.

        Returns:
        - dominant_emotion (str): The detected dominant emotion.
        - emotions (dict): A dictionary with emotion scores.
        """
        try:
            if isinstance(img, str):
                # Load the image if the input is a file path
                img = cv2.imread(img)
            # DeepFace expects RGB images
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            analysis = DeepFace.analyze(img_rgb, actions=[self.model_name], enforce_detection=False, detector_backend='ssd')[0]
            dominant_emotion = analysis['dominant_emotion']
            emotions = analysis['emotion']
            return dominant_emotion, emotions
        except Exception as e:
            # Handle exceptions (e.g., no face detected)
            print(f"Error in emotion prediction: {e}")
            return None, None
    

def main():
    # Initialize webcam (0 is the default camera)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    # Initialize ImageSentiment
    sentiment_analyzer = Emotions()

    # Define font for text display
    font = cv2.FONT_HERSHEY_SIMPLEX

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        # Optionally, resize the frame for faster processing
        # frame = cv2.resize(frame, (640, 480))

        # Predict emotion
        dominant_emotion, emotions = sentiment_analyzer.predict(frame)

        if dominant_emotion:
            # Display the dominant emotion on the top-left corner
            cv2.putText(frame,
                        dominant_emotion.capitalize(),
                        (30, 50),
                        font,
                        1,
                        (0, 255, 0),
                        2,
                        cv2.LINE_AA)
        else:
            # If no emotion detected, display 'No Face'
            cv2.putText(frame,
                        "No Face Detected",
                        (30, 50),
                        font,
                        1,
                        (0, 0, 255),
                        2,
                        cv2.LINE_AA)

        # Optionally, display all emotion probabilities
        # Uncomment the following lines to see detailed emotions
        """
        if emotions:
            y_offset = 80
            for emotion, score in emotions.items():
                text = f"{emotion.capitalize()}: {score:.2f}"
                cv2.putText(frame,
                            text,
                            (30, y_offset),
                            font,
                            0.6,
                            (255, 255, 255),
                            1,
                            cv2.LINE_AA)
                y_offset += 20
        """

        # Display the resulting frame
        cv2.imshow('Emotion Detection', frame)

        # Exit when 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()