"""
"""

from sklearn import model_selection

def train_test_split(return_X_y=False, X=None, y=None, test_size=0.25, random_state=0):
    X_train, X_test, y_train,  y_test = model_selection.train_test_split(X, y, test_size=test_size,random_state=random_state)
    return X_train, X_test, y_train, y_test

if __name__ == "__main__":
    import load
    iris = load("iris")
    X_train, X_test, y_train, y_test = train_test_split(X=X, y=y)
    
