import gzip
import logging
import os

import nltk
import numpy as np

from nlp_utils.dataset.download import getEmbeddings
from nlp_utils.embedding.word_embedding import wordNormalize


def readEmbeddings(embeddingsPath, datasetFiles=tuple(), frequencyThresholdUnknownTokens=None, reducePretrainedEmbeddings=False):
    """
    Reads the embeddingsPath.
    :param embeddingsPath: File path to pretrained embeddings
    :param datasetName:
    :param datasetFiles:
    :param frequencyThresholdUnknownTokens:
    :param reducePretrainedEmbeddings:
    :return:
    """
    # Check that the embeddings file exists
    if not os.path.isfile(embeddingsPath):
        if embeddingsPath in ['komninos_english_embeddings.gz', 'levy_english_dependency_embeddings.gz', 'reimers_german_embeddings.gz']:
            getEmbeddings(embeddingsPath)
        else:
            print("The embeddings file %s was not found" % embeddingsPath)
            exit()

    logging.info("Generate new embeddings files for a dataset")

    neededVocab = {}
    if reducePretrainedEmbeddings:
        logging.info("Compute which tokens are required for the experiment")

        def createDict(filename, tokenPos, vocab):
            for line in open(filename):
                if line.startswith('#'):
                    continue
                splits = line.strip().split()
                if len(splits) > 1:
                    word = splits[tokenPos]
                    wordLower = word.lower()
                    wordNormalized = wordNormalize(wordLower)

                    vocab[word] = True
                    vocab[wordLower] = True
                    vocab[wordNormalized] = True

        for dataset in datasetFiles:
            dataColumnsIdx = {y: x for x, y in dataset['cols'].items()}
            tokenIdx = dataColumnsIdx['tokens']
            datasetPath = 'data/%s/' % dataset['name']

            for dataset in ['train.txt', 'dev.txt', 'test.txt']:
                createDict(datasetPath + dataset, tokenIdx, neededVocab)

    # :: Read in word embeddings ::
    logging.info("Read file: %s" % embeddingsPath)
    word2Idx = {}
    embeddings = []

    embeddingsIn = gzip.open(embeddingsPath, "rt") if embeddingsPath.endswith('.gz') else open(embeddingsPath,
                                                                                               encoding="utf8")

    embeddingsDimension = None

    for line in embeddingsIn:
        split = line.rstrip().split(" ")
        word = split[0]

        if embeddingsDimension == None:
            embeddingsDimension = len(split) - 1

        if (len(
                split) - 1) != embeddingsDimension:  # Assure that all lines in the embeddings file are of the same length
            print("ERROR: A line in the embeddings file had more or less  dimensions than expected. Skip token.")
            continue

        if len(word2Idx) == 0:  # Add padding+unknown
            word2Idx["PADDING_TOKEN"] = len(word2Idx)
            vector = np.zeros(embeddingsDimension)
            embeddings.append(vector)

            word2Idx["UNKNOWN_TOKEN"] = len(word2Idx)
            vector = np.random.uniform(-0.25, 0.25, embeddingsDimension)  # Alternativ -sqrt(3/dim) ... sqrt(3/dim)
            embeddings.append(vector)

        vector = np.array([float(num) for num in split[1:]])

        if len(neededVocab) == 0 or word in neededVocab:
            if word not in word2Idx:
                embeddings.append(vector)
                word2Idx[word] = len(word2Idx)

    # Extend embeddings file with new tokens
    def createFD(filename, tokenIndex, fd, word2Idx):
        for line in open(filename):
            if line.startswith('#'):
                continue

            splits = line.strip().split()

            if len(splits) > 1:
                word = splits[tokenIndex]
                wordLower = word.lower()
                wordNormalized = wordNormalize(wordLower)

                if word not in word2Idx and wordLower not in word2Idx and wordNormalized not in word2Idx:
                    fd[wordNormalized] += 1

    if frequencyThresholdUnknownTokens != None and frequencyThresholdUnknownTokens >= 0:
        fd = nltk.FreqDist()
        for datasetName, datasetFile in datasetFiles.items():
            dataColumnsIdx = {y: x for x, y in datasetFile['columns'].items()}
            tokenIdx = dataColumnsIdx['tokens']
            datasetPath = 'data/%s/' % datasetName
            createFD(datasetPath + 'train.txt', tokenIdx, fd, word2Idx)

        addedWords = 0
        for word, freq in fd.most_common(10000):
            if freq < frequencyThresholdUnknownTokens:
                break

            addedWords += 1
            word2Idx[word] = len(word2Idx)
            vector = np.random.uniform(-0.25, 0.25, len(split) - 1)  # Alternativ -sqrt(3/dim) ... sqrt(3/dim)
            embeddings.append(vector)

            assert (len(word2Idx) == len(embeddings))

        logging.info("Added words: %d" % addedWords)
    embeddings = np.array(embeddings)

    return embeddings, word2Idx