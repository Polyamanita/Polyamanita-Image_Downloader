#

dir="tmp"

if [ ! -d "$dir" ]
then
	mkdir $dir
fi

cp -r images/*/*/*.jpg tmp/
