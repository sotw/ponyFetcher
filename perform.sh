exePythonName=./ponyFetcherList.py

function houseKeeping
{
    if [ -x /usr/syno/bin/synoindex ]; then 
        /usr/syno/bin/synoindex -R $PWD/$1
    fi
    chown admin -R $1
    chgrp users -R $1
}


target=PewDiePie
mkdir -p $target
python $exePythonName "http://hdx3.blogspot.com/search/label/PewDiePie?max-results=200" $target 0

target=BraveWarrior
mkdir -p $target
python $exePythonName "http://hdx3.blogspot.com/search/label/Bravest%20Warriors?max-results=200" $target 1

target=RegularShow
mkdir -p RegularShow
python $exePythonName "http://hdx3.blogspot.com/search/label/Regular%20Show?updated-max=2011-07-22T03:04:00-07:00&max-results=200&start=98&by-date=false" $target 0 

target=AdventureTime
mkdir -p AdventureTime
python $exePythonName "http://hdx3.blogspot.com/search/label/Adventure%20Time?updated-max=2011-09-05T03:41:00-07:00&max-results=200&start=104&by-date=false" $target 0

target=MyLittlePony
mkdir -p MyLittlePony
python $exePythonName "http://hdx3.blogspot.com/search/label/My%20Little%20Pony?max-results=200" $target 0

target=RickAndMorty
mkdir -p RickAndMorty
python $exePythonName "http://hdx3.blogspot.com/search/label/Rick%20and%20Morty?max-results=200" $target> 0

target=DanVs
mkdir -p DanVs
python $exePythonName "http://hdx3.blogspot.com/search/label/Dan%20Vs.?max-results=200" $target 0

target=UglyAmericans
mkdir -p UglyAmericans
python $exePythonName "http://hdx3.blogspot.com/search/label/Ugly%20Americans?max-results=200" $target 0

target=Metalocalypse
mkdir -p Metalocalypse
python $exePythonName "http://hdx3.blogspot.com/search/label/Metalocalypse?max-results=200" $target 0

target=AVGN
mkdir -p AVGN
python $exePythonName "http://hornydragon.blogspot.com/search/label/AVGN?max-results=200" $target 0

target=SuperJail
mkdir -p SuperJail
python $exePythonName "http://hdx3.blogspot.com/search/label/Superjail?max-results=200" $target 0

target=Mr.Pickles
mkdir -p Mr.Pickles
python $exePythonName "http://hdx3.blogspot.com/search/label/Mr.%20Pickles?max-results=200" $target 0

