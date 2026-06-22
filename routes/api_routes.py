from flask import Blueprint, request, jsonify, Response
from modules.password_analyzer import analyze_password
from modules.password_generator import (
    generate_random_password,
    generate_passphrase,
)
from modules.breach_checker import check_password_breach
from hashing import (
    sha256_hash,
    sha512_hash,
    bcrypt_hash,
    scrypt_hash,
    argon2_hash,
)
from services.export_service import ExportService
from services.graph_service import GraphDataService

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/analyze", methods=["POST"])
def analyze():
    """
    Analyzes password strength, entropy, crack time, breaches, and AI advice.
    """
    data = request.get_json() or {}
    password = data.get("password", "")
    check_breaches = data.get("check_breaches", True)

    # Run analysis
    analysis = analyze_password(password, check_breaches=check_breaches)

    # Add graph datasets for Chart.js representation
    analysis["graph_character_distribution"] = (
        GraphDataService.get_character_distribution(password)
    )
    analysis["graph_entropy_curve"] = (
        GraphDataService.get_entropy_growth_curve(password)
    )

    return jsonify(analysis)


@api_bp.route("/generate", methods=["POST"])
def generate():
    """
    Generates a password or passphrase based on options.
    """
    data = request.get_json() or {}
    mode = data.get("mode", "password")  # "password" or "passphrase"

    if mode == "password":
        length = int(data.get("length", 12))
        use_lower = data.get("use_lowercase", True)
        use_upper = data.get("use_uppercase", True)
        use_digits = data.get("use_digits", True)
        use_special = data.get("use_special", True)
        exclude_similar = data.get("exclude_similar", False)

        pwd = generate_random_password(
            length=length,
            use_lower=use_lower,
            use_upper=use_upper,
            use_digits=use_digits,
            use_special=use_special,
            exclude_similar=exclude_similar,
        )
    else:
        word_count = int(data.get("word_count", 4))
        separator = data.get("separator", "-")
        capitalize = data.get(
            "capitalize", "title"
        )  # "title", "upper", "lower"
        include_number = data.get("include_number", True)

        pwd = generate_passphrase(
            word_count=word_count,
            separator=separator,
            capitalize=capitalize,
            include_number=include_number,
        )

    return jsonify({"password": pwd})


@api_bp.route("/breach-check", methods=["POST"])
def breach_check():
    """
    Direct endpoint for checking password breach count.
    """
    data = request.get_json() or {}
    password = data.get("password", "")

    breach_count = check_password_breach(password)
    return jsonify({"breach_count": breach_count})


@api_bp.route("/hash-benchmark", methods=["POST"])
def hash_benchmark():
    """
    Runs a speed benchmark for a specific hashing algorithm with custom parameters.
    """
    data = request.get_json() or {}
    password = data.get("password", "")
    algo = data.get(
        "algorithm", "sha256"
    )  # "sha256", "sha512", "bcrypt", "scrypt", "argon2"

    hashed = ""
    time_ms = 0.0

    try:
        if algo == "sha256":
            iterations = int(data.get("iterations", 1))
            hashed, time_ms = sha256_hash.benchmark_hash(
                password, iterations=iterations
            )
        elif algo == "sha512":
            iterations = int(data.get("iterations", 1))
            hashed, time_ms = sha512_hash.benchmark_hash(
                password, iterations=iterations
            )
        elif algo == "bcrypt":
            rounds = int(data.get("rounds", 10))
            hashed, time_ms = bcrypt_hash.benchmark_hash(
                password, rounds=rounds
            )
        elif algo == "scrypt":
            n = int(data.get("n", 16384))
            r = int(data.get("r", 8))
            p = int(data.get("p", 1))
            hashed, time_ms = scrypt_hash.benchmark_hash(
                password, n=n, r=r, p=p
            )
        elif algo == "argon2":
            time_cost = int(data.get("time_cost", 2))
            memory_cost = int(data.get("memory_cost", 65536))
            parallelism = int(data.get("parallelism", 4))
            hashed, time_ms = argon2_hash.benchmark_hash(
                password,
                time_cost=time_cost,
                memory_cost=memory_cost,
                parallelism=parallelism,
            )
        else:
            return jsonify({"error": "Unknown hashing algorithm"}), 400

        return jsonify(
            {"algorithm": algo, "hash": hashed, "duration_ms": time_ms}
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/export", methods=["POST"])
def export_report():
    """
    Generates and returns export downloadable reports.
    """
    data = request.get_json() or {}
    password = data.get("password", "")
    format_type = data.get("format", "text")  # "text" or "json"

    # Run analysis
    analysis = analyze_password(password, check_breaches=True)

    if format_type == "json":
        file_content = ExportService.export_to_json(analysis)
        filename = "securepass_report.json"
        mimetype = "application/json"
    else:
        file_content = ExportService.export_to_text(password, analysis)
        filename = "securepass_report.txt"
        mimetype = "text/plain"

    return Response(
        file_content,
        mimetype=mimetype,
        headers={"Content-disposition": f"attachment; filename={filename}"},
    )
