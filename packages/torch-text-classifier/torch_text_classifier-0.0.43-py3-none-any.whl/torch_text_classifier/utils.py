import json
import re
import sys
from collections import Counter
from typing import List, Optional, Tuple

import numpy as np

import torch
from sklearn.utils import shuffle
from tqdm import tqdm

if torch.cuda.is_available():
    print('CUDA is online', file=sys.stderr)
else:
    print('CUDA is offline', file=sys.stderr)

DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
START_TAG = '<START>'
STOP_TAG = '<STOP>'
PAD_TAG = '<PAD>'
UNK_TAG = '<UNK>'
NORMAL_WORD = re.compile(r'\d')


def normalize_word(word: str) -> str:
    """normalize number"""
    word = re.sub(NORMAL_WORD, '0', word)
    return word


def json_reader(path: str, max_len: Optional[int] = None) -> Tuple[List, List]:
    """Read a json file, and return data
    data should follow this json format:
    [
        ["sentence", "sentence_tag"],
        ["sentence 2", "sentence_tag_2"],
    ]
    """
    with open(path, 'r') as fobj:
        data = json.load(fobj)

    data = [(sent, tag) for sent, tag in data
            if len(sent.strip()) > 0 and len(tag.strip()) > 0]

    if max_len is None:
        x_data = [list(normalize_word(x[0])) for x in tqdm(data, ncols=0)]
    else:
        x_data = [
            list(normalize_word(x[0][:max_len])) for x in tqdm(data, ncols=0)
        ]
    y_data = [x[1] for x in data]
    return x_data, y_data


def build_vocabulary(x_data: list, y_data: list, limit: int = 1) -> dict:
    """ Use data to build vocabulary"""
    sentence_word = Counter()
    sentence_word_char = Counter()
    tags_word = Counter()
    for sentence in x_data:
        sentence_word.update(sentence)
    for tags in y_data:
        tags_word.update(tags)

    word_to_ix = {PAD_TAG: 0, UNK_TAG: 1}
    for word, count in sentence_word.items():
        sentence_word_char.update(list(word))
        if word not in word_to_ix and count >= limit:
            indx = len(word_to_ix)
            word_to_ix[word] = indx

    char_to_ix = {PAD_TAG: 0, UNK_TAG: 1}

    for char, count in sentence_word_char.items():
        if count >= limit:
            indx = len(char_to_ix)
            char_to_ix[char] = indx

    ix_to_char = {v: k for k, v in char_to_ix.items()}

    ix_to_word = {v: k for k, v in word_to_ix.items()}

    tag_to_ix = {}

    tag_words = sorted(set(y_data))
    for tag in tag_words:
        indx = len(tag_to_ix)
        tag_to_ix[tag] = indx

    ix_to_tag = {v: k for k, v in tag_to_ix.items()}

    return {
        'word_to_ix': word_to_ix,
        'ix_to_word': ix_to_word,
        'tag_to_ix': tag_to_ix,
        'ix_to_tag': ix_to_tag,
        'char_to_ix': char_to_ix,
        'ix_to_char': ix_to_char
    }


def pad_seq(seq: list, max_len: int, pad: int = 0) -> list:
    """Padding data to max_len length"""
    if len(seq) < max_len:
        return seq + [pad] * (max_len - len(seq))
    return seq


def prepare_sequence(seq: list, to_ix: dict) -> torch.LongTensor:
    """Convert sequence to torch variable"""
    idxs = [to_ix[w] if w in to_ix else to_ix[UNK_TAG] for w in seq]
    return idxs


def extract_char_features(x_batch: list, char_max_len: int, char_to_ix: dict,
                          max_len: int) -> Tuple[list, list]:
    """extract char features"""
    char_batch = []
    char_len_batch = []
    for xseq in x_batch:
        sentence_char = []
        len_char = []
        for char in xseq:
            if re.match(r'^[\u4e00-\u9fff]+$', char):
                # Process Chinese
                from pypinyin import lazy_pinyin
                char = ' '.join([x[0] for x in lazy_pinyin(char)])
            char = char[:char_max_len]
            len_char.append(len(char))
            char = prepare_sequence(char, char_to_ix)
            char = pad_seq(char, char_max_len)
            sentence_char.append(char)
        while len(sentence_char) < max_len:
            sentence_char.append([0] * char_max_len)
        while len(len_char) < max_len:
            len_char.append(0)
        char_batch.append(sentence_char)
        char_len_batch.append(len_char)
    char_batch = np.asarray(char_batch)
    char_len_batch = np.asarray(char_len_batch)
    return char_batch, char_len_batch


def batch_flow(x_data: list,
               y_data: list,
               word_to_ix: dict,
               tag_to_ix: dict,
               char_to_ix: dict = None,
               char_max_len: int = None,
               batch_size: int = 32,
               sample_shuffle: bool = True,
               max_limit: int = 300):
    """Automatic generate batch data"""
    assert len(x_data) >= batch_size, 'len(x_data) > batch_size'
    assert len(x_data) == len(y_data), \
        'len(x_data) == len(y_data), {} != {}'.format(len(x_data), len(y_data))

    x_batch, y_batch = [], []
    inds = list(range(len(x_data)))
    if sample_shuffle:
        inds = shuffle(inds)
    while True:
        for ind in inds:
            if len(x_batch) == batch_size:
                len_batch = [len(t) for t in x_batch]
                max_len = np.max(len_batch)

                char_batch = None
                char_len_batch = None
                if char_to_ix is not None:
                    char_batch, char_len_batch = extract_char_features(
                        x_batch, char_max_len, char_to_ix, max_len)

                x_batch = [prepare_sequence(x, word_to_ix) for x in x_batch]
                x_batch = [pad_seq(x, max_len) for x in x_batch]
                y_batch = [tag_to_ix[y] for y in y_batch]

                if char_batch is not None:
                    batches = list(
                        zip(x_batch, y_batch, len_batch, char_batch,
                            char_len_batch))
                    batches = sorted(batches, key=lambda x: x[2], reverse=True)
                    (x_batch, y_batch, len_batch, char_batch,
                     char_len_batch) = zip(*batches)

                    tcx, tcy, tcl, tcc, tccl = (torch.from_numpy(
                        np.asarray(x_batch)),
                                                torch.from_numpy(
                                                    np.asarray(y_batch).astype(
                                                        np.int64)),
                                                torch.from_numpy(
                                                    np.asarray(len_batch)),
                                                torch.from_numpy(
                                                    np.asarray(char_batch)),
                                                torch.from_numpy(
                                                    np.asarray(
                                                        char_len_batch,
                                                        dtype=np.int32)))
                else:
                    batches = list(zip(x_batch, y_batch, len_batch))
                    batches = sorted(batches, key=lambda x: x[2], reverse=True)
                    (x_batch, y_batch, len_batch) = zip(*batches)

                    tcx, tcy, tcl, tcc, tccl = (torch.from_numpy(
                        np.asarray(x_batch)),
                                                torch.from_numpy(
                                                    np.asarray(y_batch).astype(
                                                        np.int64)),
                                                torch.from_numpy(
                                                    np.asarray(len_batch)),
                                                None, None)
                x_batch, y_batch = [], []
                yield tcx, tcy, tcl, tcc, tccl

            x_batch.append(x_data[ind][:max_limit])
            y_batch.append(y_data[ind])
