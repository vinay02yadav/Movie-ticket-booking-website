from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os


app = Flask(__name__)
app.secret_key = "secret key"

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_BINDS'] = {"db1":'sqlite:///' + os.path.join(basedir, 'login_db.sqlite3'), "db2":'sqlite:///' + os.path.join(basedir, 'movie_db.sqlite3')}

# app.config['SQLALCHEMY_BINDS'] = {"db1":r'sqlite:///login_db.sqlite3', "db2":r'sqlite:///C:\Users\02vya\OneDrive\Desktop\New folder\movie_db.sqlite3'}

db = SQLAlchemy()
db.init_app(app)
app.app_context().push()


class Login(db.Model):
    __bind_key__ = 'db1'
    __tablename__ = 'login'
    username = db.Column(db.String, unique=True,
                         nullable=False, primary_key=True)
    password = db.Column(db.String, nullable=False)

class Summary(db.Model):
    __bind_key__ = 'db2'
    __tablename__ = 'movies_db'
    username = db.Column(db.String,primary_key=True)
    location = db.Column(db.String,primary_key=True)
    venue = db.Column(db.String,primary_key=True)
    place = db.Column(db.String,primary_key=True)
    time = db.Column(db.String,primary_key=True)
    date = db.Column(db.String,primary_key=True)
    movie_name = db.Column(db.String,primary_key=True)
    seats = db.Column(db.String,primary_key=True)
    rating = db.Column(db.String)

class Movie(db.Model):
    __bind_key__ = 'db2'
    __tablename__ = 'movies'
    film_id = db.Column(db.Integer,primary_key=True)
    movie_name = db.Column(db.String)
    time = db.Column(db.String,primary_key=True)
    venue = db.Column(db.String,primary_key=True)
    date = db.Column(db.String,primary_key=True)
    price = db.Column(db.Integer)
    total_seats = db.Column(db.Integer)
    seats_left = db.Column(db.Integer)
    trailer = db.Column(db.String)
    rating = db.Column(db.String)
    image = db.Column(db.String)
    release_date = db.Column(db.String)
    description = db.Column(db.String)
    place = db.Column(db.String)
    location = db.Column(db.String,primary_key=True)
    genre = db.Column(db.String)


flag=False

# user login form
@app.route('/login', methods=['GET', 'POST'])
def loogin():
    if request.method == 'POST':
        usern = request.form['user']
        passw = request.form['pass']

        if usern == "" or passw == "":
            flash('Please fill all details')
            return render_template("error_login.html")
        else:
            try:
                stu = Login.query.filter_by(username=usern).first()  
                if stu.username == usern and stu.password == passw:
                    return redirect(f'/movie_dashboard/{usern}/search/ssearch')
                else:
                    flash('Invalid Username or Password')
                    return render_template("error_login.html")
            except:
                flash('Incorreect Username or Password')
                return render_template("error_login.html")

    else:
        mov=Movie.query.all()
        d=[]
        for i in mov:
            d.append(i.film_id)
        # print(d)    
        return render_template('user_login.html',d=d)


# user register form
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        usern = request.form['user']
        pass1 = request.form['pass1']
        pass2 = request.form['pass2']

        if(pass1!=pass2):
            flag="passnotmatch"
            return render_template("user_register.html",flag=flag)
        else:
            try:
                stu = Login.query.filter_by(username=usern).first()
                if stu.username == usern:
                    flag="already"
                    return render_template("user_register.html",flag=flag)
                else:
                    stu = Login(username=usern, password=pass1)
                    db.session.add(stu)
                    db.session.commit()
                    return render_template('user_login.html')
            except:
                stu = Login(username=usern, password=pass1)
                db.session.add(stu)
                db.session.commit()
                return render_template('user_login.html')

    else:
        return render_template('user_register.html')


# Basic starting template
@app.route('/', methods=["GET","POST"])
def index():
    if request.method == 'POST':
        return redirect('/admin_login')
    else:
        return render_template("index.html")


# admin login form
@app.route('/admin_login', methods=["GET","POST"])
def ad_login():
    if request.method == 'POST':
        user=request.form['user']
        passw=request.form['pass']

        if(user=="admin_01" and passw=="admin"):
            return redirect('/admin_dashboard')
        else:
            return render_template("admin_login.html",t=True)
    else:
        return render_template("admin_login.html")
    

@app.route('/admin_dashboard', methods=["GET","POST"])
def ad_dash():
    if request.method == 'POST':
        pass
    else:
        move=Movie.query.all()
        d=[]
        for i in move:
            if i.venue not in d:
                d.append(i.venue)
        # print(d)
        return render_template("admin_dashboard.html",d=d)
    

# for adding and editing new venues
@app.route('/add_venue/<old_venue>', methods=["GET","POST"])
def ad_venue(old_venue):
    if request.method == 'POST':
        vvenue=request.form['venuee']
        place=request.form['place']
        location=request.form['location']
        capacity=request.form['capacity']
        # print(old_venue)
        if old_venue=="<<none>>":  # adding new venue
            # print(vvenue,place,location,capacity)
            new_place=Movie(film_id='998999',movie_name='null',venue=vvenue,location=location,total_seats=capacity,seats_left=capacity,place=place,date='null',time='null')
            db.session.add(new_place)
            db.session.commit()
        else:       # editing old venue
            old_venue=old_venue[1:len(old_venue)-1]
            new_venue=Movie.query.filter_by(venue=old_venue).all()

            for i in new_venue:
                i.venue=vvenue
                i.place=place
                i.location=location
                i.seats_left = int(i.seats_left)+(int(capacity)-int(i.total_seats))
                i.total_seats=capacity
                db.session.commit()

        return redirect('/admin_dashboard')
    else:
        return render_template("add_admin_venue.html",old_venue=old_venue)

# for adding and editing new shows
@app.route('/add_shows/<venue>/<old_show>/<location>/<time>/<date>', methods=["GET","POST"])
def add_shows(venue,old_show,location,time,date):
    if request.method == 'POST':
        show=request.form['show']
        Rating=request.form['rating']
        Timimgs=request.form['Timimgs']
        Date=request.form['Date']
        Tags=request.form['Tags']
        Price=request.form['Price']

        if old_show=="none":   # adding new shows
            new_show=Movie(film_id='999999',movie_name=show,rating=Rating,date=Date,price=Price,venue=venue,time=Timimgs,place=time,location=location,genre=Tags,total_seats=date,seats_left=date)
            db.session.add(new_show)
            db.session.commit()

        else:           # editing old shows
            # print(old_show+"/"+venue+"/"+location+"/"+time+"/"+date)
            new_show=Movie.query.filter_by(movie_name=old_show,venue=venue,location=location,time=time,date=date).first()

            new_show.movie_name=show
            new_show.rating=Rating
            new_show.time=Timimgs
            new_show.date=Date
            new_show.price=Price
            new_show.genre=Tags
            db.session.commit()

        return redirect('/admin_dashboard')
    
    else:
        return render_template("add_admin_shows.html",venue=venue,old_show=old_show,location=location,time=time,date=date)
    
# for showing venues in admin dashboard , editing and deleting venues and shows
@app.route('/shows', methods=["GET","POST"])
def ad_show():
    if request.method == 'POST':
        ss=""
        l=[]
       
        s=request.form['btnn']
        # print(s)
        l=s.split(',')
        # print(l)

        if l[0]=='delete':
            dele = Movie.query.filter_by(venue=l[1]).all()
            for i in dele:
                db.session.delete(i)
            db.session.commit()
        elif l[0]=='edit':
            return redirect(url_for("ad_venue",old_venue=l[1]))
        elif l[0]=='delete_show':
            dele = Movie.query.filter_by(movie_name=l[1],venue=l[2],location=l[3],time=l[4],date=l[5]).first()
            db.session.delete(dele)
            db.session.commit()
        elif l[0]=='edit_show':
            return redirect(url_for("add_shows",venue=l[2],old_show=l[1],location=l[3],time=l[4],date=l[5]))

        else:
            d={}
            flagg=False
            move=Movie.query.all()
            for i in move:
                if i.venue not in d:
                    d[i.venue]=Movie.query.filter_by(venue=i.venue).all()
                    ne=Movie.query.filter_by(venue=i.venue).first()
                    place=ne.place
                    location=ne.location
                    capacity = ne.total_seats
            for i in d:
                if s==i:
                    ss=i 
                    break
        
            return render_template("admin_shows.html",d=d,s=ss,venue=ss,place=place,location=location,capacity=capacity)

        return redirect("/admin_dashboard")

    else:
        return redirect("/admin_dashboard")
    

# for showing movies in user dashboard
@app.route('/movie_dashboard/<username>/<search>/<ssearch>', methods=['GET', 'POST'])
def movies(username,search,ssearch):
    if request.method == 'POST':

        if search ==  'search':
            search_by=request.form['search_by']
            innput=request.form['search_input']

            if search_by == 'movie':
                move=Movie.query.filter_by(movie_name=innput).first()
                l=[]
                l.append(move.movie_name)
                return render_template("user_shows.html",d=l,username=username)
            
            elif search_by == 'location':
                move=Movie.query.filter_by(location=innput).all()
                l=[]
                for i in move:
                    l.append(i.movie_name)
                
                l=set(l)
                return render_template("user_shows.html",d=l,username=username)
            
            elif search_by == 'tags':
                move=Movie.query.all()
                l=[]
                
                for i in move:
                    listt = i.genre.split(',')
                    for j in listt:
                        if j == innput:
                            l.append(i.movie_name)
                
                l=set(l)
                return render_template("user_shows.html",d=l,username=username)

            elif search_by == 'rating':
                move=Movie.query.all()
                l=[]
                
                for i in move:
                    if i.rating == innput:
                        l.append(i.movie_name)
                
                l=set(l)
                return render_template("user_shows.html",d=l,username=username)

        else:
            print("esle")
            s=request.form['btnn']
            print(s)

            return redirect(url_for('dashboard',username=username,movie=s))
    else:
        
        l=[]
        move=Movie.query.all()
        for i in move:
            if i.movie_name not in l:
               l.append(i.movie_name)
        
    
        return render_template("user_shows.html",d=l,username=username)

# showing details of particular movie 
@app.route('/movie_dashboard/<username>/<movie>', methods=["GET","POST"])
def dashboard(username,movie):
    if request.method == 'POST':
        # try:
        btn=request.form['radioname']
        l=btn.split(',')
        # print(l)
        venue=l[1]
        location=l[2]
        time=l[3]
        date=l[4]
        place=l[5] 
        print(venue,location,time,date,place)

        # except:
        #     pass
    
        return redirect(f'/movie_dashboard/{username}/{movie}/{location}/{place}/{venue}/{time}/{date}/booking')
    
    else:
        print("elase")
        print(movie)
        d={}
        details=Movie.query.filter_by(movie_name=movie).first()
        all_venue=Movie.query.filter_by(movie_name=movie).all()

        for i in all_venue: 
            if i.location not in d:
                d[i.location]={}
            if i.place not in d[i.location]:
                d[i.location][i.place]={}
            if i.venue not in d[i.location][i.place]:
                d[i.location][i.place][i.venue]={}
                d[i.location][i.place][i.venue][i.time+","+i.date]=i.seats_left
            else:
                d[i.location][i.place][i.venue][i.time+","+i.date]=i.seats_left

        print(json.dumps(d,indent=4)) 
        return render_template('movie_dashboard.html',username=username,details=details,d=d)
    

# for confirming bookings
@app.route('/movie_dashboard/<username>/<movie>/<location>/<place>/<venue>/<time>/<date>/booking', methods=["GET","POST"])
def confirm_booking(username,movie,location,place,venue,time,date):
    if request.method == 'POST':
            s=Movie.query.filter_by(movie_name=movie,venue=venue,location=location,time=time,date=date,place=place).first()

            seat=request.form['number_of_seats']
            s.seats_left = s.seats_left - int(seat)
            db.session.commit()

            data=Summary(username=username,movie_name=movie,venue=venue,location=location,time=time,date=date,place=place,seats=seat,rating='0')

            db.session.add(data)
            db.session.commit()

            return redirect(f'/movie_dashboard/{username}/search/ssearch')


    else:
        details=Movie.query.filter_by(movie_name=movie,location=location,place=place,venue=venue,time=time,date=date).first()
        print(details)
        return render_template('booking.html',username=username,details=details)


@app.route('/user_shows', methods=["GET","POST"])
def us_show():
    if request.method == 'POST':
        ss=""
        l=[]
       
        s=request.form['btnn']
        # print(s)
        l=s.split(',')
        # print(l)

        if l[0]=='delete':
            pass

        else:
            d={}
            flagg=False
            move=Movie.query.all()
            for i in move:
                if i.venue not in d:
                    d[i.venue]=Movie.query.filter_by(venue=i.venue).all()
            for i in d:
                if s==i:
                    ss=i 
                    break
        
            return render_template("user_shows.html",d=d,s=ss,venue=ss)

        return redirect("/movie_dashboard")

    else:
        return redirect("/admin_dashboard")


# for showing bookings that user have booked
@app.route('/movie_dashboard/<username>/summary', methods=["GET","POST"])
def summary(username):
        if request.method == 'POST':
            btn=request.form['button']
            # print(btn)
            rating=request.form['quantity']
            l=btn.split(',')
            print(l)
            print(rating)
            s=Summary.query.filter_by(movie_name=l[0],venue=l[1],place=l[2],location=l[3],seats=l[4],username=username).first()
            s.rating=rating
            db.session.commit()
           
            return redirect(f'/movie_dashboard/{username}/summary')
        else:
            data=Summary.query.filter_by(username=username).all()
            # l=[]
            # for i in data:
            #     l.append("$"+i.rating+"$")
            # print(l)
            return render_template('user_summary.html',username=username,data=data)



# for showing admin summary
@app.route('/admin_dashboard/summary', methods=["GET","POST"])
def admin_summary():
    if request.method=="POST":
        pass
    else:
        d={}
        average=[]
        movie=[]
        summ=Summary.query.all()
        s=""
        for i in summ:
            if i.movie_name not in d:
                d[i.movie_name] = []
                d[i.movie_name].append(int(i.rating))
            else:
               d[i.movie_name].append(int(i.rating))
        
        # print(json.dumps(d,indent=4))

        for i in d:
            count=d[i].count(0)
            length = len(d[i])
            try:
                avg = sum(d[i])/(length-count)
            except:
                avg=0
            average.append(avg)
            movie.append(i)

        plt.figure().set_figheight(18)
        plt.xticks(rotation=90)

        plt.bar(movie, average, 
                width = 0.6, color = ['orange', 'lightgreen'])
        
        plt.xlabel('Movies',fontsize=10)
        plt.ylabel('Rating')
        plt.title('Rating of all movies')
        plt.savefig(r'static\img.png')
        plt.close()

        return render_template('admin_summary.html')


@app.route('/api', methods=["GET","POST"])
def api():
    data = request.form.to_dict(flat=False)
    # print(data)

    
    timee=0
    for i in range(10):

        film_id=data[f'films[{i}][film_id]'][0]
        movie_name=data[f'films[{i}][film_name]'][0]
        release_date=data[f'films[{i}][release_dates][0][release_date]'][0]
        trailer=data[f'films[{i}][film_trailer]'][0]
        description=data[f'films[{i}][synopsis_long]'][0]
        image=data[f'films[{i}][images][poster][1][medium][film_image]'][0]
        rating=data['films[0][age_rating][0][rating]'][0]

        try:
            mov=Movie(film_id=film_id,movie_name=movie_name,date='28-3-2023',venue='Rohtak mall',time=f'{timee}',price=100,total_seats=80,seats_left=80,trailer=trailer,description=description,rating=rating,image=image,release_date=release_date,location='Rohtak')
            
            
            
            db.session.add(mov)
            db.session.commit()
            timee+=1
        except:
            # print("-----------------error")
            continue
            

    return redirect('/')

@app.route('/api2', methods=["GET","POST"])
def api2():
    if request.method == 'POST':
        data = request.form.to_dict(flat=False)
        # data['title'] = request.json['title']
        # print(data) 
        
        film_id=data['film_id'][0]
        venue=data['cinemas[0][cinema_name]'][0]
        place=data['cinemas[0][address]'][0]
        location=data['cinemas[0][city]'][0]
        date=data['cinemas[0][date]'][0]
        timee=data['cinemas[0][time]'][0]

        print(film_id,venue,place,location,date,timee)

        mov=Movie.query.filter_by(film_id=film_id).all()
        for i in mov:
            i.venue=venue
            i.place=place
            i.location=location
            i.date=date
            i.time=timee
            db.session.commit()
    return redirect('/')



if __name__ == '__main__':
    app.run(debug=True)