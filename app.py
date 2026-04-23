from flask import Flask, render_template_string, request, redirect, url_for, send_file
from pathlib import Path

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent
history = []
state = {"logged": False, "route": "-", "fare": "0"}
stations = ["AIIMS Bhopal Metro Station","Alkapuri Metro Station","DRM Office Metro Station","Rani Kamlapati Metro Station","Board Office Chauraha Metro Station","DB City Mall Metro Station","Kendriya Vidyalaya Metro Station","Subhash Nagar Metro Station","Karond Circle","Krishi Upaj Mandi","DIG Bungalow","Sindhi Colony","Nandra Bus Stand","Bhopal Junction Metro Station","Aishbagh Crossing","Bogda Pul","Bhadbhada Square","Depot Square","Jawahar Chowk","Roshanpura Square","Minto Hall","Lily Talkies","Prabhat Square","Govindpura","J.K. Road","Indrapuri","Piplani","Ratnagiri Tiraha"]
HTML = """<!doctype html><html><head><meta name='viewport' content='width=device-width,initial-scale=1'><title>BHOPAL METRO Navigation</title><link rel='stylesheet' href='https://unpkg.com/leaflet/dist/leaflet.css'/><script src='https://unpkg.com/leaflet/dist/leaflet.js'></script><style>body{font-family:Arial;margin:0;background:#f4f6f8}.wrap{display:flex;min-height:100vh}.left{flex:1;background:url('/static-login') center/cover no-repeat}.right{flex:1;display:flex;align-items:center;justify-content:center;padding:20px}.card,.box{background:#fff;padding:24px;border-radius:18px;box-shadow:0 8px 20px rgba(0,0,0,.1)}.card{width:360px;max-width:100%}.dash{padding:20px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px}.input,button{width:100%;padding:10px;margin:8px 0;box-sizing:border-box}button{background:#ff7a00;color:#fff;border:0;cursor:pointer}ul{padding-left:18px;margin:0}img{width:100%;height:250px;border-radius:10px}.wide{grid-column:1/-1}#map{height:420px;border-radius:12px}</style></head><body>{% if not logged %}<div class='wrap'><div class='left'></div><div class='right'><div class='card'><h1>BHOPAL METRO Navigation</h1><form method='post' action='/login'><input class='input' name='user' placeholder='Username' required><input class='input' type='password' name='password' placeholder='Password' required><button type='submit'>Login</button></form></div></div></div>{% else %}<div class='dash'><h1>BHOPAL METRO Navigation</h1><div class='grid'><div class='box'><h3>Search Route</h3><button type='button' onclick='askAI()'>AI Chatbot</button><button type='button' onclick='voiceSearch()'>Voice Search</button><form method='post' action='/search'><input class='input' name='from_station' list='stations' placeholder='1. Station Name / From Where' required><input class='input' name='to_station' list='stations' placeholder='Destination' required><datalist id='stations'>{% for station in stations %}<option value='{{station}}'>{% endfor %}</datalist><button type='submit'>Find</button></form></div><div class='box'><h3>Route</h3><p>{{route}}</p></div><div class='box'><h3>Fare</h3><p>₹ {{fare}}</p></div><div class='box'><h3>Routes on Map</h3><a href='/route-map' target='_blank'><img src='/route-map'></a></div><div class='box wide'><h3>Interactive Metro Map</h3><div id='map'></div></div><div class='box wide'><h3>History</h3><ul>{% for item in history %}<li>{{item}}</li>{% endfor %}</ul></div></div></div><script>if(document.getElementById('map')){var map=L.map('map').setView([23.255,77.43],12);L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);var orange=[[23.332,77.412],[23.315,77.409],[23.298,77.407],[23.283,77.406],[23.270,77.409],[23.262,77.417],[23.247,77.425],[23.238,77.434],[23.232,77.442],[23.226,77.446],[23.220,77.447],[23.214,77.455],[23.208,77.463]];var blue=[[23.221,77.392],[23.232,77.402],[23.242,77.414],[23.251,77.424],[23.245,77.433],[23.247,77.443],[23.250,77.454],[23.252,77.466],[23.254,77.478],[23.256,77.492],[23.258,77.505]];L.polyline(orange,{color:'orange',weight:5}).addTo(map);L.polyline(blue,{color:'blue',weight:5}).addTo(map);}</script>{% endif %}<script>
async function askAI(){const q=prompt('Ask AI Assistant'); if(!q)return; const fd=new FormData(); fd.append('q',q); const r=await fetch('/ai-chat',{method:'POST',body:fd}); const d=await r.json(); alert(d.reply);} 
function voiceSearch(){const SR=window.SpeechRecognition||window.webkitSpeechRecognition; if(!SR){alert('Voice not supported');return;} const rec=new SR(); rec.onresult=e=>{document.querySelector("input[name='from_station']").value=e.results[0][0].transcript;}; rec.start();}
</script></body></html>"""
@app.route('/')
def home(): return render_template_string(HTML, logged=state['logged'], route=state['route'], fare=state['fare'], history=history, stations=stations)
@app.route('/login', methods=['POST'])
def login(): state['logged']=True; return redirect(url_for('home'))
@app.route('/search', methods=['POST'])
def search():
 f=request.form.get('from_station','').strip(); t=request.form.get('to_station','').strip();
 if not f or not t: return redirect(url_for('home'))
 state['route']=f+' → '+t; state['fare']=str(10 if f==t else 20); history.append(state['route']+' | ₹'+state['fare']); return redirect(url_for('home'))
@app.route('/static-login')
def static_login(): return send_file(BASE_DIR / 'm photo.jpeg', mimetype='image/jpeg')
@app.route('/route-map')
def route_map(): return send_file(BASE_DIR / 'main photo.jpeg', mimetype='image/jpeg')
@app.route('/ai-chat', methods=['POST'])
def ai_chat():
 q=request.form.get('q','').lower();
 ans='Please ask about routes, fare, timings or stations.'
 if 'fare' in q: ans='Use Search Route to see fare instantly.'
 elif 'station' in q: ans='Available stations are listed in search suggestions.'
 elif 'route' in q: ans='Enter From and To station for best route.'
 return {'reply':ans}

if __name__=='__main__': app.run(debug=True)
