p=0;
//board reset
function clearBoard(){
  for (var i = 0; i < boxes.length; i++) {
    boxes[i].textContent = "";
    p=0;
  }
}

//actual game
function mark(){
  if (this.textContent == "") {
    if (p%2 != 0) {
      this.textContent="x"
    }else {
      this.textContent="o"
    }
  }else {
    alert("celda ocupada");
    p--
  }
  p++
  if (p>=9) {
    alert("Empate, o alguien ganó y llenaste el resto de las casillas")
  }
}
//definition of variables
var reset = document.querySelector("#reset");
var boxes = document.querySelectorAll("td");

if (reset) {
  reset.addEventListener('click', clearBoard);  
}


for (var i = 0; i < boxes.length; i++) {
  boxes[i].addEventListener('click', mark)
}