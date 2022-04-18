from imutils import paths
import Utility as Utils


def main():
    source_dataset = 'Resources/Dataset/'
    encodings_path = 'Resources/encodings.pickle'
    faces_to_recognize_path = 'Resources/FacesToRecognize/'

    faces_to_recognize_paths = list(paths.list_images(faces_to_recognize_path))

    Utils.encode_faces(source_dataset, encodings_path)
    print("Face Encodings Obtained")

    for image_path in faces_to_recognize_paths:
        Utils.recognize_faces(image_path, encodings_path, source_dataset)


if __name__ == '__main__':
    main()
