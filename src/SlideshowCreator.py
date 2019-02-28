from pprint import pprint
from Image import Image
from Slide import Slide
import operator

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


def file_to_images(file_name):
    """
            Takes a file and parses the text into image objects.
        :param file_name: The name of the file.
        :return: A list of all image objects.
        """
    file = open(file_name, "r")
    images = []
    num_photos = int(file.readline())
    for i in range(0, num_photos):
        string = file.readline()
        string = string.strip("\n").split(" ")
        tags = [x for x in string[2:]]
        image = Image(i, tags, string[0] == "V")
        images.append(image)
    return images


def slides_to_file(slides, file_name):
    file = open(file_name, "w")
    file.write(str(len(slides)))
    for x in slides[1:]:
        out = ""
        for y in x.image:
            out += str(y.image_num) + " "
        file.write(out + "\n")


def pair_images(images):
    avg_tags = float(sum([len(x.tags) for x in images])) / float(len(images))
    paired_images = []
    working_images = images
    while len(working_images) > 0:
        base_image = working_images[0]
        fitnesses = {}
        for (j, image) in enumerate(working_images[1:]):
            total_tags = len(base_image.tags) + len(list(set(image.tags) - set(base_image.tags)))
            intersecting = len([x for x in base_image.tags if x in image.tags])
            optimal_tags = 2 * avg_tags
            fitnesses[image] = (optimal_tags - abs(optimal_tags - total_tags)) - intersecting
        fittest = max(fitnesses.items(), key=operator.itemgetter(1))
        paired_images.append((base_image, fittest[0]))
        working_images.remove(fittest[0])
        working_images.remove(base_image)
    for i in paired_images:
        print(i[0].tags, i[1].tags)
    return paired_images


def slides_from_images(images):
    return [Slide([x]) for x in images if not x.vertical] +\
           [Slide([x, y]) for x, y in pair_images([z for z in images if z.vertical])]


def main():
    file_name = "c_memorable_moments.txt"
    images = file_to_images("../" + file_name)
    slides = slides_from_images(images)

    slides_to_file(slides, "../" + file_name[0:1] + "_output.txt")

def construct_slideshow(slides):
    """
        Tries to construct an optimal slideshow from a set of
        all slides.
    :param slides: The set of slide objects created from images.
    :return: A (probably) optimal(ish) slideshow of images.
    """

    matrix = {}
    #  Calculate a fitness matrix for all slides.
    #  TODO: this is inefficient as the matrix is symmetrical, so you don't
    #  need to compute it all
    for i in range(0, len(slides)):
        for j in range(0, len(slides)):
            matrix[i.image[0].image_num][j.image[0].image_num] = fitness(slides[i], slides[j])

    #  Choose pairs of slides that maximise the fitness.
    pairs = []

    #  Select the pair with the worst left-hand slide and choose that as the
    #  starting slide
    #  Keep taking the first slide from slides, and find the one it has the highest fitness with.
    while len(slides) > 1:
        slide_one = slides[0]
        slides[0].taken = True
        fitness_dict = matrix[slide_one.image[0].image_num]
        candidates = fitness_dict.keys()
        fitnesses = [x[1] for x in fitness_dict.values()]
        partner = [x for (x, y) in zip(candidates, fitnesses) if y == max(fitnesses)]


    #  Select the pair with the worst left-hand slide and choose that as the starting slide

    #  Piece the rest of the slides together by selecting the best slide for
    #  the current right-hand slide

    #  Return the constructed slideshow


if __name__ == "__main__":
    main()
