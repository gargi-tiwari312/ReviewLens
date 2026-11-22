
// ==========================================
// REVIEWLENS - DASHBOARD JAVASCRIPT
// ==========================================

// Chart Variables
let ratingChart = null;
let sentimentChart = null;


// ==========================================
// 1. LOAD DASHBOARD DATA
// ==========================================

async function loadDashboard() {

    try {

        const response = await fetch("/api/dashboard");
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Unable to load dashboard");
        }

        // UPDATE DASHBOARD CARDS

        document.getElementById("totalReviews").textContent =
            data.total_reviews;

        document.getElementById("averageRating").textContent =
            data.average_rating + " / 5";

        document.getElementById("positiveReviews").textContent =
            data.positive_reviews;

        document.getElementById("negativeReviews").textContent =
            data.negative_reviews;


        // ==================================
        // 2. RATING DISTRIBUTION CHART
        // ==================================

        const ratingLabels = [
            "1 Star",
            "2 Stars",
            "3 Stars",
            "4 Stars",
            "5 Stars"
        ];

        const ratingValues = [1, 2, 3, 4, 5].map(
            rating => data.rating_distribution[rating] || 0
        );

        if (ratingChart) {
            ratingChart.destroy();
        }

        ratingChart = new Chart(
            document.getElementById("ratingChart"),
            {
                type: "bar",

                data: {
                    labels: ratingLabels,

                    datasets: [{
                        label: "Number of Reviews",
                        data: ratingValues,

                        backgroundColor: [
                            "#ef4444",
                            "#f97316",
                            "#eab308",
                            "#60a5fa",
                            "#22c55e"
                        ],

                        borderRadius: 8,
                        borderWidth: 0
                    }]
                },

                options: {
                    responsive: true,
                    maintainAspectRatio: false,

                    plugins: {
                        legend: {
                            display: false
                        }
                    },

                    scales: {
                        y: {
                            beginAtZero: true,

                            ticks: {
                                precision: 0
                            }
                        }
                    }
                }
            }
        );


        // ==================================
        // 3. SENTIMENT CHART
        // ==================================

        if (sentimentChart) {
            sentimentChart.destroy();
        }

        const sentimentData = data.sentiment_counts || {};

        const positiveCount = sentimentData.Positive || 0;
        const negativeCount = sentimentData.Negative || 0;
        const neutralCount = sentimentData.Neutral || 0;

        sentimentChart = new Chart(
            document.getElementById("sentimentChart"),
            {
                type: "doughnut",

                data: {
                    labels: [
                        "Positive",
                        "Negative",
                        "Neutral"
                    ],

                    datasets: [{
                        label: "Review Sentiment",

                        data: [
                            positiveCount,
                            negativeCount,
                            neutralCount
                        ],

                        backgroundColor: [
                            "#22c55e",
                            "#ef4444",
                            "#eab308"
                        ],

                        borderWidth: 2
                    }]
                },

                options: {
                    responsive: true,
                    maintainAspectRatio: false,

                    plugins: {
                        legend: {
                            position: "bottom"
                        },

                        title: {
                            display: true,
                            text: "AI/NLP Review Sentiment"
                        }
                    }
                }
            }
        );


        // ==================================
        // 4. PRODUCT-WISE ANALYSIS TABLE
        // ==================================

        const table = document.getElementById("productTable");

        table.innerHTML = "";

        data.product_summary.forEach(product => {

            const row = document.createElement("tr");

            const nameCell = document.createElement("td");
            nameCell.textContent = product.product;

            const countCell = document.createElement("td");
            countCell.textContent = product.total_reviews;

            const ratingCell = document.createElement("td");

            ratingCell.textContent =
                "⭐ " +
                Number(product.average_rating).toFixed(2);

            row.appendChild(nameCell);
            row.appendChild(countCell);
            row.appendChild(ratingCell);

            table.appendChild(row);

        });


        console.log("Dashboard loaded successfully!");

    }

    catch (error) {

        console.error("Dashboard Error:", error);

        document.getElementById("uploadMessage").textContent =
            error.message;

    }

}


// ==========================================
// 5. LOAD REVIEW INSIGHTS
// ==========================================

async function loadInsights() {

    try {

        const response = await fetch("/api/insights");

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Unable to load insights");
        }

        const insights = data.insights;


        // ==================================
        // OVERALL SUMMARY
        // ==================================

        document.getElementById("insightsSummary").textContent =
            insights.summary || "No summary available.";


        // ==================================
        // COMMON COMPLAINTS
        // ==================================

        const complaintsList =
            document.getElementById("complaintsList");

        complaintsList.innerHTML = "";

        if (
            insights.common_complaints &&
            insights.common_complaints.length > 0
        ) {

            insights.common_complaints.forEach(item => {

                const li = document.createElement("li");

                li.textContent =
                    `${item[0]} (${item[1]} mentions)`;

                complaintsList.appendChild(li);

            });

        } else {

            complaintsList.innerHTML =
                "<li>No complaints found.</li>";

        }


        // ==================================
        // APPRECIATED FEATURES
        // ==================================

        const featuresList =
            document.getElementById("featuresList");

        featuresList.innerHTML = "";

        if (
            insights.appreciated_features &&
            insights.appreciated_features.length > 0
        ) {

            insights.appreciated_features.forEach(item => {

                const li = document.createElement("li");

                li.textContent =
                    `${item[0]} (${item[1]} mentions)`;

                featuresList.appendChild(li);

            });

        } else {

            featuresList.innerHTML =
                "<li>No appreciated features found.</li>";

        }


        // ==================================
        // IMPROVEMENT SUGGESTIONS
        // ==================================

        const suggestionsList =
            document.getElementById("suggestionsList");

        suggestionsList.innerHTML = "";

        if (
            insights.improvement_suggestions &&
            insights.improvement_suggestions.length > 0
        ) {

            insights.improvement_suggestions.forEach(suggestion => {

                const li = document.createElement("li");

                li.textContent = suggestion;

                suggestionsList.appendChild(li);

            });

        } else {

            suggestionsList.innerHTML =
                "<li>No suggestions available.</li>";

        }


        console.log("Review Insights loaded successfully!");

    }

    catch (error) {

        console.error("Insights Error:", error);

        document.getElementById("insightsSummary").textContent =
            "Unable to load review insights.";

    }

}


// ==========================================
// 6. CSV FILE UPLOAD
// ==========================================

document.getElementById("uploadForm").addEventListener(
    "submit",

    async function(event) {

        event.preventDefault();

        const fileInput = document.getElementById("csvFile");
        const message = document.getElementById("uploadMessage");

        if (!fileInput.files.length) {
            message.textContent = "Please select a CSV file.";
            return;
        }

        const file = fileInput.files[0];

        if (!file.name.toLowerCase().endsWith(".csv")) {
            message.textContent = "Only CSV files are allowed.";
            return;
        }

        const formData = new FormData();

        formData.append("file", file);

        message.textContent = "Uploading and analysing reviews...";

        try {

            const response = await fetch("/analyze", {
                method: "POST",
                body: formData
            });

            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.error || "CSV upload failed");
            }

            message.textContent =
                result.message +
                " | Total Reviews: " +
                result.total_reviews;

            fileInput.value = "";

            // Refresh dashboard and insights

            await loadDashboard();

            await loadInsights();

        }

        catch(error) {

            console.error("Upload Error:", error);

            message.textContent = error.message;

        }

    }

);


// ==========================================
// 7. LOAD DATA WHEN PAGE OPENS
// ==========================================

document.addEventListener(
    "DOMContentLoaded",

    function() {

        loadDashboard();

        loadInsights();

    }

);
