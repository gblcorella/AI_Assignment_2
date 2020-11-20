// Main Logic with use of a Worker. Both needed to run program. 
// Part 6 of the assignment but created in javascript


var worker;
var solveButton;
var output;

function mainInit()
{
    solveButton = document.getElementById("solveButton");
    output = document.getElementById("output");
    displayResult(4, [1, 3, 0, 2]);
    worker = new Worker("worker.js");
    worker.onmessage = function(event){
	if (event.data.done)
	    disableAll(false);
	displayResult(event.data.size, event.data.moves);
    }
}

function disableAll(disable){
    solveButton.disabled = disable;
    const radioButtons = document.querySelectorAll('input[name="speed"]');
    for (var i = 0; i < radioButtons.length; i++)
	radioButtons[i].disabled = disable;
}
function liveGridCell(blackBackground, inside){
    return gridCell(blackBackground?"blackBackground":"whiteBackground", inside);
}
function emptyGridCell(blackBackground){
    return gridCell(blackBackground?"blackBlank":"whiteBlank", "&nbsp;");
}
function gridCell(className, inside){
    var result = '<SPAN CLASS="';
    result += className;
    result += '">&nbsp;';
    result += inside;
    result += "&nbsp;</SPAN>";
    return result;
}

function onClick(){
    disableAll(true);
    const size = parseInt(document.getElementById("n").value, 10);
    const periodMs =
	  parseInt(document.querySelector('input[name="speed"]:checked').value,
		   10);
    worker.postMessage({size: size, periodMs: periodMs});
}

function displayResult(size, result){
    var asHtml = "";
    if (!result)
	asHtml = '<FONT COLOR="red">No Solution</FONT>';
    else {
	for (var row = 0; row < result.length; row++){
	    const queenColumn = result[row];
	    asHtml += "<DIV>";
	    for (var column = 0; column < size; column++)
	    {
		const blackBackground = ((row + column) % 2) == 0;
		const text = (column == queenColumn)?"<B>Q</B>":"&nbsp;";
		const cell = liveGridCell(blackBackground, text);
		asHtml += cell;
	    }
	    asHtml += "</DIV>";			
	}
	for (var row = result.length; row < size; row++){
	    asHtml += "<DIV>";
            for (var column = 0; column < size; column++){
                const blackBackground = ((row + column) % 2) == 0;
                const cell = emptyGridCell(blackBackground);
                asHtml += cell;
            }
            asHtml += "</DIV>";
        }
    }
    output.innerHTML = asHtml;
}
