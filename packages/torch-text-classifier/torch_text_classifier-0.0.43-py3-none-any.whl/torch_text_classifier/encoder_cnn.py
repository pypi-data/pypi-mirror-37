# -*- coding: utf-8 -*-
"""Main text classifier class
"""

import torch
from torch import nn


def global_max_pooling(tensor, dim, topk=1):
    """Global max pooling"""
    ret, _ = torch.topk(tensor, topk, dim)
    return ret


class EncoderCNN(nn.Module):
    def __init__(self,
                 vocab_size,
                 embedding_dim=100,
                 hidden_dim=100,
                 n_class=2,
                 embedding_dropout_p=0):
        super(EncoderCNN, self).__init__()

        self._embedding_dropout = nn.Dropout(embedding_dropout_p)
        self._embeds = nn.Embedding(vocab_size, embedding_dim, padding_idx=0)
        self._cnn_1 = nn.Sequential(
            nn.Conv1d(embedding_dim, hidden_dim, 1, padding=0), nn.ReLU())

    def forward(self, sentence, lengths):
        batch_size = sentence.size(0)
        x = sentence
        x = self._embeds(x)
        x = self._embedding_dropout(x)
        x = x.transpose(2, 1)

        s = global_max_pooling(self._cnn_1(x), 2)
        x = s.view(batch_size, -1)

        return x
