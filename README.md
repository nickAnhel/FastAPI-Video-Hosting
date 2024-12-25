# ТипоTube 📽
**ТипоTube** is a modern platform where users can view and rate videos posted by other people, share their opinions in comments and own videos, and create collections on various topics using a playlist system. In addition, the platform provides a modern notification system for the release of new videos - notifications can be viewed both on the platform itself, as well as in Email or Telegram.
# Requirements
To start a project, you need to have a number of installed programs and utilities:
- `poetry`
- `python3.12`
- `docker` and `docker-compose`
- `git`
# Deploy
To run this project on local machine or on server follow the steps down bellow.

Go to the `server` directory, create a `certs` directory and navigate in it.
```bash
# Create a dir to store the keys
md certs
cd certs
```

Create private and public encryption keys.

Linux
```bash
# Create a private key
openssl genrsa -out private.pem 2048

# Create a public key
openssl rsa -in private.pem -outform PEM -pubout -out public.pem
```
Windows
```bash
# Create a private key
"C:\Program Files\Git\usr\bin\openssl.exe" genrsa -out private.pem 2048

# Create a public key
"C:\Program Files\Git\usr\bin\openssl.exe" rsa -in private.pem -outform PEM -pubout -out public.pem
```

Next, you need to find all env files ending in `.example`, create the same files next to each of them (but without the `.example` in the name) and fill them with your own data based on the examples.

In some files, you will need to insert secret keys or salt. You can generate them using the command below.

Linux
```bash
openssl rand -base64 32
```
Windows
```bash
"C:\Program Files\Git\usr\bin\openssl.exe" rand -base64 32
```

Pay attention to the files with the name `.docker-env` in the `server` and `notifications_bot` directories. The environment variable `VERIFICATION_SECRET_KEY` in the `server` directory must have the same value as the environment variable `SECRET_KEY` in the `notifications_bot` directory. Also, the environment variable `VERIFICATION_SALT` in the `server` directory must have the same value as the environment variable `SALT` in the `notifications_bot` directory.

Now go to the root directory of the project and start it using `docker`.
```bash
docker compose up --build
```