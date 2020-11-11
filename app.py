import os
import numpy
import json
from leont import Leont
from flask import Flask, request, flash, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = os.path.dirname(__file__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'txt'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/calculate_file',methods=['GET','POST'])
def manage_file():

    file = request.files['file']
    if file.filename == '':
        flash('No file attached')
        return 0

    if file and allowed_file(file.filename):

        filename = secure_filename(file.filename)
        path_to_file = os.path.join('files/',filename)

        file.save(os.path.join(UPLOAD_FOLDER,path_to_file))

        matrix = numpy.loadtxt(os.path.join(UPLOAD_FOLDER,path_to_file),dtype='i',delimiter=' ')
        #print(matrix)

        n = len(matrix)

        #itreate through matrix to get Y and X

        Y = []
        X = []
        coefs = []
        Yn = []

        for i in matrix:
            Y.append(i[len(i)-3])
            X.append(i[len(i)-2])
            coefs.append(i[len(i) - 1])


        for i in range(0, len(Y)):
            Yn.append(float(Y[i] * (coefs[i]) / 100))

        new_matrix = []

        for i in matrix:
            tmp = []
            for j in range(0,n):
                tmp.append(i[j])
            new_matrix.append(tmp)

        matrix = numpy.array(new_matrix)

        leon = Leont()
        ans = leon.solve(matrix,Y,Yn)
        X_ = []
        for i in ans:
            X_.append(i)

        print(X_)
    return json.dumps(X_)


@app.route('/calculate', methods=['GET','POST'])
def manage_matrix():
    data = json.loads(request.data)
    n = int(data[1])
    matrix = []
    tmp = []

    # get matrix
    for i in range(1,(n*n)+1):
        tmp.append(int(data[0][i-1]))
        if(i%n == 0):
            matrix.append(tmp)
            tmp = []

    matrix = numpy.array(matrix)

    # get Y and X
    Y = []
    X = []
    coefs = []
    Yn = []

    for i in range(n*n,(n*n)+ (3*n)-2,3):
        Y.append(int(data[0][i]))

    for i in range((n * n)+1, (n * n) + (3 * n)-1,3):
        X.append(int(data[0][i]))

    for i in range((n * n)+2, (n * n) + (3 * n),3):
        coefs.append(float(data[0][i]))

    for i in range(0,len(Y)):
        Yn.append(float(Y[i]*(coefs[i])/100))


    leon = Leont()
    ans = leon.solve(matrix,Y,Yn)

    X_ = []
    for i in ans:
        X_.append(i)

    print(X_)

    return json.dumps(X_)


if __name__ == '__main__':
    app.run()

