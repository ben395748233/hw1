"""
Copyright 2025 Evan Huang @nptu
"""

import re
import sys


class InvertedIndex:
    """
    A simple inverted index as explained in lecture.
    """

    def __init__(self) -> None:
        """
        Creates an empty inverted index.
        """
        self.inverted_lists: dict[str, list[int]] = {}  # The inverted lists of record ids.
        self.docs: list[tuple[str, str, str, str, str]] = []

    def build_from_file(self, file_name: str)-> None:
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

                
                

                parts: list[str] = line.split("\t", 4)
                title: str = parts[0] if len(parts) > 0 else ""
                description: str = parts[1] if len(parts) > 1 else ""
                large: str = parts[2] if len(parts) > 2 else ""
                float_i: str = parts[3] if len(parts) > 3 else ""
                integer: str = parts[4] if len(parts) > 4 else ""
                self.docs.append((title, description, large, float_i, integer))

                text: str = f"{title} {description} {large} {float_i} {integer}"
                

                seen_in_record: set[str] = set() 
                for word in re.split("[^A-Za-z0-9]+", text):
                    word: str = word.lower().strip()
                    if not word:
                        continue
                    if word in seen_in_record:
                        continue
                    seen_in_record.add(word)

                    lst: list[int] | None = self.inverted_lists.get(word)
                    if lst is None:
                        self.inverted_lists[word] = [record_id]
                    else:
                        if not lst or lst[-1] != record_id:
                            lst.append(record_id)

    def intersect(self, list1: list[int], list2: list[int]) -> list[int]:
        """
        Computes the intersection of two sorted inverted lists in linear time.
        Precondition: list1 and list2 are strictly increasing lists of integers.
        """
        i, j = 0, 0
        n1, n2 = len(list1), len(list2)
        out: list[int] | None = []
        while i < n1 and j < n2:
            a: int = list1[i]
            b: int = list2[j]
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

    def process_query(self, keywords: list[str])-> list[int] | None:
        """
        Processes the given keyword query:
        - Fetch inverted list for each keyword (case-insensitive).
        - If any keyword is missing, return [].
        - Intersect all lists using self.intersect.
        """
        # 空查詢 → 空結果（符合 doctest）
        if not keywords:
            return []

        # 依序抓倒排列表；若有缺少的關鍵字，直接空集合
        lists: list[list[int]] = []
        for kw in keywords:
            kw: str = kw.lower()
            lst: list[int] | None = self.inverted_lists.get(kw)
            if not lst:
                return []
            lists.append(lst)

        # 先交集最短的，減少中間結果大小
        lists.sort(key=len)

        # 逐一交集（使用上題的 intersect，線性合併）
        result: list[int] = lists[0]
        for lst in lists[1:]:
            result = self.intersect(result, lst)
            if not result:      # 交集已空，提前結束
                break
        return result


def main() -> None:
    """
    Constructs an inverted index from a given text file, then asks the user in
    an infinite loop for keyword queries and outputs the title and description
    of up to three matching records.
    """
    # Parse the command line arguments.
    if len(sys.argv) != 2:
        print("Usage: python3 %s <file>" % sys.argv[0])
        sys.exit(1)

    file_name: str = sys.argv[1]

    # Create a new inverted index from the given file.
    print("Reading from file '%s'." % file_name)
    ii = InvertedIndex()
    ii.build_from_file(file_name)

    # Interactive query loop
    print("Enter keywords separated by spaces (type 'quit' to exit).")
    while True:
        try:
            q: str = input("query> ")
        except (EOFError, KeyboardInterrupt):
            print("\nBye.")
            break

        q = q.replace("\u00A0", " ").replace("\u3000", " ").strip()  # 防 NBSP/全形空白
        if not q:
            continue
        if q.lower() in {"quit", "exit", ":q"}:
            print("Bye.")
            break

        keywords: list[str] = re.split(r"\s+", q)
        rids: list[int] | None = ii.process_query(keywords)

        if not rids:
            print("(no results)")
            continue

        for rid in rids:
            title, desc, large, float_i, integer = ii.docs[rid - 1]  # record_id 是 1-based
            print(f"Title:\t{title}\nDescription:\t{desc}\nCol3:\t{large}\nCol4:\t{float_i}\nCol5:\t{integer}")



if __name__ == "__main__":
    main()
