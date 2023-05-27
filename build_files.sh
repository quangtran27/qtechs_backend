# build_files.sh
pip install -r requirements.txt

# make migrations
python39 manage.py makemigrations
python39 manage.py migrate 
python39 manage.py collectstatic
