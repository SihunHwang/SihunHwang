import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    evidence = []
    labels = []
    with open(filename) as f:
        rows = csv.reader(f)
        next(rows)
        for row in rows:
            if row[-1] == 'TRUE' :      #lables
                labels.append(1)
            else:
                labels.append(0)
            ev = []
            ev.append( int(row[0]) )    #Administrative, an integer
            ev.append( float(row[1]))          #Administrative_Duration, a floating point number
            ev.append( int(row[2]) )    #Informational, an integer
            ev.append( float(row[3]))          #Informational_Duration, a floating point number
            ev.append( int(row[4]) )    #ProductRelated, an integer
            ev.append( float(row[5]))          #ProductRelated_Duration, a floating point number
            ev.append( float(row[6]))          #BounceRates, a floating point number
            ev.append( float(row[7]))          #ExitRates, a floating point number
            ev.append( float(row[8]))          #PageValues, a floating point number
            ev.append( float(row[9]))          #SpecialDay, a floating point number
            if row[10] == 'Jan':        #Month, an index from 0 (January) to 11 (December)
                ev.append(0)
            elif row[10] == 'Feb':
                ev.append(1)
            elif row[10] == 'Mar':
                ev.append(2)
            elif row[10] == 'Apr':
                ev.append(3)
            elif row[10] == 'May':
                ev.append(4)
            elif row[10] == 'June':
                ev.append(5)
            elif row[10] == 'Jul':
                ev.append(6)
            elif row[10] == 'Aug':
                ev.append(7)
            elif row[10] == 'Sep':
                ev.append(8)
            elif row[10] == 'Oct':
                ev.append(9)
            elif row[10] == 'Nov':
                ev.append(10)
            elif row[10] == 'Dec':
                ev.append(11)
            ev.append( int(row[11]) )           #OperatingSystems, an integer
            ev.append( int(row[12]) )           #Browser, an integer
            ev.append( int(row[13]) )           #Region, an integer
            ev.append( int(row[14]) )           #TrafficType, an integer
            if row[15] == 'Returning_Visitor':  #VisitorType, an integer 0 (not returning) or 1 (returning)
                ev.append(1)
            else:
                ev.append(0)
            if row[16] == 'TRUE':                #Weekend, an integer 0 (if false) or 1 (if true)
                ev.append(1)
            else:
                ev.append(0)

            evidence.append(ev)
    
    return (evidence, labels)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    machine = KNeighborsClassifier(n_neighbors=1)
    machine.fit(evidence, labels)
    return machine


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    
    sensitivity = 0
    p = 0
    specificity = 0
    n = 0

    for i in range(len(labels)):
        if labels[i] == 1:
            p += 1
            if predictions[i] == 1:
                sensitivity += 1
        else:
            n += 1
            if predictions[i] == 0:
                specificity += 1
                
    sensitivity = sensitivity/p
    specificity = specificity/n

    return (sensitivity, specificity)


if __name__ == "__main__":
    main()
