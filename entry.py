from service.app import create_app

app = create_app(config='service/config.py')


if __name__ == '__main__':
    app.run()
