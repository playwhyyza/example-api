วิธีการติดตั้ง

ที่สิ่งต้องมี:
- OS: ubuntu 18.04
- python: 3.6

1. ติดตั้ง pip โดยใช้คำสั่ง - $ sudo apt install python3-pip
2. ทำการติดตั้ง pipenv โดยใช้คำสั่ง 
    - $ sudo pip3 install pipenv
3. เปิดใช้งาน pipenv โดยการพิมพ์ 
    - $ pipenv install
    - โดยจะต้องอยู่ในตำแหน่งเดียวกันกับโฟล์เดอร์ที่มีไฟล์ Pipfile, Pipfile.lock
    - ในกรณีที่ติดตั้งไปแล้ว สามารถเข้าใช้งานโดยใช้คำสั่ง
    - $ pipenv shell 
4. ทำการสร้าง Database โดยการใช้คำสั่ง 
    - $ python api.py db init
    - $ python api.py db migrate
    - $ python api.py db upgrade

5. ทำการรันเซิร์ฟเวอร์ โดยการใช้คำสั่ง
    - $ python api.py runserver 
    
    ถ้าต้องการเปิดใช้งานโหมด debug ให้เพิ่มคำสั่ง --debug ต่อท้าย
    - $ python api.py runserver --debug
