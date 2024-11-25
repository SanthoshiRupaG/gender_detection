function toggleInputFields() {
    const inputType = document.getElementById("input_type").value;
    const ipFields = document.getElementById("ip-fields");
    if (inputType === "ip_stream") {
        ipFields.style.display = "block";
    } else {
        ipFields.style.display = "none";
    }
}
