class Puzzle {
    constructor(left, right, answer) {
        this.clues = [left, right]
        this.answer = answer;
        this.N = Math.max(left.length, right.length);
        for (let i=0; i<this.N; i++) {
            for (let j=0; j<this.answer[i].length; j++) this.answer[i][j]--;
        }
    }
  }

function SetCurrentPuzzle(puzzleID) {
    for (let line of lines) RemoveLine(line);
    puzzle = GetPuzzleByID(puzzleID);
    BuildPuzzleSVG(puzzle);
}

function GetPuzzleByID(puzzleID) {
    if (puzzleID < 50) return PUZZLES[puzzleID];
    else {
        puzzleID -= 50;
        if (puzzleID%2==0) return CONTENT_SEMANTIC[puzzleID/2];
        else return CONTENT_SPELLING[(puzzleID-1)/2];
    }
}