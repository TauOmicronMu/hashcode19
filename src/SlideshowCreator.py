from pprint import pprint
import Image
import Slide


def fitness(a, b):
    a_tags = a.tags
    b_tags = b.tags
    shared_tags = [x for x in a_tags if x in b_tags]
    exclusive_a_tags = [x for x in a_tags if x not in shared_tags]
    exclusive_b_tags = [x for x in b_tags if x not in shared_tags]

    num_shared_tags = len(shared_tags)
    num_a_tags = len(exclusive_a_tags)
    num_b_tags = len(exclusive_b_tags)

    f = min(num_a_tags, num_b_tags, num_shared_tags)
    r = float(num_shared_tags) / (float(len(a_tags + len(b_tags))) / 2.0)

    return f, r


# pass file name and will return a list of Image objects
def file_to_images(file_name):
    file = open(file_name, "r")
    images = []
    num_photos = file.readline()
    for i in range(0, num_photos):
        str = file.readline()
        str.splitline(" ")
        tags = [x for x in str[2:]]

        image = Image(i, tags, str[0] == "V")
        images.append(image)
    return images


def main():
    pprint(file_to_images("a_example.txt"))


def construct_slideshow(slides):
    """
        Tries to construct an optimal slideshow from a set of
        all slides.
    :param slides: The set of slide objects created from images.
    :return: A (probably) optimal(ish) slideshow of images.
    """

    matrix = []
    #  Calculate a fitness matrix for all slides.
    #  TODO: this is inefficient as the matrix is symmetrical, so you don't
    #  need to compute it all
    for i in range(0, len(slides)):
        for j in range(0, len(slides)):
            matrix[i][j] = fitness(slides[i], slides[j])

    #  Choose pairs of slides that maximise the fitness.
    pairs = []

    #  Select the pair with the worst left-hand slide and choose that as the
    #  starting slide

    #  Piece the rest of the slides together by selecting the best slide for
    #  the current right-hand slide

    #  Return the constructed slideshow


if __name__ == "__main__":
    main()
