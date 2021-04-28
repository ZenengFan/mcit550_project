#!/bin/bash

workDir="~/Documents/Programming/cis550/cis550GroupProject/data"

#cd ~/Documents/Programming/cis550/vaccination/covid-19-data/public/data/vaccinations && git clone https://github.com/nytimes/covid-19-data.git
#cd ~/Documents/Programming/cis550/covid-19-data && git clone https://github.com/nytimes/covid-19-data.git

#download us_state_vaccinations.csv from https://coronavirus-resources.esri.com/datasets/1044bb19da8d4dbfb6a96eb1b4ebf629_0/data
#us_state_population.csv downloaded from https://worldpopulationreview.com/states
#COVID-19_Social_Media_Counts_Sentiment.csv downloaded from https://coronavirus-resources.esri.com/datasets/feb6280d42de4e91b47cf37344a91eae_0/data?geometry=27.913%2C-0.672%2C-27.282%2C76.524&orderBy=FID&page=2&selectedAttribute=name&showData=true


cd ~/Documents/Programming/cis550/covid-19-data
git pull

cd ~/Documents/Programming/cis550/vaccination/covid-19-data
git fetch
git checkout -m origin/master -- public/data/vaccinations/us_state_vaccinations.csv
#git add public/data/vaccinations/us_state_vaccinations.csv
#git commit

cd $workDir
cat us_state_population.csv |cut -f2,3 -d, |sed 's/\"//g' |tail -n +2 > state_pop.csv

awk 'BEGIN{FS=","; OFS=","}{print $4, $2, $3}' us_counties_covid19cases.csv |grep -v "Unknown" |sort |uniq |grep -e "^[0-9]" |grep -f states.txt > counties.csv
#cat <(echo -e "fips,name,state") counties.csv > counties.hd.csv
#mv counties.hd.csv counties.csv

cut -f1 -d, counties.csv |sort |uniq > fips.txt



cat USA_Hospital_Beds.csv |awk 'BEGIN{FS=",";OFS=","}{if ($0~/HOSPITAL_NAME/) {print $4, "Address", $18, $15} else {print $4, $6"\|"$7"\|"$8"\|"$9"\|"$10, $18, $15}}' |sed 's/[(].*[)]//'| grep -f fips.txt |awk 'BEGIN{FS=",";OFS=","}{if ($4!=36061 && $4!=36005) {print $0}}'> hospitals.csv
#cat <(echo -e "name,address,icu_beds,fips") hospitals.csv > hospitals.hd.csv
#mv hospitals.hd.csv hospitals.csv

sed 's/^/,/' fips.txt > fips.comma.txt
cat COVID-19_Social_Media_Counts_Sentiment.csv | cut -d, -f1-9 |grep -f fips.comma.txt |grep -v "total" > sentiments.csv

cat us_state_vaccinations.csv | awk 'BEGIN{FS=",";OFS=","}{print $2, $1, $3, $8, $12}' |grep -f states.txt > vaccinations.csv
#cat <(echo -e "state,date,total_vaccinations,ppl_fully_vaccinated,daily_vaccinations") vaccinations.csv > vaccinations.hd.csv
#mv vaccinations.hd.csv vaccinations.csv

grep -v "Unknown" us_counties_covid19cases.csv| awk 'BEGIN{FS=","; OFS=","}{if ($4!="" && $1!="" && $5!=""){print $4, $1, $5}}' | grep -f fips.txt > cases.csv
#cat <(echo -e "fips,date,amount") cases.csv > cases.hd.csv
#mv cases.hd.csv cases.csv


grep -v "Unknown" us_counties_covid19cases.csv| awk 'BEGIN{FS=","; OFS=","}{if ($4!="" && $1!="" && $6!=""){print $4, $1, $6}}' | grep -f fips.txt > deaths.csv
#cat <(echo -e "fips,date,amount") deaths.csv > deaths.hd.csv
#mv deaths.hd.csv deaths.csv

awk 'BEGIN{FS=","; OFS=","}{print $0}' mask-use-by-county.csv |grep -f fips.txt > masks.csv
#cat <(echo -e "fips,never,rarely,sometimes,frequently,always") masks.csv > masks.hd.csv
#mv masks.hd.csv masks.csv
