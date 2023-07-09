import psycopg2
from flask import Flask


def generate_html():
    # Establish a connection to the PostgreSQL database
    conn = psycopg2.connect(host='localhost',
    port = '5432',
    user = 'postgres',
    password = '159357lol',
    dbname = 'postgres')

    # Create a cursor object to interact with the database
    cur = conn.cursor()

    # Execute a SELECT query to retrieve data from the table
    cur.execute("SELECT img, Velikost, Lokace FROM sreality")

    # Fetch all rows from the result
    rows = cur.fetchall()

    # Generate HTML for the table
    html = "<html><body><table>"
    html += "<tr><th>Velikost</th><th>Lokace</th><th>Image</th></tr>"

    for row in rows:
        image_link = row[0]
        velikost = row[1]
        lokace = row[2]
        html += "<tr>"
        html += "<td><img src='{}' width='400' height='300'></td>".format(image_link)
        html += "<td>{}</td>".format(velikost)
        html += "<td>{}</td>".format(lokace)
        html += "</tr>"

    html += "</table></body></html>"

    # Close the database connection
    cur.close()
    conn.close()

    return html

# Generate the HTML page
html_page = generate_html()

# Save the HTML page to a file
with open('output.html', 'w') as f:
    f.write(html_page)

app = Flask(__name__)

@app.route('/')
def display_html():
    # Read the HTML page from the file
    with open('output.html', 'r') as f:
        html_page = f.read()

    return html_page

if __name__ == '__main__':
    app.run(port=8080)