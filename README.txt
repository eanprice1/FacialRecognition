Facial Recognition

How It Works
        128 dimension encodings are calculated for every image in the "Resources/Dataset/" directory. Each directory
    within the Dataset directory has a persons name. Each directory only contains images of the same person. The
    directory names are used as identifiers for the images within. Once all encodings are calculated, an encoding to name
    map is stored in a dump file. Images of unknown people are stored in the "Resources/FacesToRecognize/" directory.
    This directory is the source of all candidate images that will be compared against the previously calculated
    encodings to name map. The encoding of each image in this directory is calculated and compared to the data stored
    in the dump file. The system then keeps track of "votes" or the number of matches with each known person. The name
    that ends up having the most votes or matches with the candidate image is then determined to be the identity of the
    provided candidate image.

Understanding Results
        When a facial match is found, the program will display two images. The first image will be the candidate image
    with title "Unknown: <person's name>". The second image will be a picture of the person that the candidate image
    matched with. This image will be titled "Actual: <person's name>". If no match was found or there was not enough
    evidence to prove a match then only the candidate image will be displayed with the title "Unknown: Unknown". If two
    images are displayed, but they are of different people then this is a false positive match.