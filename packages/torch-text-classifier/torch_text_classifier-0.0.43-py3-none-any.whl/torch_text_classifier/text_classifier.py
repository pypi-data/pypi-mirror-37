# -*- coding: utf-8 -*-
"""Main text classifier class
"""

import math
import os
import pickle
from collections import Counter

import numpy as np

import torch
from sklearn.base import BaseEstimator
from sklearn.metrics import accuracy_score, precision_score, recall_score
from torch import nn, optim
from tqdm import tqdm

from .text_classifier_model import TextClassifierModel
from .utils import (DEVICE, batch_flow, build_vocabulary,
                    extract_char_features, pad_seq, prepare_sequence)


class TextClassifier(BaseEstimator):
    def __init__(
            self,
            epochs=10,
            verbose=0,
            batch_size=32,
            learning_rate_decay=0,
            char_max_len=30,
            embedding_dim=100,
            hidden_dim=100,
            clip_grad_norm=None,
            average_loss=True,
            device='auto',
            bidirectional=True,
            embedding_dropout_p=0,
            encoder_dropout_p=0,
            encoder='rnn_attention',
            optimizer='SGD',
            weight_decay=0,
            momentum=0,
            learning_rate=None,
            class_weight=None,  # 'auto' or None or list
            use_char=None,
            max_length=None,
            _model=None,
            _optimizer=None,
            _word_to_ix=None,
            _ix_to_word=None,
            _tag_to_ix=None,
            _ix_to_tag=None,
            _char_to_ix=None,
            _ix_to_char=None):

        self.params = {
            'epochs': epochs,
            'verbose': verbose,
            'batch_size': batch_size,
            'learning_rate_decay': learning_rate_decay,
            'char_max_len': char_max_len,
            'embedding_dim': embedding_dim,
            'hidden_dim': hidden_dim,
            'clip_grad_norm': clip_grad_norm,
            'average_loss': average_loss,
            'device': device,
            'bidirectional': bidirectional,
            'embedding_dropout_p': embedding_dropout_p,
            'encoder_dropout_p': encoder_dropout_p,
            'encoder': encoder,
            'optimizer': optimizer,
            'weight_decay': weight_decay,
            'momentum': momentum,
            'learning_rate': learning_rate,
            'class_weight': class_weight,
            'use_char': use_char,
            'n_class': None,
            'max_length': max_length,
        }

        self._model = _model
        self._optimizer = _optimizer
        self._word_to_ix = _word_to_ix
        self._ix_to_word = _ix_to_word
        self._tag_to_ix = _tag_to_ix
        self._ix_to_tag = _ix_to_tag
        self._char_to_ix = _char_to_ix
        self._ix_to_char = _ix_to_char

    def get_params(self, deep=True):
        """Get params for scikit-learn compatible"""
        params = self.params
        if deep:
            params['_model'] = self._model.state_dict(
            ) if self._model is not None else None
            params['_optimizer'] = self._optimizer.state_dict() \
                if self._optimizer is not None else None
            params['_word_to_ix'] = self._word_to_ix
            params['_ix_to_word'] = self._ix_to_word
            params['_tag_to_ix'] = self._tag_to_ix
            params['_ix_to_tag'] = self._ix_to_tag
            params['_char_to_ix'] = self._char_to_ix
            params['_ix_to_char'] = self._ix_to_char
        return params

    def set_params(self, **parameters):
        """Set params for scikit-learn compatible"""
        for key, value in parameters.items():
            if key in self.params:
                self.params[key] = value
        return self

    def __getstate__(self):
        """Get state for pickle"""
        state = {
            'params':
            self.params,
            '_model':
            self._model.state_dict() if self._model is not None else None,
            '_optimizer':
            self._optimizer.state_dict()
            if self._optimizer is not None else None,
            '_word_to_ix':
            self._word_to_ix,
            '_ix_to_word':
            self._ix_to_word,
            '_tag_to_ix':
            self._tag_to_ix,
            '_ix_to_tag':
            self._ix_to_tag,
            '_char_to_ix':
            self._char_to_ix,
            '_ix_to_char':
            self._ix_to_char
        }
        return state

    def __setstate__(self, state):
        """Get state for pickle"""
        self.params = state['params']
        if state['_model'] is not None:
            self._word_to_ix = state['_word_to_ix']
            self._ix_to_word = state['_ix_to_word']
            self._tag_to_ix = state['_tag_to_ix']
            self._ix_to_tag = state['_ix_to_tag']
            self._char_to_ix = state['_char_to_ix']
            self._ix_to_char = state['_ix_to_char']
            self.apply_params()
            self._model.load_state_dict(state['_model'])
            self._optimizer.load_state_dict(state['_optimizer'])

    def apply_params(self, y_train=None):
        word_to_ix = self._word_to_ix
        bidirectional = self.params['bidirectional']
        embedding_dropout_p = self.params['embedding_dropout_p']
        encoder_dropout_p = self.params['encoder_dropout_p']
        encoder = self.params['encoder']
        embedding_dim = self.params['embedding_dim']
        hidden_dim = self.params['hidden_dim']
        n_class = self.params['n_class']
        optimizer = self.params['optimizer']
        weight_decay = self.params['weight_decay']
        momentum = self.params['momentum']
        model = TextClassifierModel(
            vocab_size=len(word_to_ix),
            bidirectional=bidirectional,
            embedding_dropout_p=embedding_dropout_p,
            encoder_dropout_p=encoder_dropout_p,
            encoder=encoder,
            embedding_dim=embedding_dim,
            hidden_dim=hidden_dim,
            n_class=n_class,
            class_weight=self._get_class_weight(y_train))
        if optimizer.lower() == 'adam':
            optimizer = optim.Adam(
                model.parameters(),
                lr=self._get_learning_rate(),
                weight_decay=weight_decay)
        elif optimizer.lower() == 'sgd':
            optimizer = optim.SGD(
                model.parameters(),
                lr=self._get_learning_rate(),
                weight_decay=weight_decay,
                momentum=momentum)
        self._model = model.to(self._get_device())
        self._optimizer = optimizer

    def _get_class_weight(self, y_train=None):
        class_weight = self.params['class_weight']
        if class_weight is None:
            return None
        elif isinstance(class_weight, (tuple, list)):
            class_weight = np.array(class_weight).astype(np.float32)
            assert len(class_weight.shape) == 1
            class_weight = torch.from_numpy(class_weight).to(
                self._get_device())
            return class_weight
        elif isinstance(class_weight, np.ndarray):
            assert len(class_weight.shape) == 1
            class_weight = torch.from_numpy(class_weight.astype(
                np.float32)).to(self._get_device())
            return class_weight
        elif (isinstance(class_weight, str) and class_weight == 'auto'
              and y_train is not None):
            y_class_counter = Counter([self._tag_to_ix[y] for y in y_train])
            class_weight = [1] * len(y_class_counter)
            max_yc = max(y_class_counter.values())
            y_class_counter = {
                k: max_yc / v
                for k, v in y_class_counter.items()
            }
            for k, v in y_class_counter.items():
                class_weight[k] = v
            tag_weight = {
                self._ix_to_tag[k]: v
                for k, v in y_class_counter.items()
            }
            print('auto class_weight:', tag_weight)
            class_weight = np.array(class_weight).astype(np.float32)
            assert len(class_weight.shape) == 1
            class_weight = torch.from_numpy(class_weight).to(
                self._get_device())
            return class_weight
        return None

    def _get_learning_rate(self):
        """default learning rate"""
        optimizer = self.params['optimizer']
        learning_rate = self.params['learning_rate']
        if learning_rate is not None:
            return learning_rate
        if optimizer.lower() == 'sgd':
            return 1e-2
        if optimizer.lower() == 'adam':
            return 1e-3

    def _get_device(self):
        """Get device to predict or train"""
        device = self.params['device']
        if device == 'auto':
            return DEVICE
        if device in ('cpu', ):
            return torch.device('cpu')
        if device in ('gpu', 'cuda'):
            return torch.device('cuda')

    def fit(self,
            X,
            y,
            X_dev=None,
            y_dev=None,
            patient_dev=None,
            save_best=None,
            pretrained_embedding=None,
            predict_batch_size=32):
        """Fit the model"""

        assert len(X) >= self.params['batch_size'], 'X must size >= batch_size'
        assert len(y) >= self.params['batch_size'], 'y must size >= batch_size'
        assert len(X) == len(y), 'X must size equal to y'

        # Autommatic build vocabulary
        vocabulary = build_vocabulary(X, y)
        self._char_to_ix = vocabulary['char_to_ix']
        self._ix_to_char = vocabulary['ix_to_char']
        if self._word_to_ix is None and self._tag_to_ix is None:
            self._word_to_ix = vocabulary['word_to_ix']
            self._ix_to_word = vocabulary['ix_to_word']
            self._tag_to_ix = vocabulary['tag_to_ix']
            self._ix_to_tag = vocabulary['ix_to_tag']
        elif self._word_to_ix is None:
            self._word_to_ix = vocabulary['word_to_ix']
            self._ix_to_word = vocabulary['ix_to_word']
        elif self._tag_to_ix is None:
            self._tag_to_ix = vocabulary['tag_to_ix']
            self._ix_to_tag = vocabulary['ix_to_tag']

        epochs = self.params['epochs']
        verbose = self.params['verbose']
        batch_size = self.params['batch_size']
        learning_rate_decay = self.params['learning_rate_decay']
        char_max_len = self.params['char_max_len']
        clip_grad_norm = self.params['clip_grad_norm']
        average_loss = self.params['average_loss']
        use_char = self.params['use_char']
        max_length = self.params['max_length']

        # apply n_class
        self.params['n_class'] = len(self._ix_to_tag)

        predict_batch_size = max(predict_batch_size, batch_size)

        word_to_ix = self._word_to_ix
        tag_to_ix = self._tag_to_ix
        char_to_ix = self._char_to_ix
        if use_char is None:
            char_to_ix = None

        self.apply_params(y)
        model, optimizer = self._model, self._optimizer
        if pretrained_embedding is not None:
            model.load_embedding(pretrained_embedding)

        dev_best = float('inf')
        dev_best_round = 0
        # Make sure prepare_sequence from earlier in the LSTM section is loaded
        for epoch in range(epochs):
            model.train()
            model.zero_grad()
            lnrt = self._get_learning_rate()
            if learning_rate_decay > 0:
                lnrt = lnrt / (1 + epoch * learning_rate_decay)
                for param_group in optimizer.param_groups:
                    param_group['lr'] = lnrt
            pbar = range(len(X) // batch_size + 1)
            flow = batch_flow(
                X,
                y,
                word_to_ix,
                tag_to_ix,
                batch_size=batch_size,
                char_max_len=char_max_len,
                char_to_ix=char_to_ix,
                max_limit=max_length if isinstance(max_length, int) else 1000)
            losses = []
            if verbose > 0:
                pbar = tqdm(pbar, ncols=0)
                pbar.set_description('epoch: {}/{} loss: {:.4f}'.format(
                    epoch + 1, epochs, 0))
            for _ in pbar:
                x_b, y_b, l_b, l_c, ll_c = next(flow)
                x_b = x_b.to(self._get_device())
                y_b = y_b.to(self._get_device())
                l_b = l_b.to(self._get_device())
                if l_c is not None:
                    l_c = l_c.to(self._get_device())
                    ll_c = ll_c.to(self._get_device())
                loss = model.compute_loss(
                    x_b, y_b, l_b, chars=l_c, charlens=ll_c)
                losses.append(loss.item())
                loss.backward()
                if clip_grad_norm is not None:
                    nn.utils.clip_grad_norm_(model.parameters(),
                                             clip_grad_norm)
                optimizer.step()
                model.zero_grad()
                if verbose > 0:
                    pbar.set_description(
                        'epoch: {}/{} loss: {:.4f} lr: {:.4f}'.format(
                            epoch + 1, epochs, np.mean(losses), lnrt))
            (train_score, train_precision, train_recall,
             train_f1score) = self.score(
                 X,
                 y,
                 batch_size=predict_batch_size,
                 verbose=verbose,
                 detail=True)
            dev_score = None
            if X_dev is None:
                if verbose > 0:
                    print('train: {:.4f}'.format(train_score))
            else:
                model.eval()
                with torch.no_grad():
                    (dev_score, dev_precision, dev_recall,
                     dev_f1score) = self.score(
                         X_dev,
                         y_dev,
                         batch_size=predict_batch_size,
                         verbose=verbose,
                         detail=True)
                    flow = batch_flow(
                        X_dev,
                        y_dev,
                        word_to_ix,
                        tag_to_ix,
                        batch_size=predict_batch_size,
                        char_max_len=char_max_len,
                        char_to_ix=char_to_ix)
                    dev_losses = []
                    pbar = range(math.ceil(len(X_dev) / predict_batch_size))
                    if verbose > 0:
                        pbar = tqdm(pbar, ncols=0)
                    for _ in pbar:
                        x_b, y_b, l_b, l_c, ll_c = next(flow)
                        x_b = x_b.to(self._get_device())
                        y_b = y_b.to(self._get_device())
                        l_b = l_b.to(self._get_device())
                        if l_c is not None:
                            l_c = l_c.to(self._get_device())
                            ll_c = ll_c.to(self._get_device())
                        loss = model.compute_loss(
                            x_b, y_b, l_b, chars=l_c, charlens=ll_c)
                        dev_losses.append(loss.item())
                    dev_loss = np.mean(dev_losses)
                    if not average_loss:
                        dev_loss /= (predict_batch_size / batch_size)

                if verbose > 0:
                    print(('dev loss: {:.4f}, '
                           'train acc {:.4f} '
                           'prec {:.4f} '
                           'rec {:.4f} '
                           'f1 {:.4f}, '
                           'dev acc {:.4f} '
                           'prec {:.4f} '
                           'rec {:.4f} '
                           'f1 {:.4f}').format(
                               dev_loss, train_score, train_precision,
                               train_recall, train_f1score, dev_score,
                               dev_precision, dev_recall, dev_f1score))
                if isinstance(save_best, str):
                    if dev_loss < dev_best:
                        print('save best {:.4f} > {:.4f}'.format(
                            dev_best, dev_loss))
                        dev_best = dev_loss
                        dev_best_round = 0
                        save_dir = os.path.realpath(os.path.dirname(save_best))
                        if not os.path.exists(save_dir):
                            os.makedirs(save_dir)
                        with open(save_best, 'wb') as fobj:
                            pickle.dump(self, fobj)
                    else:
                        dev_best_round += 1
                        print('no better {:.4f} <= {:.4f} {}/{}'.format(
                            dev_best, dev_loss, dev_best_round, patient_dev))
                        if isinstance(patient_dev,
                                      int) and dev_best_round >= patient_dev:
                            return
                print()

    def predict(self, X, batch_size=None, verbose=0, proba=False):
        """Predict tags"""
        model = self._model
        word_to_ix = self._word_to_ix
        ix_to_tag = self._ix_to_tag
        char_to_ix = self._char_to_ix
        use_char = self.params['use_char']
        max_length = self.params['max_length']
        if use_char is None:
            char_to_ix = None
        model.eval()
        if batch_size is None:
            batch_size = self.params['batch_size']
        char_max_len = self.params['char_max_len']
        # Check predictions after training
        data = list(enumerate(X))
        data = sorted(data, key=lambda t: len(t[1]), reverse=True)
        inds = [i for i, _ in data]
        X = [x for _, x in data]
        ret = [None] * len(X)
        with torch.no_grad():
            batch_total = math.ceil(len(X) / batch_size)
            pbar = range(batch_total)
            if verbose > 0:
                pbar = tqdm(pbar, ncols=0)
            for i in pbar:
                ind_batch = inds[i * batch_size:(i + 1) * batch_size]
                x_batch = X[i * batch_size:(i + 1) * batch_size]
                if max_length is not None:
                    x_batch = [sent[:max_length] for sent in x_batch]
                else:
                    x_batch = [sent for sent in x_batch]
                lens = [len(x) for x in x_batch]
                max_len = np.max(lens)

                char_batch = None
                char_len_batch = None
                if char_to_ix is not None:
                    char_batch, char_len_batch = extract_char_features(
                        x_batch, char_max_len, char_to_ix, max_len)

                x_batch = [
                    prepare_sequence(sent, word_to_ix) for sent in x_batch
                ]
                x_batch = [pad_seq(x, max_len) for x in x_batch]

                sent = torch.from_numpy(np.asarray(x_batch)).to(
                    self._get_device())
                lens = torch.Tensor(lens).long().to(self._get_device())
                char_batch, char_len_batch = None, None
                if char_to_ix is not None:
                    char_batch = torch.from_numpy(np.asarray(char_batch)).to(
                        self._get_device())
                    char_len_batch = torch.from_numpy(
                        np.asarray(char_len_batch,
                                   dtype=np.int32)).to(self._get_device())
                logits, predicts = model(sent, lens, char_batch,
                                         char_len_batch)
                if proba:
                    for ind, logit in zip(ind_batch, logits):
                        ret[ind] = logit
                else:
                    for ind, tag_len, tags in zip(ind_batch, lens, predicts):
                        tags = ix_to_tag[tags]
                        ret[ind] = tags
        return ret

    def score(self, X, y, batch_size=None, verbose=0, detail=False):
        """Calculate accuracy
        """

        preds = self.predict(X, verbose=verbose, batch_size=batch_size)
        preds = [self._tag_to_ix[x] for x in preds]
        y = [self._tag_to_ix[x] for x in y]

        accuracy = accuracy_score(y, preds)

        if detail:
            precision = precision_score(y, preds, average='macro')
            recall = recall_score(y, preds, average='macro')
            if precision + recall > 0:
                f1score = 2 * ((precision * recall) / (precision + recall))
            return accuracy, precision, recall, f1score
        return accuracy
