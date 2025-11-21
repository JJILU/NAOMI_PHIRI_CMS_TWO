from app import create_app

app = create_app()

if __name__ == "__main__":
    # uncomment below line in production
    # app.run(debug=False,port=5001)
    # comment in production & uncomment line below in development
    app.run(debug=True,port=5001)