async function analyzePage() {

    const url = document.getElementById("url").value.trim();
    const resultDiv = document.getElementById("result");

    if (!url) {
        resultDiv.innerHTML = "<p style='color:red;'>Please enter a website URL.</p>";
        return;
    }

    resultDiv.innerHTML = "<p><strong>Analyzing website...</strong></p>";

    try {

        const response = await fetch(
            `https://pagepulse-5.onrender.com/analyze?url=${encodeURIComponent(url)}`
        );

        if (!response.ok) {
            throw new Error(`Server Error: ${response.status}`);
        }

        const data = await response.json();

        if (data.error) {
            resultDiv.innerHTML = `
                <p style="color:red;">
                    <strong>Error:</strong> ${data.error}
                </p>
            `;
            return;
        }

        resultDiv.innerHTML = `
            <h2>Analysis Result</h2>

            <p><strong>Status Code:</strong> ${data.status_code}</p>

            <p><strong>Response Time:</strong>
            ${data.response_time_ms} ms</p>

            <p><strong>Title:</strong>
            ${data.title}</p>

            <p><strong>Meta Description:</strong>
            ${data.meta_description}</p>

            <p><strong>H1 Tags:</strong>
            ${data.h1_count}</p>

            <p><strong>Images Missing Alt Text:</strong>
            ${data.missing_alt}</p>

            <p><strong>Word Count:</strong>
            ${data.word_count}</p>
        `;

    } catch (error) {

        console.error(error);

        resultDiv.innerHTML = `
            <p style="color:red;">
                ❌ Could not connect to backend.<br><br>
                ${error.message}
            </p>
        `;
    }
}