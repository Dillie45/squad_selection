from flask import Flask, render_template, request,redirect
import mysql.connector

app = Flask(__name__)
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="454545",
    database="cricket"
)

players_global=[]
i=0
best11=[]
extra4=[]
@app.route('/')
def index():
    global players_global
    return render_template('index.html')

@app.route('/batsmen', methods=['GET', 'POST'])
def batsmen():
    return render_template('batsmen.html')


@app.route('/fetch_batsmen_data', methods=['GET', 'POST'])
def fetch_batsmen_data():
    global players_global
    if request.method == 'POST':
        name=[]
        role=[]
        batting=[]
        totalruns=[]
        totalmatches=[]
        totalaverage=[]
        totalstrikerate=[]
        if (request.form.get('runs')):
            runs=request.form.get('runs')
        else:
            runs=0
        if(request.form.get('strikerate')):
            strikerate = request.form.get('strikerate')
        else:
            strikerate=0
        cursor = db.cursor()

        query = f"SELECT batsmen.player,info.batting_style,info.playing_role,batsmen.matches,batsmen.runs,batsmen.average,batsmen.strikerate from info join batsmen on batsmen.id=info.id WHERE batsmen.Runs > {runs} AND batsmen.Strikerate > {strikerate}"
        cursor.execute(query)
        players=cursor.fetchall()
        for row in players:
            name.append(row[0])
            batting.append(row[1])
            role.append(row[2])
            totalmatches.append(row[3])
            totalruns.append(row[4])
            totalaverage.append(row[5])
            totalstrikerate.append(row[6])
        cursor.close()
        n=len(name)
        #print("Updated Players:", players_global)

        #return render_template('index.html', players=players)
    return render_template('batsmen.html',name=name,batting=batting,role=role,totalmatches=totalmatches,totalruns=totalruns,totalaverage=totalaverage,totalstrikerate=totalstrikerate,n=n)



@app.route('/best11_process', methods=['GET', 'POST'])
def best11_process():
    global best11
    global extra4
    player=request.form.get('player')
    
    if(len(best11)==11 and len(extra4)==4):
        msg15='Your squad is full'
        return render_template('best.html',best_player=best11,extra_player=extra4,msg15=msg15)
    else:
        if player in best11:
            msg="You already picked "+player
            return render_template('index.html',msg=msg)
        else:
            if(len(best11)<11):
                best11.append(player)
                return render_template('best.html',best_player=best11)
            else:
                extra4.append(player)
                return render_template('best.html',best_player=best11,extra_player=extra4)



@app.route('/allrounder',methods=['GET'])
def allrounder():
    return render_template('allrounder.html')
@app.route('/fetch_allrounder_data', methods=['GET', 'POST'])
def fetch_allrounder_data():
    global players_global
    if request.method == 'POST':
        name=[]
        role=[]
        batting=[]
        bowling=[]
        totalruns=[]
        totalmatches=[]
        totalwkts=[]
        totalstrikerate=[]
        if (request.form.get('runs')):
            runs=request.form.get('runs')
        else:
            runs=0
        if(request.form.get('strikerate')):
            strikerate = request.form.get('strikerate')
        else:
            strikerate=0
        if(request.form.get('wkts')):
            wkts=request.form.get('wkts')
        else:
            wkts=0
        cursor = db.cursor()
        query = f"SELECT batsmen.Player,info.batting_style,info.bowling_style,info.playing_role,batsmen.matches,batsmen.runs,bowler.wickets,batsmen.strikerate from batsmen JOIN bowler on batsmen.Player = bowler.Player join info on batsmen.id=info.id WHERE batsmen.Runs > {runs} AND batsmen.Strikerate > {strikerate} AND bowler.Wickets > {wkts}"
        cursor.execute(query)
        players=cursor.fetchall()
        for row in players:
            name.append(row[0])
            batting.append(row[1])
            bowling.append(row[2])
            role.append(row[3])
            totalmatches.append(row[4])
            totalruns.append(row[5])
            totalwkts.append(row[6])
            totalstrikerate.append(row[7])
        cursor.close()
        n=len(name)
        players_global = players
        #print("Updated Players:", players_global)

        #return render_template('index.html', players=players)
    return render_template('allrounder.html',name=name,batting=batting,bowling=bowling,role=role,totalmatches=totalmatches,totalruns=totalruns,totalwkts=totalwkts,totalstrikerate=totalstrikerate,n=n)


@app.route('/bowler',methods=['GET', 'POST'])
def bowler():
    return render_template('bowler.html')
@app.route('/fetch_bowler_data', methods=['GET', 'POST'])
def fetch_bowler_data():
    global players_global
    if request.method == 'POST':
        name=[]
        role=[]
        bowling=[]
        totaleconomy=[]
        totalmatches=[]
        totalwkts=[]
        totalaverage=[]
        if(request.form.get('wkts')):
            wkts=request.form.get('wkts')
        else:
            wkts=0
        if (request.form.get('average')):
            average=request.form.get('average')
        else:
            average=100
        if (request.form.get('economy')):
            economy=request.form.get('economy')
        else:
            economy=100
        cursor = db.cursor()
        query = f"SELECT bowler.Player,info.playing_role,info.bowling_style,bowler.matches,bowler.wickets,bowler.economy,bowler.average FROM bowler join batsmen on bowler.player=batsmen.player join info on batsmen.id=info.id WHERE bowler. Wickets > {wkts} AND bowler.Average < {average} and bowler.economy < {economy}"
        cursor.execute(query)
        players=cursor.fetchall()
        for row in players:
            name.append(row[0])
            role.append(row[1])
            bowling.append(row[2])
            totalmatches.append(row[3])
            totalwkts.append(row[4])
            totaleconomy.append(row[5])
            totalaverage.append(row[6])
        cursor.close()
        n=len(name)
        players_global = players
        #print("Updated Players:", players_global)
        #return render_template('index.html', players=players)
    return render_template('bowler.html',name=name,role=role,bowling=bowling,totalmatches=totalmatches,totalwkts=totalwkts,totaleconomy=totaleconomy,totalaverage=totalaverage,n=n)


@app.route('/best', methods=['GET'])
def best():
    global best11
    return render_template('best.html',best_player=best11)


@app.route('/bio')
def bio():
    player=request.args.get('player_name')
    cursor=db.cursor()
    query=f"select info.full_name,info.born,info.age,info.playing_role,info.bio from info join batsmen on batsmen.id=info.id where batsmen.player='{player}'"
    cursor.execute(query)
    biodata=cursor.fetchall()
    cursor.close()
    return render_template("bio.html",bio=biodata)



if __name__ == '__main__':
    app.run(debug=True)
