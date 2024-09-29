import cv2
import mediapipe as mp
import numpy as np

class GazeDetector:
    def __init__(self, 
                 max_num_faces=1, 
                 detection_confidence=0.7, 
                 track_confidence=0.7):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=max_num_faces,
            refine_landmarks=True,  # Enables iris landmarks
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=track_confidence)
        
        # Define iris landmarks based on MediaPipe's Face Mesh
        self.LEFT_IRIS = [468, 469, 470, 471, 472]
        self.RIGHT_IRIS = [473, 474, 475, 476, 477]
        
        # Define eye contours for visualization and further processing
        self.LEFT_EYE_LANDMARKS = [
            33, 7, 163, 144, 145, 153, 154, 155, 133, 173,
            157, 158, 159, 160, 161, 246
        ]
        self.RIGHT_EYE_LANDMARKS = [
            362, 382, 381, 380, 374, 373, 390, 249, 263, 466,
            388, 387, 386, 385, 384, 398
        ]
        
        # MediaPipe drawing specifications (optional, for debugging)
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles

    def get_gaze_direction(self, image):
        """
        Processes the input image and returns the gaze points for detected faces.
        """
        # Convert the BGR image to RGB before processing.
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_image)

        gaze_points = []

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # Get image dimensions
                h, w, _ = image.shape

                # Get iris centers
                left_iris = self._get_iris_center(face_landmarks, self.LEFT_IRIS, w, h)
                right_iris = self._get_iris_center(face_landmarks, self.RIGHT_IRIS, w, h)

                # Get eye regions for calculating gaze direction
                left_eye_region = self._get_eye_region(face_landmarks, self.LEFT_EYE_LANDMARKS, w, h)
                right_eye_region = self._get_eye_region(face_landmarks, self.RIGHT_EYE_LANDMARKS, w, h)

                # Calculate gaze direction for each eye
                left_gaze = self._calculate_gaze_direction(left_iris, left_eye_region)
                right_gaze = self._calculate_gaze_direction(right_iris, right_eye_region)

                # Average the gaze directions
                avg_gaze = (
                    int((left_gaze[0] + right_gaze[0]) / 2),
                    int((left_gaze[1] + right_gaze[1]) / 2)
                )
                gaze_points.append(avg_gaze)

        return gaze_points, results.multi_face_landmarks

    def _get_iris_center(self, landmarks, iris_indices, image_width, image_height):
        """
        Calculates the center of the iris based on the iris landmarks.
        """
        iris_x = []
        iris_y = []
        for idx in iris_indices:
            x = int(landmarks.landmark[idx].x * image_width)
            y = int(landmarks.landmark[idx].y * image_height)
            iris_x.append(x)
            iris_y.append(y)
        
        if len(iris_x) == 0 or len(iris_y) == 0:
            return (0, 0)
        
        center_x = int(np.mean(iris_x))
        center_y = int(np.mean(iris_y))
        return (center_x, center_y)

    def _get_eye_region(self, landmarks, eye_indices, image_width, image_height):
        """
        Extracts the eye region based on the provided eye landmark indices.
        """
        eye_points = []
        for idx in eye_indices:
            x = int(landmarks.landmark[idx].x * image_width)
            y = int(landmarks.landmark[idx].y * image_height)
            eye_points.append((x, y))
        return eye_points

    def _calculate_gaze_direction(self, iris_center, eye_region):
        """
        Estimates the gaze direction based on the iris center position within the eye region.
        """
        if iris_center == (0, 0):
            # Default gaze point if iris center is not detected
            return (0, 0)
        
        # Calculate the bounding rectangle of the eye region
        eye_region_np = np.array(eye_region, dtype=np.int32)
        x_min = np.min(eye_region_np[:, 0])
        x_max = np.max(eye_region_np[:, 0])
        y_min = np.min(eye_region_np[:, 1])
        y_max = np.max(eye_region_np[:, 1])
        
        # Normalize the iris position within the eye region
        norm_x = (iris_center[0] - x_min) / (x_max - x_min)
        norm_y = (iris_center[1] - y_min) / (y_max - y_min)
        
        # Define gaze direction based on normalized positions
        # Here, we map the normalized positions to screen coordinates
        # You can adjust the scaling factors as needed
        screen_x = int(norm_x * 100)  # Example scaling
        screen_y = int(norm_y * 100)  # Example scaling
        
        return (screen_x, screen_y)
    
    def isFocused(self, image, thresh=0.1):
        ##  It is focused if the iris points are within -thresh to thresh from the range 
        ##  of each eye's x coordinates
        ##  If the iris points' y coordinates are more than 5% apart, it is not focused
        gaze_points, face_landmarks_list = self.get_gaze_direction(image)
        left_iris_center = self._get_iris_center(face_landmarks_list[0], self.LEFT_IRIS, image.shape[1], image.shape[0])
        right_iris_center = self._get_iris_center(face_landmarks_list[0], self.RIGHT_IRIS, image.shape[1], image.shape[0])
        left_eye_region = self._get_eye_region(face_landmarks_list[0], self.LEFT_EYE_LANDMARKS, image.shape[1], image.shape[0])
        right_eye_region = self._get_eye_region(face_landmarks_list[0], self.RIGHT_EYE_LANDMARKS, image.shape[1], image.shape[0])
        ##  Check x coordinates...
        left_x = [point[0] for point in left_eye_region]
        right_x = [point[0] for point in right_eye_region]
        left_range = (min(left_x), max(left_x))
        right_range = (min(right_x), max(right_x))
        left_focused = 0.5 - thresh < (left_iris_center[0] - left_range[0]) / (left_range[1] - left_range[0]) < 0.5 + thresh
        right_focused = 0.5 - thresh < (right_iris_center[0] - right_range[0]) / (right_range[1] - right_range[0]) < 0.5 + thresh
        ##  Check y coordinates...
        left_y = left_iris_center[1]
        right_y = right_iris_center[1]
        y_focused = abs(left_y - right_y) < 0.02 * image.shape[0]
        return left_focused and right_focused and y_focused


def main():
    # Initialize webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    # Initialize GazeDetector
    gaze_detector = GazeDetector()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        # Optionally, resize frame for performance (commented out for accurate scaling)
        # frame = cv2.resize(frame, (640, 480))

        # Get gaze points and face landmarks
        gaze_points, face_landmarks_list = gaze_detector.get_gaze_direction(frame)
        # print('Face Landmarks:', face_landmarks_list)

        # Visualize gaze points
        for point in gaze_points:
            if point != (0, 0):
                # Draw iris center
                cv2.circle(frame, point, 5, (0, 255, 0), -1)
                
                # Draw gaze direction line (adjust the scaling as needed)
                # Here, we draw a line from the iris center upwards
                end_point = (point[0], point[1] - 50)  # Example: 50 pixels upwards
                cv2.line(frame, point, end_point, (255, 0, 0), 2)

        # Optional: Draw eye contours and iris centers for debugging
        if face_landmarks_list:
            for face_landmarks in face_landmarks_list:
                # Get image dimensions
                h, w, _ = frame.shape

                # Draw left eye contour
                left_eye_region = gaze_detector._get_eye_region(face_landmarks, gaze_detector.LEFT_EYE_LANDMARKS, w, h)
                cv2.polylines(frame, [np.array(left_eye_region, dtype=np.int32)], isClosed=True, color=(0, 255, 255), thickness=1)

                # Draw right eye contour
                right_eye_region = gaze_detector._get_eye_region(face_landmarks, gaze_detector.RIGHT_EYE_LANDMARKS, w, h)
                cv2.polylines(frame, [np.array(right_eye_region, dtype=np.int32)], isClosed=True, color=(0, 255, 255), thickness=1)

                # Draw iris centers
                left_iris_center = gaze_detector._get_iris_center(face_landmarks, gaze_detector.LEFT_IRIS, w, h)
                right_iris_center = gaze_detector._get_iris_center(face_landmarks, gaze_detector.RIGHT_IRIS, w, h)
                cv2.circle(frame, left_iris_center, 3, (255, 0, 255), -1)
                cv2.circle(frame, right_iris_center, 3, (255, 0, 255), -1)
                

        cv2.putText(frame, f"Focused: {gaze_detector.isFocused(frame)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        # Display the frame
        cv2.imshow('Gaze Detection', frame)


        # Exit on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()