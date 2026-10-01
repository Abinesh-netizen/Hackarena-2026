async function checkBackend() {
    const response = await fetch("http://127.0.0.1:5000/");
    const data = await response.text();

    document.getElementById("result").textContent = data;
}