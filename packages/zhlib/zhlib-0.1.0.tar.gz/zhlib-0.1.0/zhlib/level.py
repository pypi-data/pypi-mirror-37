from wordfreq import word_frequency
from pathlib import Path
import json
import regex
import math

from . import db
from .util import find_hanzi, find_vocab


class Level:
    def __init__(self):
        self.freq_level = []
        with Path(__file__).with_name('freq.json').open() as f:
            self.freq = json.load(f)
            for k, v in self.freq.items():
                self.freq_level.append((k, v['max'], ))

        self.freq_level = sorted(self.freq_level)

    def vocab_get_freq_level(self, vocab):
        freq = word_frequency(vocab, 'zh') * 10 ** 6
        for i, (level, freq_max) in enumerate(self.freq_level):
            if freq > freq_max:
                if i > 0:
                    return self.freq_level[i-1][0], freq
                else:
                    return self.freq_level[0][0], freq

        return None, freq

    @classmethod
    def hanzi_get_level(cls, hanzi):
        db_hanzi = db.Hanzi.get_or_none(hanzi=hanzi)
        if db_hanzi:
            return db_hanzi.junda

    def vocab_get_level(self, vocab):
        level1 = None
        db_vocab = db.Vocab.search(vocab=vocab)
        if db_vocab:
            level = sorted(t.name for t in db_vocab[0].tags if regex.match(r'HSK_Level_\d+', t.name))
            if level:
                level1 = level[0]
            else:
                level1 = None

        level2, freq = self.vocab_get_freq_level(vocab)

        try:
            if level1 < level2:
                return level1, freq
            else:
                return level2, freq
        except TypeError:
            if level1:
                return level1, freq

        return level2, freq

    def search_text(self, text):
        def _vocab_sorter(x):
            if x['level']:
                return int(regex.sub(r'[^\d]', '', x['level'])) * 10**6 - x['frequency']
            elif x['frequency']:
                return 10 * 10**6 - x['frequency']
            else:
                return math.inf

        return {
            'hanzi': sorted(self._search_hanzi(text), key=lambda x: x['number'] if x['number'] else math.inf),
            'vocab': sorted(self._search_vocab(text), key=_vocab_sorter)
        }

    def _search_hanzi(self, text):
        for hanzi in find_hanzi(text):
            level = self.hanzi_get_level(hanzi)
            db_hanzi = db.Hanzi.get_or_none(hanzi=hanzi)
            if db_hanzi:
                hanzi_dict = db_hanzi.to_json()
            else:
                hanzi_dict = {
                    'hanzi': hanzi
                }

            yield {
                'number': level,
                **hanzi_dict
            }

    def _search_vocab(self, text):
        for vocab in find_vocab(text):
            level, freq = self.vocab_get_level(vocab)
            db_vocab = db.Vocab.search(vocab)
            if db_vocab:
                vocab_dict = db_vocab[0].to_json()
            else:
                vocab_dict = {
                    'simplified': vocab
                }

            yield {
                'level': level,
                'frequency': freq,
                **vocab_dict
            }
