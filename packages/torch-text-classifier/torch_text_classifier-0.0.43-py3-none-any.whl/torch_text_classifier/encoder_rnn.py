# -*- coding: utf-8 -*-
"""Main text classifier class
"""

from torch import nn


class EncoderRNN(nn.Module):
    def __init__(self,
                 vocab_size,
                 bidirectional,
                 embedding_dim=100,
                 hidden_dim=100,
                 n_class=2,
                 embedding_dropout_p=0):
        super(EncoderRNN, self).__init__()

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
        x = sentence
        x = self._embeds(x)
        x = self._embedding_dropout(x)
        x = x.transpose(1, 0)

        packed = nn.utils.rnn.pack_padded_sequence(
            x, lengths, batch_first=False)
        rnn_out, _ = self._rnn(packed)
        x, _ = nn.utils.rnn.pad_packed_sequence(rnn_out, batch_first=True)

        x = x.sum(1)  # get sum hidden state
        return x
