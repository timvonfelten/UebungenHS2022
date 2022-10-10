function party(){
    var random = Math.floor(Math.random()*16777215).toString(16);
    var farbe = "#" + random;
    var a = document.querySelector("#eingabe");
    var i = document.querySelector("#ausgabe");
    i.innerHTML = a.value;
    if (a.value.includes("Bier") == true){
        i.innerHTML = a.value + "🍻";
    };
    ausgabe.style["font-size"] = "200px";
    ausgabe.style["color"] = farbe;
}