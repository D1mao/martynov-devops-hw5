import os
import psycopg2
from flask import Flask, jsonify


CONFIG_PATH = "/app/config/app.env"


def load_config(path: str) -> dict:
    config = {}

    if not os.path.exists(path):
        return config

    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            if "=" in line:
                key, value = line.split("=", 1)
                config[key.strip()] = value.strip()

    return config


config = load_config(CONFIG_PATH)

APP_NAME = config.get("APP_NAME", "DevOps Flask App")
DB_HOST = config.get("DB_HOST", "new_db")
DB_PORT = config.get("DB_PORT", "5432")
DB_NAME = config.get("DB_NAME", "devops_db")
DB_USER = config.get("DB_USER", "devops_user")
DB_PASSWORD = config.get("DB_PASSWORD", "devops_password")

app = Flask(__name__)


@app.get("/")
def index():
    return jsonify(
        {
            "message": "Nginx + Flask application is running",
            "app_name": APP_NAME,
            "db_host": DB_HOST,
            "available_db_names": ["new_db", "dev_db"],
        }
    )


@app.get("/api/health")
def health():
    return jsonify(
        {
            "status": "ok",
            "service": APP_NAME,
        }
    )


@app.get("/api/db-check")
def db_check():
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            connect_timeout=3,
        )

        cursor = connection.cursor()
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()[0]

        cursor.close()
        connection.close()

        return jsonify(
            {
                "status": "ok",
                "message": "Database connection successful",
                "db_host": DB_HOST,
                "db_version": db_version,
            }
        )

    except Exception as error:
        return jsonify(
            {
                "status": "error",
                "message": "Database connection failed",
                "error": str(error),
            }
        ), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)