from flask import Flask

app = Flask(__name__)

# Define your routes and Flask code for both development and production here
# You can define the routes and Flask code directly in this file

if __name__ == '__main__':
    # Manually enter the code for Prod or Local environment
    choice = 1

    if choice == 1:
        # Import and run Devapp.py for local development
        from local_dev.Devapp import app as dev_app
        dev_app.run(debug=True)
    elif choice == 2:
        # Import and run Prodapp.py for production
        from prod.Prodapp import app as prod_app
        prod_app.run(host='0.0.0.0', port=80)
