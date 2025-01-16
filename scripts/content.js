const PUZZLES = [
  new Puzzle(
    ["Throws balls","Tones","Biker jacket"],
    ["pitches","gets ripped","hosts galas"],
    [[1,3], [1,2], [2]]
  ),
  new Puzzle(
    ["open ...","... street","... in the hole","Berlin ..."],
    ["toad","wall","fire","sesame"],
    [[3,4], [2,4], [1,3],[2]]
  ),
  new Puzzle(
    ["gymnast",'instrument','furniture','glass'],
    ["flute","piano","chest","tumbler"],
    [[4], [1,2], [2,3],[1,4]]
  ),
  new Puzzle( //+++
    ['solid','music genre','verb','liquid','transparent','tree part','sodium'],
    ['metal','rock','wood','sap','water','vodka','oxygen'],
    [[1,2,3],[1,2],[2,4,5],[4,5,6],[5,6,7],[3,4],[1]]
  ),
  new Puzzle(  //+++
    ['divides by 2','divides by 3','divides by 5','factor of 10','factor of 20','factor of 35'],
    ['one','two','three','four','five','six'],
    [[2,4,6],[3,6],[5],[1,2,5],[1,2,4,5],[1,5]]
  ),
  new Puzzle( 
    ['the big','one track','shoe','pop','brain'],
    ['bang','mind','giants','song','trainer'],
    [[1,3],[2,4],[5],[1,4],[2,5]]
  ),

  new Puzzle(
    ["alphabetic homophone",'might begin a question','wherefore','form of the verb \'is\''],
    ["see","be","are","why"],
    [[1,2,3,4],[3,4],[4],[2,3]]
  ),

  new Puzzle( //fri
    ["titular carnivores", "big bucks", "stags", "you want to be in...", "best-sellers", "holy texts"],
    ["[redacted], in a way", "large male deer", "cats of the west end", "the money", "the good books", "wolves of wall street"],
    [[3,6],[2,4],[2],[4,5],[5,6],[1,5]]
  ),

  new Puzzle( //sat
    ['out of', 'the sun', 'pop', 'earth', 'baking', 'before ?'],
    ['this world', 'too hot', 'the question', 'celestial object', 'soda', 'depleted'],
    [[1,6],[2,4],[3,5],[1,4],[2,5],[3]]
  ),

  new Puzzle( //sun
    ['sometimes comes in a cup', 'sometimes comes in a cone', 'high spirits', 'cracker content', 'playful verb', 'Kennel Club grouping'],
    ['ice cream', 'joke', 'good cheer', 'party hat', 'toy', 'top shelf liquor'],
    [[1,3],[1,4],[3,6],[2,4,5],[2,5],[5]]
  ),

  new Puzzle( //mon
    ['none of moon visible','1/4 of moon visible','half of moon visible','3/4 of moon visible','empty','working','Netflix branding','low','what a newspaper is, punnily','a suit','garden tool(s)'],
    ['gibbous','sickle','new','','N','on','moo','sad: feeling...', 'red','businessman','spades'],
    [[3,4],[2,5],[6],[1,7],[4,8],[6,10],[5,9],[7,8],[3,9],[10,11],[2,11]]
  ),

  new Puzzle( //24th
    ['guise of Zeus','12 Days of Christmas gift','bird','warm blooded','vertebrate','animal','living','verb'],
    ['oil','plant','fly','snake','bear','duck','dove','swan'],
    [[8],[7,8],[6,7,8],[5,6,7,8],[4,5,6,7,8],[3,4,5,6,7,8],[2,3,4,5,6,7,8],[1,2,3,4,5,6,7,8]]
  ),

  new Puzzle( //25th
    ['reindeer','metal','bridge unit','fox','icy ball','legendary archer','roman god','might fly when having fun','time'],
    ['vixen','cupid','comet','dancer','mercury','snowball','trick','\"will tell\", you might say','time'],
    [[1,2,3,4],[5],[7],[1,7],[3,6],[2,8],[2,5],[6,9],[8,9]]
  ),
  new Puzzle( //26th
    ['peri','smart','micro','tele','psycho','para','photo','tria','penta'],
    ['ssic','gon','phone','scope','path','graph','sis','n','thlon'],
    [[4],[3],[3,4,8],[3,4,5,6],[5,7],[2,6],[6,8],[1,9],[2,9]]
  ),
  new Puzzle( //27th
    ['sweet','salty','sour','bitter','umami','spicy'],
    ['sweet chilli','lemonade','mushroom','soy sauce','dark chilli chocolate','salt and vinegar'],
    [[1,2,5],[4,6],[2,6],[5],[3,4],[1,5]]
  ),
  new Puzzle( //28th
    ['has wings','has wings and no legs','has wings and no arms','has fewer than four legs','has arms and legs','has legs'],
    ['Buckingham Palace','sofa','Taylor Swift','cat','pigeon','cherub'],
    [[1,5,6],[1],[1,5],[1,3,5,6],[2,3,6],[2,3,4,5,6]]
  ),  
  new Puzzle( //29th
    ['hazelnut','almond','cherry','chocolate','\"little bitter\" in Italy'],
    ['amaretto','frangelico','bakewell tart (often)','black forest gateau','nutella'],
    [[2,5],[1,3],[3,4],[4,5],[1]]
  ),  
  new Puzzle( //30th
    ['racquet','net','triangle','ball','bat','table'],
    ['tennis','badminton','cricket','table tennis','snooker','fishing'],
    [[1,2],[1,2,4,6],[5],[1,3,4,5],[3,4],[4,5]]
  ),  
  new Puzzle( //31st
    ['square','Adele album','spelled with an \'e\'','odd','(x+1)*(x-1) gives x*x - 1'],
    ['2025','2000','25','20','5'],
    [[1,3],[3],[1,3,4,5],[1,3,5],[1,2,3,4,5]]
  ),  
  new Puzzle( //1st
    ['named after a number','stingy with the days (<31)','named after a Roman god','springy','named after a Roman politician', 'initially a chemical symbol','ruby birthstone'],
    ['January','February','March','April','July','August','December'],
    [[7],[2,4],[3,1],[3,4],[5,6],[2,6],[5]]
  ),  
  new Puzzle(['for','inter','pro','con','mini','mon'],['ster','est','itor','mal','ference','duct'],[[2,4],[5,2],[6],[6,5],[4,1],[1,3]]),
  new Puzzle(['dashing','(nearly) a "tree [...] in the wood"','calm','apparatus to deliver fluids','bright','_ night'],['cup','all is _','silent','IV','smart','holy'],[[5],[6,4],[2,3],[4,1],[5,2],[3,6]]),
  new Puzzle(['back','con','pro','super','enter','mer','sur','inter'],['gress','ior','ing','taining','face','ground','vision','ely'],[[3,6],[1,4],[7,1],[2,7],[4,3],[8],[8,5],[5,2]]),
  new Puzzle(
    ['doctors','cooks','navigational aid','possible Wordle word','titanic','X-?','men in caps', 'found in capitals','capsized vessel, in a way'],
    ['MEN','VESSEL','GPS','FOUND','large','a spilled glass','falsifies','landmarks','peaky blinders'],
    [[3,7],[7],[3,8],[4,5],[2,5],[1],[1,9],[4,8],[2,6]]
  ),
  new Puzzle(['super','inter','under','com','back','dis','pro','con'],['crete','vision','pute','ing','standing','ference','ior','ground'],[[2,7],[7,6],[8,5],[3,4],[4,8],[1,3],[2],[6,1]]),
  new Puzzle(
    ['_ times','square','dull','tables','fade','highlights'],
    ['times _','best of','worst of','dim','boring','hairstyle'],
    [[2,3],[1,5],[4,5],[1],[4,6],[2,6]]
  ),
  new Puzzle(['trans','fore','for','mini','des','uni','anti','inter'],['mal','stry','ign','section','cription','est','que','form'],[[8,5],[3,2],[1,6],[2,1],[5,3],[7,8],[7],[6,4]]),
  new Puzzle(['white wine','undistilled','grape-based','liquid','sweet','alcoholic','edible'],['merlot','tequila','lager','chardonnay','bread',' late harvest riesling','water'],[[4,6],[3,1,4,6],[1,4,6],[7,2,3,1,4,6],[6],[2,3,1,4,6],[5,7,2,3,1,4,6]]),
  new Puzzle(['wh','u','an','si','mi'],['o','d','p','x','y'],[[5,1],[3],[2,5],[3,4],[4,2]]),
  new Puzzle(
    ['instrument','analogue','aerophone','pipe-based','brass','with valves'],
    ['trumpet','trombone','flute','harmonica','marimba','theremin'],
    [[1,2,3,4,5,6],[1,2,3,4,5],[1,2,3,4],[1,2,3],[1,2],[1]]
  ),
  new Puzzle(['res','pro','con','inc','dis'],['gress','crete','ident','rease','trict'],[[5,3],[1],[1,2],[3,4],[2,5]]),
  new Puzzle(['ja','pl','ed','tr','kn','fo','bu','lo','no','ti','ma'],['va','se','it','zz','ee','rk','er','ay','lk','ny','an'],[[1,4],[8,11],[3],[5,8],[3,5],[9,6],[4,9],[11,2],[2,1],[10,7],[6,10]]),
  new Puzzle(['proper','indu','identi','physic','chemi','possib','sele','princip'],['cal','le','ction','ly','ian','al','ty','stry'],[[7,4],[3,8],[1,7],[6,5],[8,1],[4,2],[3],[2,6]]),
  new Puzzle(['mo','mer','fi','glo','tri','yo','ca','wo'],['ung','be','sh','rst','ry','uth','ge','od'],[[8,6],[5,7],[3,4],[2,5],[2],[6,1],[7,3],[4,8]]),
  new Puzzle(['structur','reasonabl','correct','automat','princip','geograph','special','difficul'],['ion','y','e','ty','al','t','ly','ic'],[[5,3],[3,2],[1,7],[8,1],[5],[2,8],[7,4],[4,6]]),
  
  new Puzzle(['past','show','walk','present','rise','done'],['prove','a tense word','display','over','audibly a colour','hike'],[[2,4],[1,3],[6],[3,2],[6,1],[4,5]]),
  new Puzzle(['berry','vegetable','herb','adverb, outspoken','adjective, aloud','verb, heard'],['leek','chard','thyme','currant','yarrow','sloe'],[[6,4],[2,1],[3,5],[6],[4,2],[1,3]]),

  new Puzzle(['ex','cre','pa','fin','au','stu','rea','par'],['der','dio','ish','sta','dy','cel','tent','dit'],[[6,7],[8],[7,4],[1,3],[8,2],[2,5],[5,1],[3,6]]),
  new Puzzle(['accept','comple','adjust','attrac'],['able','tion','ance','ment'],[[1,3],[2,4],[4,1],[2]]),
  new Puzzle(['bu','vi','co','he','ma','ca','we','re'],['rgin','alth','rner','ndle','ader','ture','medy','sual'],[[3,4],[8,1],[7,3],[2,5],[1,6],[4,8],[2],[5,7]]),
  new Puzzle(['corre','attr','compar','innov','adjust','instru','trans'],['ative','active','ction','lation','action','ment','able'],[[3,4],[5,2],[1,7],[1],[7,6],[6,3],[4,5]]),
  new Puzzle(['wal','out','le','be','d','trac','r','visi'],['ental','side','ker','tor','ather','let','ouble','tter'],[[3,6],[6,2],[8,5],[2,8],[1,7],[4,3],[5,1],[4]]),
  new Puzzle(['pro','dis','tra','con'],['position','spective','ditional','tribution'],[[1,2],[4,1],[3],[3,4]]),
  new Puzzle(['pas','opti','regi','poss','vis','proc','deci','mon'],['sage','ess','itor','ible','onal','mal','sion','ster'],[[7,1],[5,6],[8,5],[2,4],[4,3],[2],[6,7],[3,8]]),

  new Puzzle(['absen','voi','equa','flu','chroni','publi','parti','che','sal','gol','exce'],['cle','l','tion','ce','d','sh','c','f','t','ss','id'],[[9,4],[4,5],[2,3],[6,11],[1,7],[7,6],[3,1],[8,10],[9],[5,8],[10,2]]),
];