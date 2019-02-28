def main():
    pass


def construct_slideshow(slides):
    """
        Tries to construct an optimal slideshow from a set of
        all slides.
    :param slides: The set of slide objects created from images.
    :return: A (probably) optimal(ish) slideshow of images.
    """

    matrix = []
    #  Calculate a fitness matrix for all slides.
    #  TODO: this is inefficient as the matrix is symmetrical, so you don't need to compute it all
    for i in range(0, len(slides)):
        for j in range(0, len(slides)):
            matrix[i][j] = fitness(slides[i], slides[j])

    #  Choose pairs of slides that maximise the fitness.
    pairs = []

    #  Select the pair with the worst left-hand slide and choose that as the starting slide

    #  Piece the rest of the slides together by selecting the best slide for the current right-hand slide

    #  Return the constructed slideshow




if __name__ == "__main__":
    main()
