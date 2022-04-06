# %%
import os
import pickle
from glob import glob


def prepare_text_for_processing(potentially_dirty_text):
    for i in "'!.,:@#$*<>()%[}?^{]=;&/\"\\\t\n":
        clean_text = potentially_dirty_text.replace(i, ' ') if (
            i in '\n;?:!.,.') else potentially_dirty_text.replace(i, '')

    # lastly ensure text uniformity by using only lowercase
    return clean_text.lower()


# build byword index from documents
def build_biword_index():
    biword_index = {}

    for index in range(len(documents)):
        # for index in range(0, len(documents)):
        current_doc = documents[index]
        with open(current_doc, "r") as f:
            doc = [a for a in prepare_text_for_processing(
            f.read()).split(" ") if a != ""]
            for i in range(len(doc) - 1):
                biword = " ".join([doc[i], doc[i + 1]])
                if biword in biword_index:
                    biword_index[biword].append(current_doc)
                else:
                    biword_index[biword] = [current_doc]

    return biword_index


# build positional index from documents
def build_positional_index():
    positional_index = {}
    for index in range(len(documents)):
        current_doc = documents[index]
        with open(current_doc, "r") as f:
            doc = [a for a in prepare_text_for_processing(
                f.read()).split(" ") if a != ""]
            for position_index, p_index in enumerate(doc):
                if p_index in positional_index:
                    positional_index[p_index].append(
                        (current_doc, position_index))
                else:
                    positional_index[p_index] = [(current_doc, position_index)]

    return positional_index


def biword_search(user_query):
    results = []
    for query in user_query:
        query.lower()  # format queries to uniform case (lowercase)
        words = query.split()
        biword = words[0] + " " + words[1]

        if biword in biword_indexes:
            results.append(biword_indexes[biword])
        else:
            results.append([])
    # sort the output
    for i in range(len(results)):
        results[i] = sorted(results[i])

    return results


def positional_search(user_query):
    results = []
    for query in user_query:
        query.lower()  # format queries to uniform case (lowercase)
        words = query.split()
        for word in words:
            if word in positional_indexes:
                results.append(positional_indexes[word])
            else:
                results.append([])

    # sort the output
    for i in range(len(results)):
        results[i] = sorted(results[i])
    return results


if __name__ == "__main__":
    working_directory = os.getcwd()

    # document resources
    documents = glob(working_directory + "/documents/file*.txt")

    # save positional index to file
    with open(working_directory + '/positional_index.pickle', 'wb') as f:
        pickle.dump(build_positional_index(), f,
                    protocol=pickle.HIGHEST_PROTOCOL)

    # save biword index to file
    with open(working_directory + '/biword_index.pickle', 'wb') as f:
        pickle.dump(build_biword_index(), f, protocol=pickle.HIGHEST_PROTOCOL)

    # load positional index from saved file
    with open(working_directory + '/positional_index.pickle', 'rb') as f:
        positional_indexes = pickle.load(f)

    # load biword index from saved file
    with open(working_directory + '/biword_index.pickle', 'rb') as f:
        biword_indexes = pickle.load(f)

    # load in the queries file
    queries = []
    with open('queries.txt', "r") as f:
        for line in f:
            queries.append(line.strip())

    print("You have provided the following queries for analysis:")
    for query in queries:
        print(f"\t- {query}")
    print()

    # biword and positional search
    biword_results = biword_search(queries)
    positional_results = positional_search(queries)

    # display results
    print(
        "---------------------------------------------------------------------------||---------------------------------------------------------------------------")

    for i in range(len(queries)):
        print("Query: " + queries[i])
        print("Size of biword index search: " + str(len(biword_results[i])))
        print("Biword index results:")
        for output in biword_results[i]:
            print(f"\t{output}")
        print()
        print("Positional index results:")
        print("Size of positional index search: " +
              str(len(positional_results[i])))
        for output in positional_results[i]:
            print(f"\t{output}")

        print(
            "---------------------------------------------------------------------------||---------------------------------------------------------------------------")

# %%
