from flask import Flask, render_template, request, redirect, url_for, send_file
import mysql.connector
from io import BytesIO

app = Flask(__name__)

# MySQL Configuration
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'omar',  # Replace with your MySQL username
    'password': 'omar',  # Replace with your MySQL password
    'database': 'StoreImageApp'  # Replace with your database name
}

def get_db_connection():
    return mysql.connector.connect(**MYSQL_CONFIG)

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return 'No image part'
    file = request.files['image']
    if file.filename == '':
        return 'No selected file'
    if file:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO images (image_name, image_data) VALUES (%s, %s)",
            (file.filename, file.read())
        )
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('view_images'))

@app.route('/images')
def view_images():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT id, image_name FROM images")
    images = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('display.html', images=images)

@app.route('/image/<int:image_id>')
def get_image(image_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT image_name, image_data FROM images WHERE id = %s", (image_id,))
    image = cursor.fetchone()
    cursor.close()
    connection.close()
    return send_file(BytesIO(image[1]), download_name=image[0], as_attachment=False)

@app.route('/view/<int:image_id>')
def view_image(image_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT id, image_name FROM images WHERE id = %s", (image_id,))
    image = cursor.fetchone()
    cursor.close()
    connection.close()
    return render_template('view_image.html', image=image)

@app.route('/delete/<int:image_id>', methods=['POST'])
def delete_image(image_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM images WHERE id = %s", (image_id,))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for('view_images'))

if __name__ == '__main__':
    app.run(debug=True)
