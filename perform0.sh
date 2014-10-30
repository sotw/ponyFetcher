synoindexPath='/usr/syno/bin/synoindex'
pythonPath='python'

function synoindex_update
{
	if [ -x $synoindexPath ]; then
		$synoindexPath -R $PWD/$1
	fi
}

function travelNode
{
	mkdir -p $1
	if [ -x $pythonPath ]; then
		$pythonPath ponyFetcherList.py $2 $1 0
	fi
}

mkdir -p BraveWarrior
python ponyFetcherList.py "http://hdx3.blogspot.com/search/label/Bravest%20Warriors?max-results=200" BraveWarrior 0
if [ -x /usr/syno/bin/synoindex ]; then 
   /usr/syno/bin/synoindex -R $PWD/BraveWarrior 
fi
mkdir -p RegularShow
python ponyFetcherList.py "http://hdx3.blogspot.com/search/label/Regular%20Show?updated-max=2011-07-22T03:04:00-07:00&max-results=200&start=98&by-date=false" RegularShow 0 
if [ -x /usr/syno/bin/synoindex ]; then 
   /usr/syno/bin/synoindex -R $PWD/RegularShow 
fi
mkdir -p AdventureTime
python ponyFetcherList.py "http://hdx3.blogspot.com/search/label/Adventure%20Time?updated-max=2011-09-05T03:41:00-07:00&max-results=200&start=104&by-date=false" AdventureTime 0
if [ -x /usr/syno/bin/synoindex ]; then 
   /usr/syno/bin/synoindex -R $PWD/AdventureTime 
fi
mkdir -p MyLittlePony
python ponyFetcherList.py "http://hdx3.blogspot.com/search/label/My%20Little%20Pony?max-results=200" MyLittlePony 0
if [ -x /usr/syno/bin/synoindex ]; then 
   /usr/syno/bin/synoindex -R $PWD/MyLittlePony 
fi
mkdir -p RickAndMorty
python ponyFetcherList.py "http://hdx3.blogspot.com/search/label/Rick%20and%20Morty?max-results=200" RickAndMorty 0
if [ -x /usr/syno/bin/synoindex ]; then 
   /usr/syno/bin/synoindex -R $PWD/RickAndMorty 
fi
mkdir -p DanVs
python ponyFetcherList.py "http://hdx3.blogspot.com/search/label/Dan%20Vs.?max-results=200" DanVs 0
if [ -x /usr/syno/bin/synoindex ]; then 
   /usr/syno/bin/synoindex -R $PWD/DanVs 
fi
mkdir -p UglyAmericans
python ponyFetcherList.py "http://hdx3.blogspot.com/search/label/Ugly%20Americans?max-results=200" UglyAmericans 0
if [ -x /usr/syno/bin/synoindex ]; then 
   /usr/syno/bin/synoindex -R $PWD/UglyAmericans 
fi
mkdir -p Metalocalypse
python ponyFetcherList.py "http://hdx3.blogspot.com/search/label/Metalocalypse?max-results=200" Metalocalypse 0
if [ -x /usr/syno/bin/synoindex ]; then 
   /usr/syno/bin/synoindex -R $PWD/Metalocalypse 
fi
mkdir -p AVGN
python ponyFetcherList.py "http://hornydragon.blogspot.com/search/label/AVGN?max-results=200" AVGN 0
if [ -x /usr/syno/bin/synoindex ]; then 
   /usr/syno/bin/synoindex -R $PWD/AVGN 
fi
mkdir -p SuperJail
python ponyFetcherList.py "http://hdx3.blogspot.com/search/label/Superjail?max-results=200" SuperJail 0
if [ -x /usr/syno/bin/synoindex ]; then 
   /usr/syno/bin/synoindex -R $PWD/Superjail 
fi
