from flask import Flask, request, jsonify
from deepface import DeepFace
import os
import cv2
import tempfile

app = Flask(__name__)

KNOWN_FACES_DIR = "known_faces"

@app.route('/match', methods=['POST'])
def match_faces():
    if 'group_photo' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    # Save uploaded image temporarily
    image_file = request.files['group_photo']
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
    image_path = temp_file.name
    image_file.save(image_path)

    results = []

    for filename in os.listdir(KNOWN_FACES_DIR):
        student_path = os.path.join(KNOWN_FACES_DIR, filename)
        try:
            verification = DeepFace.verify(img1_path=student_path, img2_path=image_path, enforce_detection=False)
            if verification['verified']:
                student_id = filename.split('_')[0]
                student_name = "_".join(filename.split('_')[1:]).split('.')[0]
                results.append({
                    "id": student_id,
                    "name": student_name,
                    "distance": verification['distance']
                })
        except Exception as e:
            print("Error verifying", filename, e)

    os.remove(image_path)

    return jsonify({"present_students": results})

if __name__ == '__main__':
    app.run(debug=True)