# -*- coding: utf-8 -*-
"""Main text classifier class
"""

import torch
import torch.nn.functional as F
from torch import nn

from .encoder_cnn import EncoderCNN
from .encoder_rnn import EncoderRNN
from .encoder_rnn_attention import EncoderRNNAttention


class TextClassifierModel(nn.Module):
    def __init__(self, vocab_size, bidirectional, embedding_dim, hidden_dim,
                 n_class, encoder, embedding_dropout_p, encoder_dropout_p,
                 class_weight):
        super(TextClassifierModel, self).__init__()
        if encoder.lower() == 'cnn':
            self._encoder = EncoderCNN(vocab_size, embedding_dim, hidden_dim,
                                       n_class, embedding_dropout_p)
        elif encoder.lower() == 'rnn':
            self._encoder = EncoderRNN(vocab_size, bidirectional,
                                       embedding_dim, hidden_dim, n_class,
                                       embedding_dropout_p)
        elif encoder.lower() == 'rnn_attention':
            self._encoder = EncoderRNNAttention(vocab_size, bidirectional,
                                                embedding_dim, hidden_dim,
                                                n_class, embedding_dropout_p)
        self._softmax = nn.Linear(hidden_dim, n_class)
        self._encoder_dropout = nn.Dropout(encoder_dropout_p)
        self._class_weight = class_weight

    def forward(self, sentence, lengths, chars=None, charlens=None):
        x = self._encoder(sentence, lengths)
        x = self._softmax(x)
        scores = x.max(dim=1)
        _, pred = torch.max(x, dim=1)
        return scores, pred.cpu().detach().numpy()

    def compute_loss(self, sentence, tags, lengths, chars=None, charlens=None):
        batch_size = sentence.size(0)
        x = self._encoder(sentence, lengths)
        x = self._encoder_dropout(x)
        x = self._softmax(x)
        loss = F.cross_entropy(
            x, tags, reduction='sum', weight=self._class_weight)
        loss /= batch_size
        return loss
