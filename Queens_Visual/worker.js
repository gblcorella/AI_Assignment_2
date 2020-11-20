console.log("Wait it's working");

var periodMs;
var nextReportTime;

onmessage = function(e) {
    console.log('Worker: Message received from main script');
    periodMs = e.data.periodMs;
    nextReportTime = new Date();
    const size = e.data.size;
    const moves = solve(size);
    postMessage({size: size, moves: moves, done: true});
}

function reportIfRequired(size, moves){
    const now = new Date();
    if (now >= nextReportTime){
	postMessage({size: size, moves: moves, done: false});
	nextReportTime = new Date(now.getTime() + periodMs);
    }
}
 
// Solve iteratively 
function solve(size, initialState = []){
    reportIfRequired(size, initialState);
    if (size == initialState.length)
	return initialState;
    var available = {};
    for (var i = 0; i < size; i++){
	available[i] = i;
    }
    for (var row = 0; row < initialState.length; row++){
	    delete available[initialState[row]];
	    const offset = initialState.length - row;
	    delete available[initialState[row] - offset];
	    delete available[initialState[row] + offset];		  
    }
    for (var columnName in available){
	    const column = available[columnName];
	    const tryThis = initialState.slice(0);
	    tryThis.push(column);
	    const result = solve(size, tryThis);
	    if (!!result)
	        return result;		  
        }
        return false;
    }
