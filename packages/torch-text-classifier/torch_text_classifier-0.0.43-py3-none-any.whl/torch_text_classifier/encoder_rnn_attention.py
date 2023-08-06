# -*- coding: utf-8 -*-
"""RNN attention

@TODO multi-head attention

Reference:

https://github.com/jadore801120/attention-is-all-you-need-pytorch/blob/master/transformer/SubLayers.py

https://github.com/jadore801120/attention-is-all-you-need-pytorch/blob/master/transformer/Modules.py
"""

import torch
import torch.nn.functional as F
from torch import nn


class EncoderRNNAttention(nn.Module):
    def __init__(self,
                 vocab_size,
                 bidirectional,
                 embedding_dim=100,
                 hidden_dim=100,
                 n_class=2,
                 embedding_dropout_p=0):
        super(EncoderRNNAttention, self).__init__()

        self._embedding_dropout = nn.Dropout(embedding_dropout_p)
        self._embeds = nn.Embedding(vocab_size, embedding_dim, padding_idx=0)
        if bidirectional:
            self._rnn = nn.LSTM(
                embedding_dim,
                hidden_dim // 2,
                bidirectional=True,
                batch_first=False)
        else:
            self._rnn = nn.LSTM(embedding_dim, hidden_dim, batch_first=False)

    def forward(self, sentence, lengths):
        embeds = self._embeds(sentence)
        embeds = self._embedding_dropout(embeds)
        x = embeds.transpose(1, 0)

        packed = nn.utils.rnn.pack_padded_sequence(
            x, lengths, batch_first=False)
        rnn_out, _ = self._rnn(packed)
        x, _ = nn.utils.rnn.pad_packed_sequence(rnn_out, batch_first=True)

        # x = attention(x, embeds)
        x = attention(x, x)
        return x


def attention(x, embeds=None):
    batch_size, seq_len, hidden_dim = x.size()
    m = torch.bmm(embeds, embeds.transpose(2, 1))
    m = F.softmax(m, dim=2)
    x = torch.bmm(m, x)
    x = x.sum(1)
    return x
