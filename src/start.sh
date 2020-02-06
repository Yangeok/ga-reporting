echo ""
echo -n "> startDate: "
read START_DATE
echo ""
echo -n "> endDate: "
read END_DATE

export START_DATE
export END_DATE

python index.py --noauth_local_webserver