import numpy as np
# different utility functions


def f1(pr, tr, class_num):
    """
    Calculates F1 score for a given class
    :param pr: list of predicted values
    :param tr: list of actual values
    :param class_num: indicates class
    :return: f1 score of class_num for predicted and true values in pr, tr
    """

    # Filter lists by class
    pred = [x == class_num for x in pr]
    truth = [x == class_num for x in tr]
    mix = list(zip(pred, truth))
    # Find true positives, false positives and false negatives
    tp = mix.count((True, True))
    fp = mix.count((False, True))
    fn = mix.count((True, False))
    # Return f1 score, if conditions are met
    if tp == 0 and fn == 0:
        recall = 0
    else:
        recall = tp / (tp + fn)
    if tp == 0 and fp == 0:
        precision = 0
    else:
        precision = tp / (tp + fp)
    if recall == 0 and precision == 0:
        return 0
    else:
        return 2 * recall * precision / (recall + precision)


def macro_f1(predictions, truth):
    """
    Calculates macro f1 score, where all classes have the same weight
    :param predictions: logits of model predictions
    :param truth: list of actual values
    :return: macro f1 between model predictions and actual values
    """
    different_f1s = [f1(predictions, truth, lab) for lab in set(truth)]
    return sum(different_f1s) / len(different_f1s)



def weighted_f1(predictions, truth):
    """
    Calculates weighted f1 score, where all classes have different weights based on appearance
    :param predictions: logits of model predictions
    :param truth: list of actual values
    :return: weighted f1 between model predictions and actual values
    """
    different_f1s = [f1(predictions, truth, lab) for lab in set(truth)]
    different_weights = [np.sum([x == lab for x in truth]) for lab in set(truth)]
    return sum(x*y for x, y in zip(different_f1s, different_weights)) / len(predictions)


def decode(token_list, tokenizer, mode='torch'):
    """
    translates a list of tokens including two sentences/sequences into a readable string
    :param mode: flag for determining how to handle type of token list
    :param token_list: list of wordpiece tokens /
    :param tokenizer: huggingface tokenizer
    :return: string sequence 1, string sequence 2
    """
    if mode == 'torch':
        decoded = tokenizer.decode(token_list.squeeze().tolist())
    elif mode == 'list':
        decoded = tokenizer.decode(token_list.input_ids)
    # Clean-up
    x = decoded.replace(tokenizer.cls_token, '')
    ans_list = x.split(tokenizer.sep_token, 1)
    ans_list[1] = ans_list[1].replace(tokenizer.sep_token, '')
    ans_list[1] = ans_list[1].replace(tokenizer.pad_token, '')
    return ans_list[0].lstrip().rstrip(), ans_list[1].lstrip().rstrip()