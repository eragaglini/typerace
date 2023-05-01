var createChessBoard = function(x, y) {

    var boardHeight = x || 8;
    var boardWidth = y || 8;
  
    var domFragment = document.createDocumentFragment();
    var chess = document.querySelector('.chess');
  
    for ( var i=0; i<boardHeight; i++) {
  
      for(var j=0; j<boardWidth; j++) {
  
        var cell = document.createElement('div');
  
        if(i%2 === 0 && j%2 === 0 || i%2 !== 0 && j%2 !== 0){
          cell.className = 'odd';
        } else {
          cell.className = 'even';
        }
        domFragment.appendChild(cell);
      }
  
    }
  
    chess.appendChild(domFragment);
}
  
document.addEventListener("DOMContentLoaded", function() {
    console.log( "ready!" );
    createChessBoard();
});