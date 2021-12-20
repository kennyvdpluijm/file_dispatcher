from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
import os

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'msg'}
app = Flask(__name__)
app.config['SECRET_KEY'] = "donttell"
path = 'yourPath'
Actual_ops_files = os.listdir(path)

for folder in Actual_ops_files:
    folder_list = folder.split(" ")
    client_reference = str(folder_list[0])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def test():
    if request.method == 'POST':
        if 'filename' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['filename']
        string_file = str(file)
        begin_match_value = string_file.find(client_reference)
        end_match_value = begin_match_value + len(client_reference)
        complete_matching_value = str(string_file[begin_match_value:end_match_value])

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            if complete_matching_value in client_reference:
                for map_name in Actual_ops_files:
                    map_list = map_name.split(" ")
                    if client_reference == map_list[0] in map_name:
                        UPLOAD = r'yourPath' + str("/" + map_name)
                        app.config['UPLOAD'] = UPLOAD
                        filename = secure_filename(file.filename)
                        file.save(os.path.join(app.config['UPLOAD'], filename))
                        return render_template("load.html")
                    else:
                        pass
            else:
                print("fail")
    return render_template("load.html")


if __name__ == "__main__": app.run(debug='True')
