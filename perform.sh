exePythonName=./ponyFetcherList.py

target=PewDiePie
mkdir -p $target
python $exePythonName "http://hdx3.blogspot.com/search/label/PewDiePie?max-results=200" $target 0
if [ -x /usr/syno/bin/synoindex ]; then 
   /usr/syno/bin/synoindex -R $PWD/$target
fi
chown admin -R $target
chgrp users -R $target

target=BraveWarrior
mkdir -p $target
python $exePythonName "http://hdx3.blogspot.com/search/label/Bravest%20Warriors?max-results=200" $target 0
if [ -x /usr/syno/bin/synoindex ]; then 
   /usr/syno/bin/synoindex -R $PWD/$target
fi
chown admin -R $target
chgrp users -R $target

target=RegularShow
mkdir -p RegularShow
python $exePythonName "http://hdx3.blogspot.com/search/label/Regular%20Show?updated-max=2011-07-22T03:04:00-07:00&max-results=200&start=98&by-date=false" $target 0 
if [ -x /usr/syno/bin/synoindex ]; then 
   /usr/syno/bin/synoindex -R $PWD/$target
fi
chown admin -R $target
chgrp users -R $target

target=AdventureTime
mkdir -p AdventureTime
python $exePythonName "http://hdx3.blogspot.com/search/label/Adventure%20Time?updated-max=2011-09-05T03:41:00-07:00&max-results=200&start=104&by-date=false" AdventureTime 0
if [ -x /usr/syno/bin/synoindex ]; then 
   /usr/syno/bin/synoindex -R $PWD/AdventureTime 
fi
chown admin -R $target
chown users -R $target

target=MyLittlePony
mkdir -p MyLittlePony
python $exePythonName "http://hdx3.blogspot.com/search/label/My%20Little%20Pony?max-results=200" MyLittlePony 0
if [ -x /usr/syno/bin/synoindex ]; then 
   /usr/syno/bin/synoindex -R $PWD/MyLittlePony 
fi
chown admin -R $target
chgrp users -R $target

target=RickAndMorty
mkdir -p RickAndMorty
python $exePythonName "http://hdx3.blogspot.com/search/label/Rick%20and%20Morty?max-results=200" RickAndMorty 0
if [ -x /usr/syno/bin/synoindex ]; then 
   /usr/syno/bin/synoindex -R $PWD/RickAndMorty 
fi
chown admin -R $target
chgrp users -R $target

target=DanVs
mkdir -p DanVs
python $exePythonName "http://hdx3.blogspot.com/search/label/Dan%20Vs.?max-results=200" DanVs 0
if [ -x /usr/syno/bin/synoindex ]; then 
   /usr/syno/bin/synoindex -R $PWD/DanVs 
fi
chown admin -R $target
chgrp users -R $target

target=UglyAmericans
mkdir -p UglyAmericans
python $exePythonName "http://hdx3.blogspot.com/search/label/Ugly%20Americans?max-results=200" UglyAmericans 0
if [ -x /usr/syno/bin/synoindex ]; then 
   /usr/syno/bin/synoindex -R $PWD/UglyAmericans 
fi
chown admin -R $target
chgrp users -R $target

target=Metalocalypse
mkdir -p Metalocalypse
python $exePythonName "http://hdx3.blogspot.com/search/label/Metalocalypse?max-results=200" Metalocalypse 0
if [ -x /usr/syno/bin/synoindex ]; then 
   /usr/syno/bin/synoindex -R $PWD/Metalocalypse 
fi
chown admin -R $target
chgrp users -R $target

target=AVGN
mkdir -p AVGN
python $exePythonName "http://hornydragon.blogspot.com/search/label/AVGN?max-results=200" AVGN 0
if [ -x /usr/syno/bin/synoindex ]; then 
   /usr/syno/bin/synoindex -R $PWD/AVGN 
fi
chown admin -R $target
chgrp users -R $target

target=SuperJail
mkdir -p SuperJail
python $exePythonName "http://hdx3.blogspot.com/search/label/Superjail?max-results=200" SuperJail 0
if [ -x /usr/syno/bin/synoindex ]; then 
   /usr/syno/bin/synoindex -R $PWD/Superjail 
fi
chown admin -R $target
chgrp users -R $target

target=Mr.Pickles
mkdir -p Mr.Pickles
python $exePythonName "http://hdx3.blogspot.com/search/label/Mr.%20Pickles?max-results=200" Mr.Pickles 0
if [ -x /usr/syno/bin/synoindex ]; then 
   /usr/syno/bin/synoindex -R $PWD/Mr.Pickles 
fi
chown admin -R $target
chgrp users -R $target


