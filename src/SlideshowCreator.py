def fitness(a, b):
    a_tags = a.tags
    b_tags = b.tags
    shared_tags = [x for x in a_tags if x in b_tags]
    exclusive_a_tags = [x for x in a_tags if x not in shared_tags]
    exclusive_b_tags = [x for x in b_tags if x not in shared_tags]

    num_shared_tags = len(shared_tags)
    numATags = len(exclusive_a_tags)
    numBTags = len(exclusive_b_tags)

    f = min(numATags, numBTags, num_shared_tags)
    r = float(num_shared_tags) / (float(len(a_tags + len(b_tags))) / 2.0)

    return f, r


def main():
    pass


if __name__ == "__main__":
    main()
