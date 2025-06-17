from flask import Flask, request, jsonify
import os
import json

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/collect", methods=["GET"])
def collect():
    result_dir = "/k6_results"
    if not os.path.exists(result_dir):
        return jsonify({
            "error": f"Directory {result_dir} does not exist",
            "json_results": [],
            "log_results": [],
            "debug_info": {}
        })

    files = os.listdir(result_dir)

    json_results = {}
    log_results = {}

    for f in files:
        file_path = os.path.join(result_dir, f)
        test_case_id = f.replace(".json", "").replace(".log", "")

        try:
            if f.endswith(".json"):
                with open(file_path, "r") as file:
                    content = json.load(file)
                    json_results[test_case_id] = content

            elif f.endswith(".log"):
                with open(file_path, "r") as file:
                    content = file.read()
                    log_results[test_case_id] = content

        except Exception as e:
            print(f"Error reading {f}: {e}")

    return jsonify({
        "error": None,
        "json_results": json_results,
        "log_results": log_results,
        "debug_info": {"files_found": files}
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)