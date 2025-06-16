from enum import Enum
from random import choice #Was macht das?
from sklearn.model_selection import cross_validate

class SplitMethod(Enum):
    KFold= "Kfold"
    Boostrap632= "Bootstrap 0.632"

#Kreuzvalidierung bekommt das Modell, Merkmalsvariablen, Zielvariablen, Validierungsstrategie, Validierungsmethode) und berechnet Accuracy, F1, Precision, Recall
def cross_validation(estimator, X, Y, cv, method):
    result= cross_validate(
        estimator,
        X,
        Y,
        cv=cv,
        return_estimator=True,
        return_indices=True,
        scoring=["accuracy", "precision", "recall", "f1"]
    )

    result["split_method"] = method

    return result

#Kreuzvalidierung mit 10-Folds
def kfold (estimator, X, Y):
    return cross_validation(estimator, X, Y, cv=10, method=SplitMethod.KFold)

def bootstrap(estimator, X, Y):
    def split(n, iterations):
        splits=[]
        rng= range(0,n)

        for i in range(0, iterations):
            # Erstellen eines zufälligen Trainingssets von Zahlen aus dem Bereich
            train ={choice(rng) for _ in rng}
            # Erstellt das Testset durch Subtraktion des Trainingssets vom Gesamtbereich
            test = set(rng) - train

            splits.append((list(train), list(test)))

        return splits
    return cross_validation(estimator, X, Y, cv=split(len(X), 10), method=SplitMethod.Boostrap632)
