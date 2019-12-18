from __future__ import absolute_import, division, print_function

import os

class InputExample(object):
    """A single training/test example for simple sequence classification."""

    def __init__(self, guid, text_a, text_b=None, label=None, polarity=None):
        """Constructs a InputExample.

        Args:
            guid: Unique id for the example.
            text_a: string. The untokenized text of the first sequence. For single
            sequence tasks, only this sequence must be specified.
            text_b: (Optional) string. The untokenized text of the second sequence.
            Only must be specified for sequence pair tasks.
            label: (Optional) string. The label of the example. This should be
            specified for train and dev examples, but not for test examples.
        """
        self.guid = guid
        self.text_a = text_a
        self.text_b = text_b
        self.label = label
        self.polarity = polarity

class InputFeatures(object):
    """A single set of features of data."""

    def __init__(self, input_ids_spc, input_mask, segment_ids, label_id, polarities=None, valid_ids=None, label_mask=None):
        self.input_ids_spc = input_ids_spc
        self.input_mask = input_mask
        self.segment_ids = segment_ids
        self.label_id = label_id
        self.valid_ids = valid_ids
        self.label_mask = label_mask
        self.polarities = polarities

def readfile(filename):
    '''
    read file
    '''
    f = open(filename, encoding='utf8')
    data = []
    sentence = []
    tag= []
    polarity = []
    for line in f:
        if len(line )==0 or line.startswith('-DOCSTART') or line[0 ]=="\n":
            if len(sentence) > 0:
                data.append((sentence, tag, polarity))
                sentence = []
                tag = []
                polarity = []
            continue
        splits = line.split(' ')
        sentence.append(splits[0])
        tag.append(splits[-2])
        polarity.append(int(splits[-1][:-1]))

    if len(sentence) > 0:
        data.append((sentence, tag, polarity))
    return data


class DataProcessor(object):
    """Base class for data converters for sequence classification data sets."""

    def get_train_examples(self, data_dir):
        """Gets a collection of `InputExample`s for the train set."""
        raise NotImplementedError()

    def get_dev_examples(self, data_dir):
        """Gets a collection of `InputExample`s for the dev set."""
        raise NotImplementedError()

    def get_labels(self):
        """Gets the list of labels for this data set."""
        raise NotImplementedError()

    @classmethod
    def _read_tsv(cls, input_file, quotechar=None):
        """Reads a tab separated value file."""
        return readfile(input_file)


class ATEPCProcessor(DataProcessor):
    """Processor for the CoNLL-2003 data set."""

    def get_train_examples(self, data_dir):
        """See base class."""
        if 'laptop' in data_dir:
            return self._create_examples(
                self._read_tsv(os.path.join(data_dir, "Laptops.atepc.train.dat")), "train")
        elif 'rest' in data_dir:
            return self._create_examples(
                self._read_tsv(os.path.join(data_dir, "Restaurants.atepc.train.dat")), "train")
        elif 'twitter' in data_dir:
            return self._create_examples(
                self._read_tsv(os.path.join(data_dir, "twitter.atepc.train.dat")), "train")
        elif 'car' in data_dir:
            return self._create_examples(
                self._read_tsv(os.path.join(data_dir, "car.atepc.train.dat")), "train")
        elif 'phone' in data_dir:
            return self._create_examples(
                self._read_tsv(os.path.join(data_dir, "phone.atepc.train.dat")), "train")
        elif 'camera' in data_dir:
            return self._create_examples(
                self._read_tsv(os.path.join(data_dir, "camera.atepc.train.dat")), "train")
        elif 'notebook' in data_dir:
            return self._create_examples(
                self._read_tsv(os.path.join(data_dir, "notebook.atepc.train.dat")), "train")
        elif 'mixed' in data_dir:
            return self._create_examples(
                self._read_tsv(os.path.join(data_dir, "mixed.atepc.train.dat")), "train")

    # def get_dev_examples(self, data_dir):
    #     """See base class."""
    #     if 'laptop' in data_dir:
    #         return self._create_examples(
    #             self._read_tsv(os.experiments.join(data_dir, "Laptops.atepc.valid.dat")), "valid")
    #     elif 'rest' in data_dir:
    #         return self._create_examples(
    #             self._read_tsv(os.experiments.join(data_dir, "Restaurants.atepc.valid.dat")), "valid")
    #     else:
    #         return self._create_examples(
    #             self._read_tsv(os.experiments.join(data_dir, "twitter.atepc.valid.dat")), "valid")

    def get_test_examples(self, data_dir):
        """See base class."""
        if 'laptop' in data_dir:
            return self._create_examples(
                self._read_tsv(os.path.join(data_dir, "Laptops.atepc.test.dat")), "test")
        elif 'rest' in data_dir:
            return self._create_examples(
                self._read_tsv(os.path.join(data_dir, "Restaurants.atepc.test.dat")), "test")
        elif 'twitter' in data_dir:
            return self._create_examples(
                self._read_tsv(os.path.join(data_dir, "twitter.atepc.test.dat")), "test")
        elif 'car' in data_dir:
            return self._create_examples(
                self._read_tsv(os.path.join(data_dir, "car.atepc.test.dat")), "test")
        elif 'phone' in data_dir:
            return self._create_examples(
                self._read_tsv(os.path.join(data_dir, "phone.atepc.test.dat")), "test")
        elif 'camera' in data_dir:
            return self._create_examples(
                self._read_tsv(os.path.join(data_dir, "camera.atepc.test.dat")), "test")
        elif 'notebook' in data_dir:
            return self._create_examples(
                self._read_tsv(os.path.join(data_dir, "notebook.atepc.test.dat")), "test")
        elif 'mixed' in data_dir:
            return self._create_examples(
                self._read_tsv(os.path.join(data_dir, "mixed.atepc.test.dat")), "test")


    def get_labels(self):
        return ["O", "B-ASP", "I-ASP", "[CLS]", "[SEP]"]

    def _create_examples(self, lines, set_type):
        examples = []
        for i, (sentence, tag, polarity) in enumerate(lines):
            aspect = ['[SEP]']
            aspect_tag = ['O']
            aspect_polarity = [-1]
            for w, t, p in zip(sentence, tag, polarity):
                if p != -1:
                    aspect.append(w)
                    aspect_tag.append(t)
                    aspect_polarity.append(-1)
            guid = "%s-%s" % (set_type, i)
            text_a = ' '.join(sentence) + ' ' + ' '.join(aspect)
            text_b = ' '.join(sentence)
            tag.extend(aspect_tag)
            polarity.extend(aspect_polarity)
            examples.append(InputExample(guid=guid, text_a=text_a, text_b=text_b, label=tag, polarity=polarity))
        return examples

def convert_examples_to_features(examples, label_list, max_seq_length, tokenizer):
    """Loads a data file into a list of `InputBatch`s."""
    # logger.info('converting_examples_to_features')
    label_map = {label: i for i, label in enumerate(label_list, 1)}

    features = []
    for (ex_index, example) in enumerate(examples):
        text_spc_tokens = example.text_a.split(' ')
        labellist = example.label
        polaritiylist = example.polarity
        tokens = []
        labels = []
        polarities = []
        valid = []
        label_mask = []
        for i, word_of_spc in enumerate(text_spc_tokens):
            token_of_spc = tokenizer.tokenize(word_of_spc)
            tokens.extend(token_of_spc)
            label_1 = labellist[i]
            polarity_1 = polaritiylist[i]
            for m in range(len(token_of_spc)):
                if m == 0:
                    labels.append(label_1)
                    polarities.append(polarity_1)
                    valid.append(1)
                    label_mask.append(1)
                else:
                    valid.append(0)
        if len(tokens) >= max_seq_length - 1:
            tokens = tokens[0:(max_seq_length - 2)]
            labels = labels[0:(max_seq_length - 2)]
            polarities = polarities[0:(max_seq_length - 2)]
            valid = valid[0:(max_seq_length - 2)]
            label_mask = label_mask[0:(max_seq_length - 2)]
        ntokens = []
        segment_ids = []
        label_ids = []
        polarities.insert(0,-1)
        polarities.append(-1)
        ntokens.append("[CLS]")
        segment_ids.append(0)
        valid.insert(0, 1)
        label_mask.insert(0, 1)
        label_ids.append(label_map["[CLS]"])
        for i, token_of_spc in enumerate(tokens):
            ntokens.append(token_of_spc)
            segment_ids.append(0)
            if len(labels) > i:
                label_ids.append(label_map[labels[i]])
        ntokens.append("[SEP]")
        segment_ids.append(0)
        valid.append(1)
        label_mask.append(1)
        label_ids.append(label_map["[SEP]"])
        input_ids_spc = tokenizer.convert_tokens_to_ids(ntokens)
        input_mask = [1] * len(input_ids_spc)
        label_mask = [1] * len(label_ids)
        while len(input_ids_spc) < max_seq_length:
            input_ids_spc.append(0)
            input_mask.append(0)
            segment_ids.append(0)
            label_ids.append(0)
            valid.append(1)
            label_mask.append(0)
        while len(label_ids) < max_seq_length:
            label_ids.append(0)
            label_mask.append(0)
        while len(polarities) < max_seq_length:
            polarities.append(-1)
        assert len(input_ids_spc) == max_seq_length
        assert len(input_mask) == max_seq_length
        assert len(segment_ids) == max_seq_length
        assert len(label_ids) == max_seq_length
        assert len(polarities) == max_seq_length
        assert len(valid) == max_seq_length
        assert len(label_mask) == max_seq_length

        # if ex_index < 5:
        #     logger.info("*** Example ***")
        #     logger.info("guid: %s" % (example.guid))
        #     logger.info("tokens: %s" % " ".join(
        #         [str(x) for x in tokens]))
        #     logger.info("input_ids_spc: %s" % " ".join([str(x) for x in input_ids_spc]))
        #     logger.info("input_mask: %s" % " ".join([str(x) for x in input_mask]))
        #     logger.info(
        #         "segment_ids: %s" % " ".join([str(x) for x in segment_ids]))
        #     # logger.info("label: %s (id = %d)" % (example.label, label_ids))

        features.append(
            InputFeatures(input_ids_spc=input_ids_spc,
                          input_mask=input_mask,
                          segment_ids=segment_ids,
                          label_id=label_ids,
                          polarities=polarities,
                          valid_ids=valid,
                          label_mask=label_mask))
    return features