# doc_manage
A simple document management application. Built to handle construction projects.  
  
`$ git clone git@github.com:grzegorzswitek/doc_manage.git`  
`$ cd doc_manage`  
`$ sudo docker-compose -f docker-compose.prod.yml build web`  
`$ sudo docker-compose -f docker-compose.prod.yml up`  
Open new bash tab  
`$ docker exec -it doc_manage_web_1 bash`  
`# python manage.py migrate`  
`# python manage.py createsuperuser`  
`# (...)`  
`# exit`  
Open in browser `localhost:1337/admin` and log in  
