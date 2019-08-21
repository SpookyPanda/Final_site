//variable to check what turn it is
p=0;

//definition of variables to interact with the user input
var reset = document.querySelector("#reset");
var boxes = document.querySelectorAll("td");

//board reset
function clearBoard(){
  for (var i = 0; i < boxes.length; i++) {
    boxes[i].textContent = "";
    p=0;
  }
}


//wincheck
//all of this could me mashed in to one if but no, this is already messy  to read.
function winCheck(q){
  for (i=0; i < 3; i++){
    //check for vertical win, then horizontal, and finally diagonal
    //i know there is an extra check in the horizontal but feels like cheating doing otherwise
    if (boxes[i].textContent==q && boxes[i+3].textContent==q && boxes[i+6].textContent==q){
      return true;
    }else if (boxes[i*3].textContent==q && boxes[i*3+1].textContent==q && boxes[i*3+2].textContent==q){
      return true;
    }else if(boxes[i].textContent==q && boxes[4].textContent==q && boxes[i+(8-(2*i))].textContent==q){
      return true;
    }
  }
  return false;
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
  if (winCheck(this.textContent)){
    alert(this.textContent+" gana!")
    clearBoard()
  }else if (p>=9) {
    alert("Empate, o alguien ganó y llenaste el resto de las casillas")
  }
}


//the 'reset' box got clicked
if (reset) {
  reset.addEventListener('click', clearBoard);  
}

//make the boxes 'clickable'
for (var i = 0; i < boxes.length; i++) {
  boxes[i].addEventListener('click', mark)
}