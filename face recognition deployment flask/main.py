# import the necessary packages
from flask import Flask, render_template, Response,request,redirect,url_for
from camera import VideoCamera
import sqlite3
import os
app = Flask(__name__)
@app.route('/')
def startpage():
    # rendering webpage
    return render_template('start_page.html')
@app.route('/index')
def index():
    # rendering webpage
    return render_template('index.html')
@app.route('/fill_details')
def fill_details():
    # rendering webpage
    return render_template('fill_details.html')

@app.route('/get_info',methods=['POST'])
def get_info():
    name=[x for x in request.form.values()]
    print(name)
    n1=name[0].replace(" ","")
    n2=name[1].replace(" ","")
    if n1=="" or n2=="":
        return redirect(url_for('fill_details'))
    else:
        # return redirect(" {{url_for('index')}} ")
        # return redirect(url_for('startpage'))             # See we write the function name of the route ie start page is the fn of the home page 
        conn=sqlite3.connect("user.db") #-----------------------------------------------
        
        #if the no. of user >20 then delete the last 19 users

        
        cmd="select count(id) from user;"
        cursor=conn.execute(cmd)
        data=cursor.fetchall()
        print(data)
        if data[0][0]>5:
            cmd="delete from user where id>1;"
            conn.execute(cmd)
            conn.commit()
            cmd="UPDATE SQLITE_SEQUENCE SET seq = 0 WHERE name = 'user';"
            conn.execute(cmd)
            conn.commit()
            path='dataset'
            imagePaths=[os.path.join(path,f) for f in os.listdir(path)] 
            for imagePath in imagePaths:
                Id=int(os.path.split(imagePath)[-1].split(".")[1])
                # print("id is: ",id)
                if Id>1:
                    os.remove(imagePath)













        cmd="insert into user(f_name,l_name) values('"+str(n1)+"','"+str(n2)+"');"
        conn.execute(cmd)
        conn.commit()
        conn.close()
        # data=cursor.fetchall() 
        return render_template('make_dataset.html')

    
def gen(camera):
    while True:
        #get camera frame
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def create_data(camera):
    conn=sqlite3.connect("user.db") #-----------------------------------------------
    cmd="select count(id) from user;"
    cursor=conn.execute(cmd)
    data=cursor.fetchall()
    num=0
    
    id=data[0][0]
    while True:
        if num>30:
            break
        num+=1
        #get camera frame
        frame = camera.create(id,num)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/create_dataset')
def create_dataset():
          

        return Response(create_data(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/train_dataset')
def train_dataset():
        print("training going on................................")
        VideoCamera.train()
        return redirect(url_for('startpage'))



if __name__ == '__main__':
    # defining server ip address and port
    app.run(host='0.0.0.0',port='5000', debug=True)
