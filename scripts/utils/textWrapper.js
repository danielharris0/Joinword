class TextWrapper {
    static wrap(textSVGAttributes, text, maxWidth) {
        let words = text.split(' ');
        let i = 0;
        let lines = [];
        let currentWord = "";
    
        let testEl = AddElementToSVG('text', textSVGAttributes);
    
        while (i < words.length) {    
        if (currentWord.length==0) {
            currentWord = words[i];
            testEl.innerHTML = words[i] + ((i+1 < words.length) ? (' ' + words[i+1]) : '');
            i++;
        }
        else {
            if (testEl.getBBox().width > maxWidth) {
                testEl.innerHTML = currentWord;
                lines[lines.length] = {"word":currentWord, "BBox":testEl.getBBox()};
                currentWord = '';
            }
            else {
                currentWord = testEl.innerHTML;
                if (i+1 < words.length) testEl.innerHTML += ' ' + words[i+1];
                i++;
            }
        }
    
        }
        lines[lines.length] = {"word":testEl.innerHTML, "BBox":testEl.getBBox()};
        testEl.remove();    
        return lines;
    }
}