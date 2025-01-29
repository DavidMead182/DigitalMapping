document.getElementById("imageUpload").addEventListener("change", (event) => {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            const img = document.getElementById("imagePreview");
            img.src = e.target.result;
            img.style.display = "block";
        };
        reader.readAsDataURL(file);
    }
});

const socket = io("http://localhost:3000");

socket.on("serialData", (data) => {
    document.getElementById("data").innerText = `Received: ${data}`;
});
