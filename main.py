from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    #return 'Hello World! vom laptop'
    return '<!DOCTYPE html>' \
           '<html lang="en">' \
           '    <head>' \
           '        <meta charset="utf-8">' \
           '        <meta http-equiv="X-UA-Compatible" content="IE=edge">' \
           '        <meta name="viewport" content="width=device-width, initial-scale=1">' \
           '        <title>Bootstrap 101 Template</title>' \
           '        <link href="css/bootstrap.css" rel="stylesheet">' \
           '        <!--[if lt IE 9]>' \
           '            <script src="https://oss.maxcdn.com/html5shiv/3.7.3/html5shiv.min.js"></script>' \
           '            <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>' \
           '        <![endif]-->' \
           '    </head>' \
           '    <body>' \
           '        <h1>Hello, world!</h1>' \
           '        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>' \
           '        <!-- Include all compiled plugins (below), or include individual files as needed -->' \
           '        <script src="js/bootstrap.min.js"></script>' \
           '    </body>' \
           '</html>'

if __name__ == '__main__':
    app.run()