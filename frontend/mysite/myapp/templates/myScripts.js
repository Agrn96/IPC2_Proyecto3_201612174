function displayDate() {
    document.getElementById("text_entrada").innerHTML = "test";
}

document.getElementById("myfile").addEventListener('change', function () {
    var fr = new FileReader();
    fr.onload = function () {
        document.getElementById("text_entrada").textContent = this.result;
    }
    fr.readAsText(this.files[0]);
})

document.getElementById("fecha").addEventListener('change', function () {
    var date = document.getElementById("fecha").value;
    document.getElementById("text_salida").innerHTML = date;
})