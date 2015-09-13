import os
from main import application

application.debug = True
application.config['SECRET_KEY'] = 'secret!'
port = os.getenv('APP_PORT', '5000')

if __name__ == '__main__':
    application.run(debug=True, host='0.0.0.0', port=int(port))
