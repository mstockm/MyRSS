echo "------------------------\n" >> `dirname $0`/out.log

echo "Loading venv.....\n" >> `dirname $0`/out.log
source `dirname $0`/activate
echo "Updating streams.......\n" >> `dirname $0`/out.log
python `dirname $0`/update.py
echo "Complete\n" >> `dirname $0`/out.log
