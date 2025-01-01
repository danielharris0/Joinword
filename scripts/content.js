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
];