
async function analyzePage() {
    const url = document.getElementById("url").value;

    if (!url) {
        alert("Please enter a URL.");
        return;
    }

    try {
        const response = await fetch(
            `http://127.0.0.1:8000/analyze?url=${encodeURIComponent(url)}`
        );

        const data = await response.json();

        if (data.error) {
            document.getElementById("result").innerHTML = `
                <p style="color:red;"><strong>Error:</strong> ${data.error}</p>
            `;
            return;
        }

        document.getElementById("result").innerHTML = `
            <h2>Analysis Report</h2>
            <p><strong>HTTP Status:</strong> ${data.status_code}</p>
            <p><strong>Response Time:</strong> ${data.response_time_ms} ms</p>
            <p><strong>Title:</strong> ${data.title}</p>
            <p><strong>Meta Description:</strong> ${data.meta_description}</p>
            <p><strong>H1 Count:</strong> ${data.h1_count}</p>
            <p><strong>Images Missing Alt:</strong> ${data.missing_alt}</p>
            <p><strong>Word Count:</strong> ${data.word_count}</p>
        `;
    } catch (error) {
        document.getElementById("result").innerHTML = `
            <p style="color:red;"><strong>Error:</strong> Could not connect to the backend.</p>
        `;
    }
}