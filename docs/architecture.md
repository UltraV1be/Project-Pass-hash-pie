# System Architecture: SecurePass-Intelligence

SecurePass-Intelligence is a modular password evaluation and benchmarking platform designed to demonstrate modern cybersecurity password best practices.

## Modular Component Overview

```mermaid
graph TD
    UI[HTML/JS Frontend Templates] -->|AJAX| API[api_routes.py Blueprint]
    API -->|analyze| Orchestrator[password_analyzer.py]
    API -->|generate| Generator[password_generator.py]
    API -->|benchmark| HashLab[Hashing Modules]
    
    Orchestrator --> Entropy[entropy_calculator.py]
    Orchestrator --> Strength[strength_calculator.py]
    Orchestrator --> Breach[breach_checker.py]
    Orchestrator --> Estimator[crack_time_estimator.py]
    
    Breach --> HIBP[hibp_service.py Client]
    HIBP -->|HTTPS GET| HIBPApi[HaveIBeenPwned API]
    
    Orchestrator --> Risk[risk_engine.py]
    Orchestrator --> Suggestion[suggestion_engine.py]
    Orchestrator --> AI[ai_advisor.py]
```

## Core Engine Flow

The following sequence diagram outlines the process when a user inputs a password for analysis:

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant BackendAPI
    participant Analyzer
    participant HIBP

    User->>Frontend: Types Password
    Frontend->>BackendAPI: POST /api/analyze {password}
    BackendAPI->>Analyzer: analyze_password(pwd)
    
    par Mathematical Scoring
        Analyzer->>Analyzer: Calculate Entropy (H)
        Analyzer->>Analyzer: Estimate Crack Times
    and Heuristic Analysis
        Analyzer->>Analyzer: Dictionary checks
        Analyzer->>Analyzer: Pattern mapping
    and Breach Checking
        Analyzer->>HIBP: GET range check (k-Anonymity)
        HIBP-->>Analyzer: Leaked hashes
    end
    
    Analyzer-->>BackendAPI: Security Metrics JSON
    BackendAPI-->>Frontend: JSON Response
    Frontend-->>User: Render Gauges & Warnings
```

## Cryptographic Mathematics

### 1. Shannon Entropy

Entropy ($$H$$) measures the unpredictability or randomness of the password. It is calculated based on the length of the password ($$L$$) and the size of the character pool ($$R$$).

$$
H = L \times \log_2(R)
$$

- **$$L$$ (Length)**: The number of characters in the password.
- **$$R$$ (Pool Size)**: The total number of unique characters in the sets used (e.g., 26 lowercase + 26 uppercase + 10 digits = 62).

*Higher entropy means the password is exponentially harder to brute-force.*

### 2. Crack Time Estimation

Crack time is the estimated time it would take an attacker to guess the password. For pure brute-force attacks, the mathematical relationship is defined by the total number of possible combinations ($$N$$) divided by the attacker's guessing speed ($$S$$).

Total combinations:
$$
N = R^L = 2^H
$$

Estimated Time to Crack:
$$
\text{Time (seconds)} = \frac{N}{S} = \frac{2^H}{S}
$$

- **$$S$$ (Speed)**: Guesses per second. Online attacks might be limited to 100 guesses/sec. Offline hardware attacks (using GPUs) can easily reach $$10^{10}$$ (10 billion) guesses/sec against weak hashing functions like MD5 or SHA-1.


### 1. Presentation Layer (`templates/` & `static/`)
- **Control Cockpits**: Rendered via Flask templates (`index.html`, `analysis.html`, `generator.html`, `breach.html`, `hashing.html`, `dashboard.html`).
- **Styling**: Managed in `style.css` using slate glassmorphic panels, Outfits typography, and custom variables for semantic feedback.
- **Client Logic (`main.js`)**: Debounces input events, makes AJAX fetch requests to JSON routes, runs clipboards integration, and renders charts via Chart.js.

### 2. Service Layer (`services/`)
- **HIBP Service (`hibp_service.py`)**: Responsible for querying the HaveIBeenPwned range API using the first 5 characters of a password's SHA-1 hash (k-Anonymity privacy technique).
- **Graph Service (`graph_service.py`)**: Formats character categories and creates data grids for line/pie charts.
- **Export Service (`export_service.py`)**: Compiles assessment summaries into JSON and structured plain text files.

### 3. Hashing Sandbox (`hashing/`)
Contains wrappers to benchmark and evaluate:
- Fast hashing: SHA-256 and SHA-512.
- Key Derivation Functions: Bcrypt, Scrypt, and Argon2id.

### 4. Engine & Analysis Modules (`modules/`)
- **Password Analyzer (`password_analyzer.py`)**: Serves as the main orchestrator, collecting all metrics.
- **Entropy Calculator (`entropy_calculator.py`)**: Computes Shannon entropy dynamically.
- **Strength Calculator (`strength_calculator.py`)**: Scores passwords against dictionary lookups, keyboard walk lists, and sequences.
- **Risk Engine (`risk_engine.py`)**: Evaluates overall risk level.
- **AI Advisor (`ai_advisor.py`)**: Fallback expert advice system with optional Google Gemini integration.
