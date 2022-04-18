import os
import pickle
import cv2
import face_recognition
from imutils import paths


def convert_images(source_directory: str, target_directory: str, target_format: str):

    for folder in os.listdir(source_directory):
        subdirectory = os.path.join(source_directory, folder)
        new_subdirectory = os.path.join(target_directory, folder)

        if os.path.exists(new_subdirectory) is False:
            os.makedirs(new_subdirectory)
            print(f'Directory Created: {new_subdirectory}')

        for filename in os.listdir(subdirectory):
            image_path = os.path.join(subdirectory, filename)

            begin_extension_index = filename.find(".")
            filename = filename[0: begin_extension_index] + f'.{target_format}'

            new_image_path = os.path.join(new_subdirectory, filename)
            new_image_path = new_image_path.replace("\\", "/")

            image = cv2.imread(image_path)
            cv2.imwrite(new_image_path, image, [cv2.IMWRITE_JPEG_QUALITY, 100])


def encode_faces(source_directory: str, target_encodings: str):
    image_paths = list(paths.list_images(source_directory))

    known_encodings = []
    known_names = []

    for (i, image_path) in enumerate(image_paths):
        name = image_path.split(os.path.sep)[-2]
        name = name.split("/")[2]

        image = cv2.imread(image_path)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        boxes = face_recognition.face_locations(rgb, model='hog')

        encodings = face_recognition.face_encodings(rgb, boxes)

        for encoding in encodings:
            known_encodings.append(encoding)
            known_names.append(name)

        print(f'Completed Encoding for {name}')

    data = {"encodings": known_encodings, "names": known_names}
    f = open(target_encodings, 'wb')
    f.write(pickle.dumps(data))
    f.close()


def recognize_faces(image_path: str, source_encodings: str, source_dataset: str):
    data = pickle.loads(open(source_encodings, 'rb').read())

    image = cv2.imread(image_path)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    boxes = face_recognition.face_locations(rgb, model='hog')

    encodings = face_recognition.face_encodings(rgb, boxes)

    names = []

    for encoding in encodings:
        matches = face_recognition.compare_faces(data['encodings'], encoding)
        name = 'Unknown'

        if True in matches:
            matched_indexes = [i for (i, b) in enumerate(matches) if b]
            counts = {}

            for i in matched_indexes:
                name = data['names'][i]
                counts[name] = counts.get(name, 0) + 1

            name = max(counts, key=counts.get)

        if counts[name] > 3:
            names.append(name)
        else:
            names.append('Unknown')

    for name in names:
        larger_image = resize_image(rgb, 300, cv2.INTER_CUBIC)
        print(f'Name: {name}')
        cv2.imshow(f'Unknown: {name}', larger_image)

        if name != 'Unknown':
            actual = cv2.imread(f'{source_dataset}{name}/1.jpg')
            actual = resize_image(actual, 300, cv2.INTER_CUBIC)
            cv2.imshow(f'Actual: {name}', actual)

        cv2.waitKey()
        cv2.destroyAllWindows()


def resize_image(image, scale_percent: int, interpolation: int):
    (h, w, _) = image.shape
    dimensions = aspect_ratio_resize(w, h, scale_percent)
    return cv2.resize(image, dimensions, fx=0, fy=0, interpolation=interpolation)


def aspect_ratio_resize(width, height, scale_percent: int):
    width = int(width * scale_percent / 100)
    height = int(height * scale_percent / 100)
    return width, height
