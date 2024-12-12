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
    puzzle = PUZZLES[puzzleID];
    BuildPuzzleSVG(puzzle);
}