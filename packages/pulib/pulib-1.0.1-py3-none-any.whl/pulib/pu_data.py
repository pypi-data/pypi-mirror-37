import math

def pnu_from_dataframe(dataframe, pos_column, pos_class, pos_size=0.8, neg_size=0.8):
    '''
    Function to generate random positive-negative-unlabeled data from any pandas dataframe. It returns the same dataset with a 'y' column containing the positive-negative-unlabeled data.

    REQUIRED

    dataframe: pandas.Dataframe to be extracted to positive-negative-unlabeled.
    pos_column: dataframe column to be compared to extract the positive class.
    pos_class: class in the pos_column to be considered as positive.

    OPTIONAL

    pos_size: positive rate (if [0, 1]) or positive literal number (greater than one).
    pos_size will default to 0.8 if no value is specified.
    neg_size: negative rate (if [0, 1]) or positive literal number (greater than one).
    neg_size will default to 0.8 if no value is specified.
    '''

    if pos_size > 0 and neg_size > 0:
        if pos_size <= 1:
            pos_total = math.floor(pos_size * len(dataframe[dataframe[pos_column] == pos_class]))

        if pos_size > 1:
            pos_total = pos_size

        if neg_size <= 1:
            neg_total = math.floor(neg_size * len(dataframe[dataframe[pos_column] != pos_class]))

        if neg_size > 1:
            neg_total = neg_size

        dataframe = dataframe.sample(frac=1).reset_index(drop=True)

        actual_pos = 0
        actual_neg = 0
        for index, value in enumerate(dataframe.loc[:, pos_column]):
            if value == pos_class:
                if actual_pos < pos_total:
                    dataframe.loc[index, 'y'] = 1
                    actual_pos += 1
                else:
                    dataframe.loc[index, 'y'] = 0
            else:
                if actual_neg < neg_total:
                    dataframe.loc[index, 'y'] = -1
                    actual_neg += 1
                else:
                    dataframe.loc[index, 'y'] = 0

        return dataframe

    else:
        raise ArithmeticError('pos_size and neg_size must be greater than 0')
