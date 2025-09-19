"""
Copyright 2025 Evan Huang @nptu
"""

import re
import sys


class InvertedIndex:
    """
    A simple inverted index as explained in lecture.
    """

    def __init__(self):
        """
        Creates an empty inverted index.
        """
        self.inverted_lists = {}  # The inverted lists of record ids.
        self.docs = []

    def build_from_file(self, file_name):
        """
        Constructs the inverted index from given file in linear time 
        (linear in the number of words in the file). 
        The expected format of the file is one record per line, in the format
        <title>TAB<description>TAB<num_ratings>TAB<rating>TAB<num_sitelinks>
        You can ignore the last three columns for now.

        TODO: Make sure that each inverted list contains a particular record id
        at most once, even if the respective word occurs multiple times in the
        same record.

        >>> ii = InvertedIndex()
        >>> ii.build_from_file("example.tsv")
        >>> sorted(ii.inverted_lists.items())
        [('a', [1, 2]), ('doc', [1, 2, 3]), ('film', [2]), ('movie', [1, 3])]
        """
        with open(file_name, "r",newline="") as file:
            record_id = 0
            for line in file:
                record_id += 1
                line = line.strip()
                # Get the title and the text
                # title, text, rest = line.split("\t", 2)
                #print("%s %s" % (title, text)

                # # Index both title and the text
                # text = title + " " + text
                # # Iterate over all words in the text
                # for word in re.split("[^A-Za-z]+", text):
                #     print(word)

                
                

                parts = line.split("\t", 4)
                title = parts[0] if len(parts) > 0 else ""
                description = parts[1] if len(parts) > 1 else ""
                self.docs.append((title, description))

                text = f"{title} {description}"
                

                seen_in_record = set() 
                for word in re.split("[^A-Za-z]+", text):
                    word = word.lower().strip()
                    if not word:
                        continue
                    if word in seen_in_record:
                        continue
                    seen_in_record.add(word)

                    lst = self.inverted_lists.get(word)
                    if lst is None:
                        self.inverted_lists[word] = [record_id]
                    else:
                        if not lst or lst[-1] != record_id:
                            lst.append(record_id)

    def intersect(self, list1, list2):
        """
    Computes the intersection of two sorted inverted lists in linear time.
    Precondition: list1 and list2 are strictly increasing lists of integers.
    """
        i, j = 0, 0
        n1, n2 = len(list1), len(list2)
        out = []
        while i < n1 and j < n2:
            a = list1[i]
            b = list2[j]
            if a == b:
                if not out or out[-1] != a:  
                    out.append(a)
                i += 1
                j += 1
            elif a < b:
                i += 1
            else:
                j += 1
        return out

    def process_query(self, keywords):
        """
        Processes the given keyword query as follows: Fetches the inverted list
        for each of the keywords in the given query and computes the
        intersection of all inverted lists (which is empty, if there is a
        keyword in the query which has no inverted list in the index).

        >>> ii = InvertedIndex()
        >>> ii.build_from_file("example.tsv")
        >>> ii.process_query([])
        []
        >>> ii.process_query(["doc"])
        [1, 2, 3]
        >>> ii.process_query(["doc", "movie"])
        [1, 3]
        >>> ii.process_query(["doc", "movie", "comedy"])
        []
        """
        pass  # TODO: add your code here


def main():
    """
    Constructs an inverted index from a given text file, then asks the user in
    an infinite loop for keyword queries and outputs the title and description
    of up to three matching records.
    """
    # Parse the command line arguments.
    if len(sys.argv) != 2:
        print("Usage: python3 %s <file>" % sys.argv[0])
        sys.exit()

    file_name = sys.argv[1]

    # Create a new inverted index from the given file.
    print("Reading from file '%s'." % file_name)
    ii = InvertedIndex()
    ii.build_from_file(file_name)
    print(ii.inverted_lists)
    
    # #Zif's law
    # for word, inverted_list in ii.inverted_lists.items():
    #     print("%d\t%s" % (len(inverted_list), word))


    # TODO: add your code here


if __name__ == "__main__":
    main()
