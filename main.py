from app import create_app

if __name__ == "__main__":
    app = create_app()
    app.run("127.0.0.1", port=8080, debug=True)
