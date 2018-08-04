for i in {1..24}
  do
	cat Data/$1.phon | python Data/dataprep/makeBootstrap.py $2 > Data/$1_${i}.phon
done
