/* ==========================================================================
   SecurePass-Intelligence Client-Side Orchestrator
   ========================================================================== */

document.addEventListener("DOMContentLoaded", () => {
    initNavigation();
    
    // Feature Detect and Route Page Handlers
    if (document.getElementById("passwordInput")) {
        initAnalyzerPage();
    }
    if (document.getElementById("generateBtn")) {
        initGeneratorPage();
    }
    if (document.getElementById("scanBreachBtn")) {
        initBreachPage();
    }
    if (document.getElementById("runBenchmarkBtn")) {
        initHashingPage();
    }
});

/* 1. Shared Helper Functions */
function initNavigation() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll(".nav-link");
    navLinks.forEach(link => {
        const href = link.getAttribute("href");
        if (href === currentPath || (currentPath === "/dashboard" && href === "/dashboard")) {
            link.classList.add("active");
        } else if (currentPath === "/" && href === "/") {
            link.classList.add("active");
        } else {
            link.classList.remove("active");
        }
    });
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function getBadgeClassByScore(score) {
    if (score >= 80) return "badge-emerald";
    if (score >= 60) return "badge-cyan";
    if (score >= 40) return "badge-amber";
    return "badge-crimson";
}

function getBadgeClassByRisk(riskLevel) {
    if (riskLevel === "Critical") return "text-crimson";
    if (riskLevel === "High") return "text-crimson";
    if (riskLevel === "Medium") return "text-amber";
    return "text-emerald";
}

function getProgressColorByScore(score) {
    if (score >= 80) return "hsl(145, 80%, 45%)"; // Emerald
    if (score >= 60) return "hsl(180, 100%, 50%)"; // Cyan
    if (score >= 40) return "hsl(40, 95%, 55%)"; // Amber
    return "hsl(350, 85%, 50%)"; // Crimson
}


/* 2. Password Analyzer Page Logic */
function initAnalyzerPage() {
    const passwordInput = document.getElementById("passwordInput");
    const togglePasswordBtn = document.getElementById("togglePasswordBtn");
    const toggleIcon = document.getElementById("toggleIcon");
    const checkBreachesCheckbox = document.getElementById("checkBreachesCheckbox");
    
    const scoreProgressCircle = document.getElementById("scoreProgressCircle");
    const scoreText = document.getElementById("scoreText");
    const ratingBadge = document.getElementById("ratingBadge");
    const entropyValue = document.getElementById("entropyValue");
    const entropyDesc = document.getElementById("entropyDesc");
    const riskLevelText = document.getElementById("riskLevelText");
    const riskDesc = document.getElementById("riskDesc");
    const breachCountText = document.getElementById("breachCountText");
    const breachDesc = document.getElementById("breachDesc");
    
    const onlineCrackTime = document.getElementById("onlineCrackTime");
    const offlineFastCrackTime = document.getElementById("offlineFastCrackTime");
    const offlineSlowCrackTime = document.getElementById("offlineSlowCrackTime");
    
    const warningsList = document.getElementById("warningsList");
    const suggestionsList = document.getElementById("suggestionsList");
    const aiAdviceContent = document.getElementById("aiAdviceContent");
    
    const exportTxtBtn = document.getElementById("exportTxtBtn");
    const exportJsonBtn = document.getElementById("exportJsonBtn");

    // Circumference of SVG circle (r = 70) => 2 * pi * 70 = 439.82
    const circleCircumference = 439.82;
    scoreProgressCircle.style.strokeDasharray = circleCircumference;
    scoreProgressCircle.style.strokeDashoffset = circleCircumference;

    // Chart.js references
    let charDistChart = null;
    let entropyCurveChart = null;

    // Toggle password view
    togglePasswordBtn.addEventListener("click", () => {
        if (passwordInput.type === "password") {
            passwordInput.type = "text";
            toggleIcon.className = "fa-solid fa-eye-slash";
        } else {
            passwordInput.type = "password";
            toggleIcon.className = "fa-solid fa-eye";
        }
    });

    // Main analysis event
    const runAnalysis = async () => {
        const password = passwordInput.value;
        if (!password) {
            resetAnalyzer();
            return;
        }

        const checkBreaches = checkBreachesCheckbox.checked;

        try {
            const response = await fetch("/api/analyze", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ password, check_breaches: checkBreaches })
            });

            if (!response.ok) throw new Error("Analysis failed");
            const data = await response.json();
            
            updateAnalyzerUI(data);
            enableExportButtons(true);

        } catch (error) {
            console.error("Error analyzing password:", error);
        }
    };

    const resetAnalyzer = () => {
        scoreText.innerText = "0";
        scoreProgressCircle.style.strokeDashoffset = circleCircumference;
        scoreProgressCircle.style.stroke = "var(--cyan-primary)";
        
        ratingBadge.innerText = "No Input";
        ratingBadge.className = "badge badge-gray";
        
        entropyValue.innerHTML = `0.00 <span class="unit">bits</span>`;
        entropyDesc.innerText = "Pool size: 0 characters";
        
        riskLevelText.innerText = "None";
        riskLevelText.className = "text-gray";
        riskDesc.innerText = "Vulnerability flag";
        
        breachCountText.innerHTML = `0 <span class="unit">leaks</span>`;
        breachCountText.className = "text-emerald";
        breachDesc.innerText = "Compromise database count";
        
        onlineCrackTime.innerText = "Instant";
        offlineFastCrackTime.innerText = "Instant";
        offlineSlowCrackTime.innerText = "Instant";
        
        warningsList.innerHTML = `<li class="empty-list-placeholder">No vulnerabilities flagged.</li>`;
        suggestionsList.innerHTML = `<li class="empty-list-placeholder">Checklist will populate on input.</li>`;
        aiAdviceContent.innerText = "Input a password to receive an expert cybersecurity advisory statement.";
        
        enableExportButtons(false);
        destroyCharts();
    };

    const enableExportButtons = (enable) => {
        exportTxtBtn.disabled = !enable;
        exportJsonBtn.disabled = !enable;
    };

    const destroyCharts = () => {
        if (charDistChart) charDistChart.destroy();
        if (entropyCurveChart) entropyCurveChart.destroy();
        charDistChart = null;
        entropyCurveChart = null;
    };

    const updateAnalyzerUI = (data) => {
        const score = data.strength.score;
        const rating = data.strength.rating;
        const warnings = data.strength.warnings;
        const details = data.strength.details;
        const entropyVal = data.entropy.entropy;
        const poolSize = data.entropy.pool_size;
        const crackTimes = data.crack_times;
        const risk = data.risk;
        const breachCount = data.breach_count;
        const suggestions = data.suggestions;
        const aiAdvice = data.ai_advice;

        // 1. Progress circle & score text
        scoreText.innerText = score;
        const dashOffset = circleCircumference - (score / 100) * circleCircumference;
        scoreProgressCircle.style.strokeDashoffset = dashOffset;
        scoreProgressCircle.style.stroke = getProgressColorByScore(score);

        // 2. Rating Badge
        ratingBadge.innerText = rating;
        ratingBadge.className = `badge ${getBadgeClassByScore(score)}`;

        // 3. Metrics Summary
        entropyValue.innerHTML = `${entropyVal.toFixed(2)} <span class="unit">bits</span>`;
        entropyDesc.innerText = `Pool size: ${poolSize} characters`;

        riskLevelText.innerText = risk.risk_level;
        riskLevelText.className = getBadgeClassByRisk(risk.risk_level);
        riskDesc.innerText = risk.reasons.length > 0 ? risk.reasons[0] : "Vulnerability flag";

        breachCountText.innerHTML = `${breachCount.toLocaleString()} <span class="unit">leaks</span>`;
        if (breachCount > 0) {
            breachCountText.className = "text-crimson";
            breachDesc.innerText = "Password found in public leaks";
        } else {
            breachCountText.className = "text-emerald";
            breachDesc.innerText = "No compromised registers match";
        }

        // 4. Crack Times
        onlineCrackTime.innerText = crackTimes.online_readable;
        offlineFastCrackTime.innerText = crackTimes.offline_fast_readable;
        offlineSlowCrackTime.innerText = crackTimes.offline_slow_readable;

        // 5. Warnings List
        warningsList.innerHTML = "";
        if (warnings.length > 0) {
            warnings.forEach(warn => {
                const li = document.createElement("li");
                li.innerText = warn;
                warningsList.appendChild(li);
            });
        } else {
            warningsList.innerHTML = `<li class="empty-list-placeholder">No vulnerabilities flagged.</li>`;
        }

        // 6. Suggestions checklist
        suggestionsList.innerHTML = "";
        if (suggestions.length > 0) {
            suggestions.forEach(sug => {
                const li = document.createElement("li");
                li.innerText = sug;
                suggestionsList.appendChild(li);
            });
        } else {
            suggestionsList.innerHTML = `<li class="empty-list-placeholder">All indicators healthy.</li>`;
        }

        // 7. AI advice
        aiAdviceContent.innerText = aiAdvice;

        // 8. Re-draw Charts
        destroyCharts();
        renderCharDistChart(data.graph_character_distribution);
        renderEntropyCurveChart(data.graph_entropy_curve);
    };

    const renderCharDistChart = (chartData) => {
        const ctx = document.getElementById("charDistChart").getContext("2d");
        charDistChart = new Chart(ctx, {
            type: "doughnut",
            data: {
                labels: chartData.labels,
                datasets: [{
                    data: chartData.values,
                    backgroundColor: [
                        "rgba(0, 242, 254, 0.6)",
                        "rgba(79, 172, 254, 0.6)",
                        "rgba(16, 185, 129, 0.6)",
                        "rgba(245, 158, 11, 0.6)",
                        "rgba(239, 68, 68, 0.6)"
                    ],
                    borderColor: "rgba(7, 10, 19, 0.8)",
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: "right",
                        labels: {
                            color: "#94a3b8",
                            font: { size: 10, family: "Plus Jakarta Sans" }
                        }
                    }
                }
            }
        });
    };

    const renderEntropyCurveChart = (chartData) => {
        const ctx = document.getElementById("entropyCurveChart").getContext("2d");
        entropyCurveChart = new Chart(ctx, {
            type: "line",
            data: {
                labels: chartData.lengths,
                datasets: [{
                    label: "Shannon Entropy (bits)",
                    data: chartData.entropies,
                    borderColor: "rgba(0, 242, 254, 0.8)",
                    backgroundColor: "rgba(0, 242, 254, 0.05)",
                    borderWidth: 2,
                    fill: true,
                    tension: 0.3
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    x: {
                        grid: { color: "rgba(255,255,255,0.03)" },
                        ticks: { color: "#94a3b8", font: { size: 9 } }
                    },
                    y: {
                        grid: { color: "rgba(255,255,255,0.03)" },
                        ticks: { color: "#94a3b8", font: { size: 9 } }
                    }
                }
            }
        });
    };

    // Debounce analysis triggering
    const debouncedAnalysis = debounce(runAnalysis, 250);
    passwordInput.addEventListener("input", debouncedAnalysis);
    checkBreachesCheckbox.addEventListener("change", runAnalysis);

    // Export Action handlers
    const triggerExport = (format) => {
        const password = passwordInput.value;
        if (!password) return;

        // Post request to export route to trigger file download
        const form = document.createElement("form");
        form.method = "POST";
        form.action = "/api/export";
        form.target = "_blank";

        // Embed form elements
        const inputPwd = document.createElement("input");
        inputPwd.type = "hidden";
        inputPwd.name = "password";
        inputPwd.value = password;
        form.appendChild(inputPwd);

        const formatType = document.createElement("input");
        formatType.type = "hidden";
        formatType.name = "format";
        formatType.value = format;
        form.appendChild(formatType);

        // Append to DOM, submit, and remove
        document.body.appendChild(form);
        form.submit();
        document.body.removeChild(form);
    };

    // We override standard form action using fetch and download file
    const triggerExportFetch = async (format) => {
        const password = passwordInput.value;
        if (!password) return;

        try {
            const response = await fetch("/api/export", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ password, format })
            });

            if (!response.ok) throw new Error("Export failed");
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = format === "json" ? "securepass_report.json" : "securepass_report.txt";
            document.body.appendChild(a);
            a.click();
            a.remove();
            window.URL.revokeObjectURL(url);
        } catch (err) {
            console.error("Export download failed:", err);
        }
    };

    exportTxtBtn.addEventListener("click", () => triggerExportFetch("text"));
    exportJsonBtn.addEventListener("click", () => triggerExportFetch("json"));
}


/* 3. Credentials Generator Page Logic */
function initGeneratorPage() {
    const tabPasswordBtn = document.getElementById("tabPasswordBtn");
    const tabPassphraseBtn = document.getElementById("tabPassphraseBtn");
    const tabKeywordBtn = document.getElementById("tabKeywordBtn");
    const passwordTabContent = document.getElementById("passwordTabContent");
    const passphraseTabContent = document.getElementById("passphraseTabContent");
    const keywordTabContent = document.getElementById("keywordTabContent");
    
    // Sliders
    const charLength = document.getElementById("charLength");
    const charLengthValue = document.getElementById("charLengthValue");
    const wordCount = document.getElementById("wordCount");
    const wordCountValue = document.getElementById("wordCountValue");
    
    // Options Password
    const genLower = document.getElementById("genLower");
    const genUpper = document.getElementById("genUpper");
    const genDigits = document.getElementById("genDigits");
    const genSpecial = document.getElementById("genSpecial");
    const genExcludeSimilar = document.getElementById("genExcludeSimilar");
    
    // Options Passphrase
    const passSeparator = document.getElementById("passSeparator");
    const passCapitalize = document.getElementById("passCapitalize");
    const passIncludeNumber = document.getElementById("passIncludeNumber");
    
    // Options Keyword
    const keywordInput = document.getElementById("keywordInput");
    const keywordLength = document.getElementById("keywordLength");
    const keywordLengthValue = document.getElementById("keywordLengthValue");
    const keyLeetspeak = document.getElementById("keyLeetspeak");
    const keyNumbers = document.getElementById("keyNumbers");
    const keySpecial = document.getElementById("keySpecial");
    
    // Action triggers
    const generateBtn = document.getElementById("generateBtn");
    const generatedPasswordBox = document.getElementById("generatedPasswordBox");
    const copyPasswordBtn = document.getElementById("copyPasswordBtn");
    const copyNotification = document.getElementById("copyNotification");
    
    // Visual Assessment fields
    const genStrengthBar = document.getElementById("genStrengthBar");
    const genScoreText = document.getElementById("genScoreText");
    const genRatingBadge = document.getElementById("genRatingBadge");
    const genEntropyText = document.getElementById("genEntropyText");
    const genCrackTimeText = document.getElementById("genCrackTimeText");

    let currentMode = "password"; // "password" or "passphrase"

    // Tab togglers
    tabPasswordBtn.addEventListener("click", () => {
        currentMode = "password";
        tabPasswordBtn.classList.add("active");
        tabPassphraseBtn.classList.remove("active");
        tabKeywordBtn.classList.remove("active");
        passwordTabContent.classList.add("active");
        passphraseTabContent.classList.remove("active");
        keywordTabContent.classList.remove("active");
        generateCredentials();
    });

    tabPassphraseBtn.addEventListener("click", () => {
        currentMode = "passphrase";
        tabPassphraseBtn.classList.add("active");
        tabPasswordBtn.classList.remove("active");
        tabKeywordBtn.classList.remove("active");
        passphraseTabContent.classList.add("active");
        passwordTabContent.classList.remove("active");
        keywordTabContent.classList.remove("active");
        generateCredentials();
    });

    tabKeywordBtn.addEventListener("click", () => {
        currentMode = "keyword";
        tabKeywordBtn.classList.add("active");
        tabPasswordBtn.classList.remove("active");
        tabPassphraseBtn.classList.remove("active");
        keywordTabContent.classList.add("active");
        passwordTabContent.classList.remove("active");
        passphraseTabContent.classList.remove("active");
        generateCredentials();
    });

    // Slider syncs
    charLength.addEventListener("input", () => {
        charLengthValue.innerText = charLength.value;
    });

    wordCount.addEventListener("input", () => {
        wordCountValue.innerText = wordCount.value;
    });

    keywordLength.addEventListener("input", () => {
        keywordLengthValue.innerText = keywordLength.value;
    });

    const generateCredentials = async () => {
        let payload = { mode: currentMode };
        
        if (currentMode === "password") {
            payload = {
                ...payload,
                length: charLength.value,
                use_lowercase: genLower.checked,
                use_uppercase: genUpper.checked,
                use_digits: genDigits.checked,
                use_special: genSpecial.checked,
                exclude_similar: genExcludeSimilar.checked
            };
        } else if (currentMode === "keyword") {
            payload = {
                ...payload,
                keyword: keywordInput.value,
                length: keywordLength.value,
                leetspeak: keyLeetspeak.checked,
                include_numbers: keyNumbers.checked,
                include_special: keySpecial.checked
            };
        } else {
            payload = {
                ...payload,
                word_count: wordCount.value,
                separator: passSeparator.value,
                capitalize: passCapitalize.value,
                include_number: passIncludeNumber.checked
            };
        }

        try {
            const response = await fetch("/api/generate", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });

            if (!response.ok) throw new Error("Generation failed");
            const data = await response.json();
            
            const pwd = data.password;
            generatedPasswordBox.innerText = pwd;
            
            // Run a quick local analysis benchmark on the generated password
            runQuickGenAnalysis(pwd);

        } catch (error) {
            console.error("Error generating credentials:", error);
        }
    };

    const runQuickGenAnalysis = async (password) => {
        try {
            // Fetch password analysis metrics from api (disable breach checking to keep it fast)
            const response = await fetch("/api/analyze", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ password, check_breaches: false })
            });

            if (!response.ok) return;
            const data = await response.json();

            // Update mini strength preview card
            const score = data.strength.score;
            const rating = data.strength.rating;
            const entropy = data.entropy.entropy;
            const crackTime = data.crack_times.offline_slow_readable;

            genScoreText.innerText = `${score}/100`;
            genStrengthBar.style.width = `${score}%`;
            genStrengthBar.style.backgroundColor = getProgressColorByScore(score);

            genRatingBadge.innerText = rating;
            genRatingBadge.className = `badge ${getBadgeClassByScore(score)}`;
            
            genEntropyText.innerText = `${entropy.toFixed(2)} bits`;
            genCrackTimeText.innerText = crackTime;

        } catch (error) {
            console.error("Error in generated analysis query:", error);
        }
    };

    // Clipboard copy action
    copyPasswordBtn.addEventListener("click", () => {
        const text = generatedPasswordBox.innerText;
        if (text === "Press Generate...") return;

        navigator.clipboard.writeText(text).then(() => {
            copyNotification.classList.add("show");
            setTimeout(() => {
                copyNotification.classList.remove("show");
            }, 2000);
        }).catch(err => {
            console.error("Failed to copy password:", err);
        });
    });

    generateBtn.addEventListener("click", generateCredentials);
    
    // Auto-generate a password on initial load
    generateCredentials();
}


/* 4. Breach Scanner Page Logic */
function initBreachPage() {
    const breachPasswordInput = document.getElementById("breachPasswordInput");
    const toggleBreachPasswordBtn = document.getElementById("toggleBreachPasswordBtn");
    const breachToggleIcon = document.getElementById("breachToggleIcon");
    const scanBreachBtn = document.getElementById("scanBreachBtn");
    const breachResultCard = document.getElementById("breachResultCard");
    
    const statusIconWrapper = document.getElementById("statusIconWrapper");
    const statusIcon = document.getElementById("statusIcon");
    const breachStatusTitle = document.getElementById("breachStatusTitle");
    const breachStatusDetails = document.getElementById("breachStatusDetails");

    toggleBreachPasswordBtn.addEventListener("click", () => {
        if (breachPasswordInput.type === "password") {
            breachPasswordInput.type = "text";
            breachToggleIcon.className = "fa-solid fa-eye-slash";
        } else {
            breachPasswordInput.type = "password";
            breachToggleIcon.className = "fa-solid fa-eye";
        }
    });

    const runScan = async () => {
        const password = breachPasswordInput.value;
        if (!password) return;

        // Show loading state
        breachResultCard.classList.remove("hide");
        statusIconWrapper.className = "status-icon-wrapper";
        statusIcon.className = "fa-solid fa-arrows-spin fa-spin";
        breachStatusTitle.innerText = "Scanning compromised databases...";
        breachStatusDetails.innerText = "Computing SHA-1 prefix checks. Local validation running.";

        try {
            const response = await fetch("/api/breach-check", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ password })
            });

            if (!response.ok) throw new Error("Breach check failed");
            const data = await response.json();
            
            const count = data.breach_count;
            updateBreachUI(count);

        } catch (error) {
            console.error("Breach check failed:", error);
            statusIconWrapper.className = "status-icon-wrapper";
            statusIcon.className = "fa-solid fa-circle-exclamation text-crimson";
            breachStatusTitle.innerText = "Scanning Failed";
            breachStatusDetails.innerText = "Could not reach database check servers. Check your internet connection.";
        }
    };

    const updateBreachUI = (count) => {
        if (count > 0) {
            statusIconWrapper.className = "status-icon-wrapper danger";
            statusIcon.className = "fa-solid fa-triangle-exclamation";
            breachStatusTitle.innerText = "Password Compromised!";
            breachStatusDetails.innerHTML = (
                `<p>This password was found in <strong>${count.toLocaleString()}</strong> public data leaks.</p>` +
                `<p class="margin-top-md text-muted text-small">This means this password has been exposed previously. Continuing to use this password across any accounts constitutes a severe security vulnerability. <strong>Change it immediately.</strong></p>`
            );
        } else {
            statusIconWrapper.className = "status-icon-wrapper safe";
            statusIcon.className = "fa-solid fa-shield-halved";
            breachStatusTitle.innerText = "No Exposed Leaks Found";
            breachStatusDetails.innerHTML = (
                `<p class="text-emerald">Safe. This password does not appear in known public compromised database records.</p>` +
                `<p class="margin-top-md text-muted text-small">This password is safe to use as long as it has high entropy and is not reused on other platforms.</p>`
            );
        }
    };

    scanBreachBtn.addEventListener("click", runScan);
}


/* 5. Cryptographic Hashing Workbench Logic */
function initHashingPage() {
    const hashInput = document.getElementById("hashInput");
    const hashAlgorithm = document.getElementById("hashAlgorithm");
    
    // Settings Sections
    const settingsSha256 = document.getElementById("settingsSha256");
    const settingsSha512 = document.getElementById("settingsSha512");
    const settingsBcrypt = document.getElementById("settingsBcrypt");
    const settingsScrypt = document.getElementById("settingsScrypt");
    const settingsArgon2 = document.getElementById("settingsArgon2");

    // Inputs inside setting sections
    const sha256Iterations = document.getElementById("sha256Iterations");
    const sha256IterationsVal = document.getElementById("sha256IterationsVal");
    
    const sha512Iterations = document.getElementById("sha512Iterations");
    const sha512IterationsVal = document.getElementById("sha512IterationsVal");
    
    const bcryptRounds = document.getElementById("bcryptRounds");
    const bcryptRoundsVal = document.getElementById("bcryptRoundsVal");
    
    const scryptN = document.getElementById("scryptN");
    const scryptNVal = document.getElementById("scryptNVal");
    const scryptR = document.getElementById("scryptR");
    const scryptP = document.getElementById("scryptP");
    
    const argon2Time = document.getElementById("argon2Time");
    const argon2TimeVal = document.getElementById("argon2TimeVal");
    const argon2Memory = document.getElementById("argon2Memory");
    const argon2MemoryVal = document.getElementById("argon2MemoryVal");
    const argon2Parallelism = document.getElementById("argon2Parallelism");
    const argon2ParallelismVal = document.getElementById("argon2ParallelismVal");

    // Action and display
    const runBenchmarkBtn = document.getElementById("runBenchmarkBtn");
    const benchmarkDuration = document.getElementById("benchmarkDuration");
    const attackCostBadge = document.getElementById("attackCostBadge");
    const benchmarkHashOutput = document.getElementById("benchmarkHashOutput");

    // Slider syncing events
    sha256Iterations.addEventListener("input", () => {
        sha256IterationsVal.innerText = parseInt(sha256Iterations.value).toLocaleString();
    });
    sha512Iterations.addEventListener("input", () => {
        sha512IterationsVal.innerText = parseInt(sha512Iterations.value).toLocaleString();
    });
    bcryptRounds.addEventListener("input", () => {
        bcryptRoundsVal.innerText = bcryptRounds.value;
    });
    scryptN.addEventListener("input", () => {
        scryptNVal.innerText = scryptN.value;
    });
    argon2Time.addEventListener("input", () => {
        argon2TimeVal.innerText = argon2Time.value;
    });
    argon2Memory.addEventListener("input", () => {
        argon2MemoryVal.innerText = parseInt(argon2Memory.value).toLocaleString();
    });
    argon2Parallelism.addEventListener("input", () => {
        argon2ParallelismVal.innerText = argon2Parallelism.value;
    });

    // Toggle dynamic parameters card layout
    hashAlgorithm.addEventListener("change", () => {
        const selected = hashAlgorithm.value;
        
        // Hide all
        document.querySelectorAll(".algo-setting-section").forEach(sec => sec.classList.remove("active"));
        
        // Show active
        if (selected === "sha256") settingsSha256.classList.add("active");
        else if (selected === "sha512") settingsSha512.classList.add("active");
        else if (selected === "bcrypt") settingsBcrypt.classList.add("active");
        else if (selected === "scrypt") settingsScrypt.classList.add("active");
        else if (selected === "argon2") settingsArgon2.classList.add("active");
    });

    // Timing comparison chart reference
    let benchmarkLatencyChart = null;

    // Track latency history to fill comparison chart
    const benchmarkHistory = {
        labels: ["SHA-256", "SHA-512", "Bcrypt", "Scrypt", "Argon2id"],
        latencies: [0.0, 0.0, 0.0, 0.0, 0.0]
    };

    const updateLatencyChart = () => {
        const ctx = document.getElementById("benchmarkLatencyChart").getContext("2d");
        
        if (benchmarkLatencyChart) {
            benchmarkLatencyChart.data.datasets[0].data = benchmarkHistory.latencies;
            benchmarkLatencyChart.update();
            return;
        }

        benchmarkLatencyChart = new Chart(ctx, {
            type: "bar",
            data: {
                labels: benchmarkHistory.labels,
                datasets: [{
                    label: "Execution Latency (ms)",
                    data: benchmarkHistory.latencies,
                    backgroundColor: [
                        "rgba(239, 68, 68, 0.25)",  // SHA256 (Weak)
                        "rgba(239, 68, 68, 0.25)",  // SHA512 (Weak)
                        "rgba(245, 158, 11, 0.25)",  // Bcrypt (Amber)
                        "rgba(0, 242, 254, 0.25)",   // Scrypt (Cyan)
                        "rgba(16, 185, 129, 0.25)"   // Argon2 (Emerald)
                    ],
                    borderColor: [
                        "var(--crimson-danger)",
                        "var(--crimson-danger)",
                        "var(--amber-warning)",
                        "var(--cyan-primary)",
                        "var(--emerald-secure)"
                    ],
                    borderWidth: 1.5
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    x: {
                        ticks: { color: "#94a3b8", font: { size: 10, family: "Plus Jakarta Sans" } },
                        grid: { color: "rgba(255,255,255,0.02)" }
                    },
                    y: {
                        type: "logarithmic", // Using log scale because KDF and hashes differ by 10000x!
                        ticks: { color: "#94a3b8", font: { size: 9 } },
                        grid: { color: "rgba(255,255,255,0.02)" }
                    }
                }
            }
        });
    };

    const runBenchmark = async () => {
        const password = hashInput.value;
        const algo = hashAlgorithm.value;
        
        let payload = { password, algorithm: algo };
        
        // Pack algorithm parameters
        if (algo === "sha256") {
            payload.iterations = sha256Iterations.value;
        } else if (algo === "sha512") {
            payload.iterations = sha512Iterations.value;
        } else if (algo === "bcrypt") {
            payload.rounds = bcryptRounds.value;
        } else if (algo === "scrypt") {
            payload.n = scryptN.value;
            payload.r = scryptR.value;
            payload.p = scryptP.value;
        } else if (algo === "argon2") {
            payload.time_cost = argon2Time.value;
            payload.memory_cost = argon2Memory.value;
            payload.parallelism = argon2Parallelism.value;
        }

        runBenchmarkBtn.disabled = true;
        runBenchmarkBtn.innerHTML = `<i class="fa-solid fa-arrows-spin fa-spin"></i> Hashing...`;

        try {
            const response = await fetch("/api/hash-benchmark", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });

            if (!response.ok) throw new Error("Benchmark failed");
            const data = await response.json();
            
            const hash = data.hash;
            const duration = data.duration_ms;
            
            benchmarkHashOutput.innerText = hash;
            benchmarkDuration.innerText = `${duration.toFixed(3)} ms`;
            
            updateBenchmarkHistory(algo, duration);
            updateCostBadge(duration);

        } catch (err) {
            console.error("Benchmark failed:", err);
            benchmarkHashOutput.innerText = "Cryptographic execution failed. Check inputs.";
        } finally {
            runBenchmarkBtn.disabled = false;
            runBenchmarkBtn.innerText = "Generate Hash & Benchmark";
        }
    };

    const updateBenchmarkHistory = (algo, duration) => {
        const indexMap = {
            "sha256": 0,
            "sha512": 1,
            "bcrypt": 2,
            "scrypt": 3,
            "argon2": 4
        };
        const index = indexMap[algo];
        benchmarkHistory.latencies[index] = duration;
        updateLatencyChart();
    };

    const updateCostBadge = (duration) => {
        if (duration > 150) {
            attackCostBadge.innerText = "Extremely High (Strongest)";
            attackCostBadge.className = "badge badge-emerald";
        } else if (duration > 50) {
            attackCostBadge.innerText = "High Cost (Hardened)";
            attackCostBadge.className = "badge badge-cyan";
        } else if (duration > 2) {
            attackCostBadge.innerText = "Moderate Cost";
            attackCostBadge.className = "badge badge-amber";
        } else {
            attackCostBadge.innerText = "Negligible (Insecure for PWs)";
            attackCostBadge.className = "badge badge-crimson";
        }
    };

    runBenchmarkBtn.addEventListener("click", runBenchmark);
    
    // Draw empty latency chart
    updateLatencyChart();
}
