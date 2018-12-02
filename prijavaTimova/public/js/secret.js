(function main() {

    const secret = JSON.parse(localStorage.getItem("secret-mode") || "false");

    function colorElement(el) {
        const backgroundColor = "#" + Math.floor(Math.random() * Math.pow(256, 3)).toString(16);
        const borderColor = "#" + Math.floor(Math.random() * Math.pow(256, 3)).toString(16);
        const color = "#" + Math.floor(Math.random() * Math.pow(256, 3)).toString(16);
        el.style.backgroundColor = backgroundColor;
        el.style.borderColor = borderColor;
        el.style.color = color;
    }

    function execute(arg) {
        if (secret) {
            colorElement(document.body);
            document.body.querySelectorAll("*").forEach(colorElement);
        }
        return arg;
    }
    setTimeout(execute, 1000);

    window.Secret = {
        execute,
    };

})();