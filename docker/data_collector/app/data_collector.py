from flask import Flask, request, jsonify
import os
import json
import subprocess

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

@app.route("/save-k6-script", methods=["POST"])
def save_k6_script_route():
    payload = request.json
    test_cases = payload.get("payload")

    if not isinstance(test_cases, list):
        return jsonify({
            "status": "error",
            "message": "Missing or invalid 'payload' (must be a list)"
        }), 400

    results = []

    for test_case in test_cases:
        name = test_case.get("test_case")
        script = test_case.get("script")

        if not name:
            results.append({
                "test_case": None,
                "status": "error",
                "message": "Missing 'test_case'"
            })
            continue

        if script is None:
            results.append({
                "test_case": name,
                "status": "skipped",
                "message": "Script is null, file not saved"
            })
            continue

        ext = ".js" if not name.endswith(".js") else ""
        try:
            file_path = save_k6_script(f"{name}{ext}", script)
            results.append({
                "test_case": name,
                "status": "success",
                "file_path": file_path
            })
        except Exception as e:
            results.append({
                "test_case": name,
                "status": "error",
                "message": str(e)
            })

    return jsonify(results)

@app.route("/execute-k6", methods=["GET"])
def execute_k6_route():
    silent = request.args.get("silent", "false").lower() == "true"

    try:
        output = execute_sh_file(silent=silent)
        return jsonify({
            "status": "executed",
            "output": output
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

def save_k6_script(test_case: str, script: str):
    scripts_dir = "/k6/scripts"
    os.makedirs(scripts_dir, exist_ok=True)

    file_name = test_case if test_case.endswith('.js') else f"{test_case}.js"
    file_path = os.path.join(scripts_dir, file_name)

    print(f"[save_k6_script] Writing to: {file_path}")
    print(f"[save_k6_script] Script content (first 200 chars): {script[:200]}")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(script)

    return file_path

def execute_sh_file(silent=False):
    print("[execute_sh_file] Running run_k6.sh ...")
    result = subprocess.run(
        ["sh", "run_tests.sh"],
        cwd="/k6",
        capture_output=True,
        text=True
    )

    if not silent:
        print("[execute_sh_file] STDOUT:\n", result.stdout)
        print("[execute_sh_file] STDERR:\n", result.stderr)
        print("[execute_sh_file] Exit Code:", result.returncode)

    return {
        "stdout": result.stdout,
        "stderr": result.stderr,
        "exit_code": result.returncode
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)