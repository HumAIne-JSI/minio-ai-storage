import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

from minio_humaine_client.auth import HumaineAuth

import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

HUMAINE_API_BASE_URL = os.getenv("HUMAINE_API_BASE_URL", "http://localhost:8000")
HUMAINE_API_TIMEOUT = int(os.getenv("HUMAINE_TIMEOUT", 30))
HUMAINE_API_USERNAME = os.getenv("HUMAINE_API_USERNAME", "user")
HUMAINE_API_PASSWORD = os.getenv("HUMAINE_API_PASSWORD", "pass")

from pprint import pprint

def main():
    print("🔐 Logging in to Humaine API...")
    auth = HumaineAuth(HUMAINE_API_BASE_URL)
    token = auth.login(HUMAINE_API_USERNAME, HUMAINE_API_PASSWORD)
    print("✅ Login successful.\n")

    print("📦 Fetching available buckets...")
    buckets = auth.list_buckets()
    print("Available Buckets:")
    for b in buckets:
        print(f"  - {b}")
    print()

    selected_bucket = "smart-finance-results"
    print(f"📁 Selecting bucket: {selected_bucket}")
    auth.select_bucket(selected_bucket)
    print("✅ Bucket selected.\n")

    print("📄 Listing objects in selected bucket...")
    objects = auth.list_objects()
    if objects:
        print("Objects:")
        for obj in objects:
            print(f"  - {obj}")
    else:
        print("⚠️  No objects found.")

    print("\n🏷️  Uploading a file to the selected bucket...")

    # create a simple model pickle file
    print("📦 Generating pickle file ...")
    iris = load_iris()
    X_train, X_test, y_train, y_test = train_test_split(
        iris.data, iris.target, test_size=0.2, random_state=42
    )

    # Train a model
    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    # Save the model to a .pkl file
    with open("tmp/test_random_forest.pkl", "wb") as f:
        pickle.dump(model, f)

    print("✅ Model saved to iris_random_forest.pkl")

    object_name = "test_random_forest.pkl"
    filepath = "tmp/test_random_forest.pkl"
    response = auth.upload_object(object_name, filepath)
    print("✅ File uploaded successfully.")

    # update metadata
    print("🏷️  Updating metadata for the uploaded object...")
    metadata = {
        "description": "Random Forest model for Iris dataset",
        "version": "1.0",
        "author": "Klemen Kenda",
    }
    response = auth.update_metadata(object_name, metadata)
    print("✅ Metadata updated successfully.")

    # get metadata
    print("📄 Fetching metadata for the uploaded object...")
    response = auth.get_metadata(object_name)
    print("✅ Metadata fetched successfully.")
    print("Metadata:")
    pprint(response)
    print()


if __name__ == "__main__":
    main()