from service.app import create_app

app = create_app(config='config.py')


if __name__ == '__main__':
    app.run()
