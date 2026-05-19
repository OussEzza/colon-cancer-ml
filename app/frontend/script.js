const API_BASE_URL =
    "http://127.0.0.1:8000";

const geneInputsContainer =
    document.getElementById("gene-inputs");

const form =
    document.getElementById("prediction-form");

const resultDiv =
    document.getElementById("result");

const predictionBadge =
    document.getElementById("prediction-badge");

const confidenceText =
    document.getElementById("confidence-text");

const loadingDiv =
    document.getElementById("loading");

const apiStatus =
    document.getElementById("api-status");

const demoBtn =
    document.getElementById("demo-btn");

const resetBtn =
    document.getElementById("reset-btn");

let selectedGenes = [];

// ======================================
// API Health Check
// ======================================

async function checkHealth() {

    try {

        const response =
            await fetch(
                `${API_BASE_URL}/health`
            );

        if (response.ok) {

            apiStatus.innerHTML =
                `<span class="online">
                    API Online
                </span>`;

        } else {

            apiStatus.innerHTML =
                `<span class="offline">
                    API Offline
                </span>`;
        }

    } catch {

        apiStatus.innerHTML =
            `<span class="offline">
                API Offline
            </span>`;
    }
}

// ======================================
// Load genes
// ======================================

async function loadGenes() {

    try {

        const response =
            await fetch(
                `${API_BASE_URL}/genes`
            );

        const data =
            await response.json();

        selectedGenes =
            data.selected_genes;

        generateInputs(selectedGenes);

    } catch (error) {

        console.error(error);
    }
}

// ======================================
// Generate inputs
// ======================================

function generateInputs(genes) {

    geneInputsContainer.innerHTML = "";

    genes.forEach(gene => {

        const div =
            document.createElement("div");

        div.className =
            "input-group";

        div.innerHTML = `
            <label>${gene}</label>

            <input
                type="number"
                step="any"
                id="${gene}"
                placeholder="Enter value"
                required
            >
        `;

        geneInputsContainer.appendChild(div);
    });
}

// ======================================
// Demo Data
// ======================================

demoBtn.addEventListener(
    "click",
    () => {

        selectedGenes.forEach(gene => {

            const randomValue =
                (Math.random() * 4 - 2)
                .toFixed(3);

            document.getElementById(
                gene
            ).value = randomValue;
        });
    }
);

// ======================================
// Reset Form
// ======================================

resetBtn.addEventListener(
    "click",
    () => {

        form.reset();

        resultDiv.classList.add(
            "hidden"
        );
    }
);

// ======================================
// Prediction
// ======================================

form.addEventListener(
    "submit",
    async (e) => {

        e.preventDefault();

        loadingDiv.classList.remove(
            "hidden"
        );

        resultDiv.classList.add(
            "hidden"
        );

        const payload = {};

        selectedGenes.forEach(gene => {

            payload[gene] =
                parseFloat(
                    document.getElementById(
                        gene
                    ).value
                );
        });

        try {

            const response =
                await fetch(
                    `${API_BASE_URL}/predict`,
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(
                                payload
                            )
                    }
                );

            const result =
                await response.json();

            loadingDiv.classList.add(
                "hidden"
            );

            resultDiv.classList.remove(
                "hidden"
            );

            predictionBadge.className =
                "badge";

            if (
                result.prediction ===
                "Normal"
            ) {

                predictionBadge.classList.add(
                    "normal"
                );

            } else {

                predictionBadge.classList.add(
                    "abnormal"
                );
            }

            predictionBadge.innerText =
                result.prediction;

            confidenceText.innerText =
                `Confidence: ${
                    (
                        result.confidence
                        * 100
                    ).toFixed(2)
                }%`;

        } catch (error) {

            loadingDiv.classList.add(
                "hidden"
            );

            alert(
                "Prediction failed."
            );

            console.error(error);
        }
    }
);

// ======================================
// Initialize
// ======================================

checkHealth();

loadGenes();