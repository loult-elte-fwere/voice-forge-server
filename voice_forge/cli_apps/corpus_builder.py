import argparse
import operator
from itertools import product, chain
from pathlib import Path
import json
import logging
from typing import Dict, List, Set, Tuple, Iterable

import voxpopuli
from tqdm import tqdm

argparser = argparse.ArgumentParser()
argparser.add_argument("input", type=Path,
                       help="Path of words list or phonemized words list's json")
argparser.add_argument("-pj", "--pho_json", action="store_true",
                       help="Indicates that the input is a phonemized json file")
argparser.add_argument("-o", "--output", type=Path,
                       help="Output path for the selected words")
argparser.add_argument("-v", "--verbose", action="store_true",
                       help="Verbose mode")
argparser.add_argument("-l", "--language", type=str, default="fr",
                       help="Language for phonemization")

Diphone = Tuple[str, str]
DiphoneList = List[Diphone]
DiphoneSet = Set[Diphone]


def phones_to_diphones(pho_list: List[str]) -> DiphoneList:
    return list(zip(pho_list[:-1], pho_list[1:]))


class WordSet:

    def __init__(self, words: Dict[str, DiphoneSet] = None):
        self.words: Dict[str, DiphoneSet] = dict() if not word else words
        self._current_diphones: Set[Diphone] = set(chain.from_iterable(self.words.values()))

    @property
    def diphone_set(self):
        return self._current_diphones

    def add_word(self, word: str, diphones: DiphoneSet):
        self.words[word] = diphones
        self._current_diphones.update(diphones)

    def remove_word(self, word: str, update_diphone_set=False):
        del self.words[word]

        if update_diphone_set:
            self._current_diphones = set(chain.from_iterable(self.words.values()))

    def __iter__(self):
        return iter(self.words.items())

    def __getitem__(self, word: str):
        return self.words[word]


if __name__ == "__main__":
    args = argparser.parse_args()
    logging.getLogger().setLevel(logging.DEBUG if args.verbose else logging.INFO)

    pho_dict: Dict[str, List[str]] = {}
    voice = voxpopuli.Voice(lang=args.language)

    if not args.pho_json:
        logging.info(f"Loading word list {args.input}")
        with open(args.input) as wordlist_file:
            wordlist = wordlist_file.read().split("\n")

        logging.info("Phonemizing the words list...")
        for word in tqdm(wordlist):
            word = word.strip()
            phonemized_word = voice.to_phonemes(word)
            phonemes = [pho.name for pho in phonemized_word if pho.name != "_"]
            pho_dict[word] = phonemes
        pho_json_path = args.input.parent / Path(args.input.stem + ".json")
        logging.info(f"Done phonemizing. Saving phonemized JSON at {pho_json_path}")
        with open(pho_json_path, "w") as json_file:
            json.dump(pho_dict, json_file)

    else:
        logging.info(f"Loading json file {args.input}")
        with open(args.input) as json_file:
            pho_dict = json.load(json_file)

    logging.info("Converting phone form to diphone form")
    diphone_dict = {word: set(phones_to_diphones(pho_list)) for
                    word, pho_list in pho_dict.items()}

    logging.info("Beginning to search for optimal word set for the phoneme set...")

    pho_set = voxpopuli.main.lg_code_to_phonem[args.language]._all
    all_diphones_set = set(product(pho_set, pho_set))
    logging.info(f"There are {len(pho_set)} phonemes, which translates "
                 f"into {len(all_diphones_set)} potential diphones")

    logging.info("Running maximum-cover algorithm to find the best word subset..")
    remaining_words = WordSet(diphone_dict)
    selected_words = WordSet()
    with tqdm(total=len(all_diphones_set)) as pbar:
        while len(all_diphones_set) > len(selected_words.diphone_set):
            intersection_lengths = {}
            for word, word_diphones in remaining_words:
                intersection_len = len(word_diphones - selected_words.diphone_set)
                if intersection_len == 0:
                    continue
                intersection_lengths[word] = intersection_len

            if not intersection_lengths:
                logging.info("Couldn't find any more words to add to the selected words set. Ending.")

            best_word = max(intersection_lengths.items(), key=operator.itemgetter(1))[0]
            logging.debug(f"Adding word f{best_word}, which adds {intersection_lengths[best_word]} to the "
                          f"selected word set")
            selected_words.add_word(best_word, remaining_words[best_word])
            remaining_words.remove_word(best_word)
            pbar.update(intersection_lengths[best_word])

            if not remaining_words.words:
                logging.debug("No more words to add. Ending.")
                break

    if args.output:
        with open(args.output, "w") as output_file:
            for word, _ in selected_words:
                output_file.write(word + "\n")