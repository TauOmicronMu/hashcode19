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
    r = float(num_shared_tags) / (float(len(a_tags) + len(b_tags)) / 2.0)

    return f, r


def file_to_images(file_name):
    """
            Takes a file and parses the text into image objects.
        :param file_name: The name of the file.
        :return: A list of all image objects.
        """
    file = open(file_name, "r")
    images = list()
    num_photos = int(file.readline())
    for i in range(0, num_photos):
        string = file.readline()
        string = string.strip("\n").split(" ")
        tags = [x for x in string[2:]]
        image = Image(i, tags, string[0] == "V")
        images.append(image)
    return images


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
    images = file_to_images("../c_short.txt")
    slides = slides_from_images(images)
    slideshow = construct_slideshow(slides)
    for slide in slideshow:
        images = slide.image
        print(str([x.image_num for x in images]))


def construct_slideshow(slides):
    """
        Tries to construct an optimal slideshow from a set of
        all slides.
    :param slides: The set of slide objects created from images.
    :return: A (probably) optimal(ish) slideshow of images.
    """

    matrix = {}
    #  Calculate a fitness matrix for all slides.
    #  TODO: this is inefficient as the matrix is symmetrical, so you don't need to compute it all
    for i in range(0, len(slides)):
        for j in range(0, len(slides)):
            i_slide_num = slides[i].image[0].image_num
            j_slide_num = slides[j].image[0].image_num
            try:
                matrix[i_slide_num][j_slide_num] = fitness(slides[i], slides[j])
            except KeyError:
                matrix[i_slide_num] = {}
                matrix[i_slide_num][j_slide_num] = fitness(slides[i], slides[j])

    #  Choose pairs of slides that maximise the fitness.
    pairs = []

    print("Started on pairs")

    #  Keep taking the first slide from slides, and find the one it has the highest fitness with.
    #  Then add this to pairs.
    while len(slides) > 1:
        slide_one = slides[0]
        slides[0].taken = True

        candidate_nums = [x for x in matrix.keys() if not [y for y in slides if y.image[0].image_num == x][0].taken]
        candidates = list()
        for i in range(0, len(candidate_nums)):
            candidates.append([x for x in slides if x.image[0].image_num == candidate_nums[i]][0])

        if len(candidates) == 0:
            slides[0].taken = True
            break

        partner = get_partner(slide_one, candidates, matrix)

        pairs.append((slide_one, partner))
        slides[slides.index(partner)].taken = True

    #  Select the pair with the worst left-hand slide and choose that as the starting slide
    #  i.e. the one with the lowest number of tags on the LHS
    #  TODO: we could do this based on the frequency of tags too?
    #        Like, use the LHS with the least, less-frequent tags
    nums = [len(x.tags) for x in slides]
    i = nums.index(min(nums))
    start_pair = pairs[i]
    pairs.remove(start_pair)

    pair_slideshow = list()
    pair_slideshow.append(start_pair)

    #  Piece the rest of the slides together by selecting the best slide for
    #  the current right-hand slide

    print("Started pairing up pairs")

    #  Get the final slide in the current slideshow
    while len(pair_slideshow) < len(pairs):
        print("Pairing loop")
        current_final_slide = pair_slideshow[-1][1]

        #  Now get the best next slide from our list of pairs
        final_slide_partner = get_partner(current_final_slide, [x for (x, y) in pairs], matrix, True)
        print("b")
        next_pair = [(x, y) for (x, y) in pairs if x.image[0].image_num == final_slide_partner.image[0].image_num]
        print("c")
        pair_slideshow.append(next_pair)
        print("d")

    #  Return the constructed slideshow
    print(pair_slideshow)

    first = pair_slideshow[0]
    rest = pair_slideshow[1:]

    ret = list()
    ret.append(first)
    for t in rest:
        ret.append(t[0])
        ret.append(t[1])

    ret2 = []
    for t in ret:
        ret2.append(t[0])
        ret2.append(t[1])

    with open('text.txt', 'w') as f:
        f.write(str(ret2))

    return ret2

def get_partner(slide, candidates, matrix, pairs=False):
    """
        Returns the optimal partner for a given slide.
    :param slide: The slide to find a partner for.
    :param candidates: all the currently non-taken slides.
    :return: The best candidate for the given slide that isn't currently taken.
    """
    try:
        slide = slide[0]
    except TypeError:
        pass
    fitness_dict = matrix[slide.image[0].image_num]
    fitnesses = [x[1] for x in fitness_dict.values()]

    print(len(candidates))

    #  Choose the best non-taken candidate.
    selected = False
    sorted_pairs = list(zip(candidates, fitnesses))
    sorted_pairs.sort(key=lambda x: -x[1])  # Sort descending on fitness
    print(sorted_pairs)
    partner_num = 0
    while not selected:
        if candidates[0].taken and not pairs:
            partner_num += 1
            continue
        selected = True

    return sorted_pairs[partner_num][0]


if __name__ == "__main__":
    main()
