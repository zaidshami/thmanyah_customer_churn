import os
import requests

scripts = {
    "feature_engineering.py": "https://raw.githubusercontent.com/zaidshami/thmanyah_customer_churn/refs/heads/develop/sagemaker_pipeline/feature_engineering.py",
    "evaluate.py": "https://raw.githubusercontent.com/zaidshami/thmanyah_customer_churn/refs/heads/develop/sagemaker_pipeline/evaluate.py"
}

output_dir = "/opt/ml/processing/output/scripts"
os.makedirs(output_dir, exist_ok=True)

for filename, url in scripts.items():
    print(f"Downloading {filename} from {url}...")
    response = requests.get(url)
    if response.status_code == 200:
        with open(os.path.join(output_dir, filename), "w") as f:
            f.write(response.text)
        print(f"✅ Saved {filename}")
    else:
        print(f"❌ Failed to download {filename}")