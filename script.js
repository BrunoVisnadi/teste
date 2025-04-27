document.addEventListener("keyup", function (e) {
    if (e.key === "PrintScreen") {
        console.log('printScreen');
        fetch("/log_screenshot", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ judge_uuid: JUDGE_UUID }),
         });
        document.body.style.filter = "blur(5px)";
        return false;
    }
});



document.addEventListener("keydown", function (e) {
    if (e.key.length === 1 && e.key.match(/[a-zA-Z]/)) {
        console.log('opa2')
        document.body.style.filter = "";
        return false;
    }
});


document.addEventListener("copy", function () {
    event.preventDefault();
    const customMessage = "Não é permitido copiar e/ou distribuir o conteúdo do teste.";
    event.clipboardData.setData("text/plain", customMessage);

});
