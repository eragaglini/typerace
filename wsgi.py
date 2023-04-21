from App.main import create_app

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()

if __name__=='__main__':
    app.run()