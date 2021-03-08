import json
import datetime
from typing import Dict, List

class ScoreFileIO:

    # class constants, don't use annotations in constants, it
    # doesn't work in all cases so don't try

    # top level key in the json file
    _THE_SCORE_KEY = "the_scores"

    # key strings in individual score dict
    SCORE_KEY = 'score'
    NAME_KEY = 'name'
    DATE_KEY = 'date'

    # a single default score dictionary
    _SCORE_DEFAULT = {SCORE_KEY: 9999, NAME_KEY: 'None', DATE_KEY: '03-01-2021'}

    # the max number of scores to display and save in the file
    # note: public constant
    MAX_SCORES = 4

    # initialize and set the score file name
    def __init__(self, fname='') -> None:

        self._score_list: List[Dict[str: int, str: str, str: str]] = []
        self._fname: str = fname

    # end init


    def make_default_score_list(self) -> List[any]:

        # make a list of default score dictionary values
        scores: List[Dict[str: int, str: str, str: str]] = []
        for _ in range(self.MAX_SCORES):
            scores.append(self._SCORE_DEFAULT)

        return scores
    # end make_default_score_list


    # read the scored from the file
    def read_in_scores(self) -> None:

        try:

            fp = open(self._fname, 'r')

        except IOError:

            # make a list of default score dictionary values
            self._score_list = self.make_default_score_list()

        else:

            try:
                # score_list is an in-memory representation of json file list
                # of dictionaries
                self._score_list = json.load(fp)[self._THE_SCORE_KEY]

            except ValueError:

                # make a list of default score dictionary values
                self._score_list = self.make_default_score_list()

            else:
                fp.close()

    # end read_in_scores


    # -> List[Dict[str: int, str: str, str: str]]
    def get_score_list(self) -> List[any]:
        return self._score_list
    # end get_score_list


    # add a new score dict to the
    def add_new_score(self, score: int, name: str) -> int:
        ret: int = -1

        # add new item to _score_list
        new_date = datetime.datetime.now().strftime("%m-%d-%Y")
        new_score_dict = {self.SCORE_KEY: score, self.NAME_KEY: name, self.DATE_KEY: new_date}
        self._score_list = sorted(self._score_list, key=lambda k: k[self.SCORE_KEY])
        # self._score_list.append(new_score_dict)

        # sort acending on _SCORE_KEY, low scores are better
        # use linear search to insert a new score dict, saving the index as the return
        for idx in range(len(self._score_list)):
            if score <= self._score_list[idx][self.SCORE_KEY]:
                self._score_list.insert(idx, new_score_dict)
                ret = idx
                break

        # keep the size to _MAX_SCORES in top (low) scores
        while len(self._score_list) > self.MAX_SCORES:
            self._score_list.pop()

        return ret
    # end add_new_score


    # run this after add_new_score()
    def save_scores(self) -> None:

        # make a new high score dictionary
        score_dict = {self._THE_SCORE_KEY: self._score_list}

        # save over the original json file
        fp = open(self._fname, 'w')
        json.dump(score_dict, fp, indent=3)
        fp.close()

    # end save_scores

    # test if score belongs in the top scores
    def is_leader(self, score: int) -> bool:
        ret: bool = False

        # get the max score (longest time) value
        max_score: int = max(self._score_list, key=lambda k: k[self.SCORE_KEY])[self.SCORE_KEY]
        if score <= max_score:
            ret = True

        return ret
    # end is_leader


if __name__ == "__main__":
    sf = ScoreFileIO("topscores.json")
    sf.read_in_scores()
    sl = sf.get_score_list()
    print(sl)
    leader = sf.is_leader(150)
    print(leader)
    sf.add_new_score(150,'BooBoo Bear')
    sf.save_scores()


