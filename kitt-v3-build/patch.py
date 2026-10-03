from pathlib import Path

root = Path("JARVIS_FERDI_ANDROID")
html = root / "app/src/main/assets/index.html"
s = html.read_text()

def req(old, new, label):
    global s
    if old not in s:
        raise SystemExit("Patch target missing: " + label)
    s = s.replace(old, new)

req(
""".voicebox{min-height:275px;border-radius:17px;border:1px solid #45000a;background:radial-gradient(circle at 50% 45%,rgba(190,0,0,.12),#010101 63%);display:flex;align-items:center;justify-content:center;position:relative;overflow:hidden;box-shadow:inset 0 0 20px #000}.bars{height:240px;width:90%;display:flex;justify-content:center;gap:5px;align-items:center}.barcol{display:flex;flex-direction:column-reverse;gap:4px;justify-content:center}.barcol i{display:block;width:22px;height:12px;background:#450006;border-radius:1px}.barcol.active i{animation:led 1.1s infinite ease-in-out}.barcol:nth-child(2) i{width:27px}.barcol:nth-child(2).active i{animation-delay:.12s}.barcol:nth-child(3).active i{animation-delay:.23s}@keyframes led{0%,100%{background:#350006;box-shadow:none}45%{background:#ff1820;box-shadow:0 0 9px #f00}70%{background:#8f0008}}
.voicebox.listening .barcol i{animation-duration:.42s}.voicebox.speaking .barcol i{animation-duration:.28s}.center""",
""".voicebox{min-height:275px;border-radius:17px;border:1px solid #45000a;background:radial-gradient(circle at 50% 45%,rgba(190,0,0,.12),#010101 63%);display:flex;align-items:center;justify-content:center;position:relative;overflow:hidden;box-shadow:inset 0 0 20px #000}.bars{height:240px;width:90%;display:flex;justify-content:center;gap:5px;align-items:center}.barcol{display:flex;flex-direction:column-reverse;gap:4px;justify-content:center}.barcol i{display:block;width:22px;height:12px;background:#300004;border-radius:1px;box-shadow:none;transition:background .035s linear,box-shadow .035s linear,opacity .035s linear;opacity:.65}.barcol:nth-child(2) i{width:27px}.barcol i.lit{background:#ff1820;box-shadow:0 0 8px #f00,0 0 15px rgba(255,0,0,.55);opacity:1}.voicebox.speaking{box-shadow:inset 0 0 25px rgba(255,0,0,.12),0 0 12px rgba(255,0,0,.08)}.center""",
"voice CSS"
)

req(
'<div class="barcol active" id="c1"></div><div class="barcol active" id="c2"></div><div class="barcol active" id="c3"></div>',
'<div class="barcol" id="c1"></div><div class="barcol" id="c2"></div><div class="barcol" id="c3"></div>',
"voice markup"
)

req(
"for(let n of [['c1',11],['c2',15],['c3',11]]){const e=$('#'+n[0]);for(let i=0;i<n[1];i++)e.appendChild(document.createElement('i'))}",
"for(let n of [['c1',11],['c2',15],['c3',11]]){const e=$('#'+n[0]);for(let i=0;i<n[1];i++)e.appendChild(document.createElement('i'))}let lastVoiceLevel=0;function lightColumn(id,count){const seg=[...document.querySelectorAll('#'+id+' i')];seg.forEach((x,i)=>x.classList.toggle('lit',i<count))}function setVoiceLevel(raw){let level=Math.max(0,Math.min(1,Number(raw)||0));lastVoiceLevel=level;if(level<.035){lightColumn('c1',0);lightColumn('c2',0);lightColumn('c3',0);return}const center=Math.max(1,Math.round(level*15));const sideBase=Math.max(0,Math.round(level*10));const wobble=Math.round(Math.sin(Date.now()/43)*1.5);lightColumn('c2',center);lightColumn('c1',Math.max(0,Math.min(11,sideBase+wobble)));lightColumn('c3',Math.max(0,Math.min(11,sideBase-wobble)))}",
"voice JS"
)

req(
"function setVisual(mode){const v=$('#voicebox'),eq=$('#eq');v.classList.remove('listening','speaking');eq.classList.remove('active');if(mode==='listen'){v.classList.add('listening');eq.classList.add('active');$('#systemStatus').textContent='LISTENING'}else if(mode==='speak'){v.classList.add('speaking');eq.classList.add('active');$('#systemStatus').textContent='RESPONDING'}else{$('#systemStatus').textContent='SYSTEM ONLINE';eq.classList.add('active')}}",
"function setVisual(mode){const v=$('#voicebox'),eq=$('#eq');v.classList.remove('listening','speaking');eq.classList.remove('active');if(mode==='listen'){v.classList.add('listening');$('#systemStatus').textContent='LISTENING';setVoiceLevel(0)}else if(mode==='speak'){v.classList.add('speaking');eq.classList.add('active');$('#systemStatus').textContent='RESPONDING'}else{$('#systemStatus').textContent='SYSTEM ONLINE';setVoiceLevel(0)}}",
"setVisual"
)

req(
"function speak(text){if(!settings.tts)return;setVisual('speak');if(NATIVE&&AndroidJarvis.speak){try{AndroidJarvis.speak(text);setTimeout(()=>setVisual('idle'),Math.min(7000,900+text.length*45));return}catch(e){}}if('speechSynthesis'in window){speechSynthesis.cancel();const u=new SpeechSynthesisUtterance(text);u.lang='de-DE';u.rate=.9;u.pitch=.72;const vs=speechSynthesis.getVoices();u.voice=vs.find(v=>/de/i.test(v.lang)&&/male|mann|de-de-x-deb/i.test(v.name))||vs.find(v=>/de/i.test(v.lang))||null;u.onend=u.onerror=()=>setVisual('idle');speechSynthesis.speak(u)}else setVisual('idle')}",
"function speak(text){if(!settings.tts)return;if(NATIVE&&AndroidJarvis.speak){try{AndroidJarvis.speak(text);return}catch(e){}}if('speechSynthesis'in window){speechSynthesis.cancel();const u=new SpeechSynthesisUtterance(text);u.lang='de-DE';u.rate=.86;u.pitch=.68;const vs=speechSynthesis.getVoices();u.voice=vs.find(v=>/de/i.test(v.lang)&&/male|mann|de-de-x-deb/i.test(v.name))||vs.find(v=>/de/i.test(v.lang))||null;u.onstart=()=>{setVisual('speak');setVoiceLevel(.45)};u.onboundary=()=>setVoiceLevel(.35+Math.random()*.55);u.onend=u.onerror=()=>{setVoiceLevel(0);setVisual(settings.wake?'listen':'idle')};speechSynthesis.speak(u)}}",
"speak"
)

req(
"window.onNativeJarvisEvent=function(type,text){if(type==='wake'){setVisual('listen');$('#wakeState').textContent='WAKE: ERKANNT';toast('K.I.T.T. aktiviert');return}if(type==='command'){addMessage('user',text);$('#systemStatus').textContent='THINKING';return}if(type==='reply'){addMessage('kitt',text);setVisual('speak');setTimeout(()=>setVisual('idle'),2500);return}if(type==='status'){$('#wakeDiag').textContent=text;if(/IMMER AN|NATIV AKTIV|Befehl sagen|WAKE WORD/i.test(text)){$('#wakeState').textContent='WAKE: AKTIV';settings.wake=true}return}if(type==='error'){toast(text);$('#wakeDiag').textContent='FEHLER: '+text;setVisual('idle')}};",
"window.onNativeJarvisEvent=function(type,text){if(type==='tts_start'){setVoiceLevel(0);setVisual('speak');return}if(type==='tts_level'){setVoiceLevel(parseFloat(text)||0);return}if(type==='tts_end'){setVoiceLevel(0);setVisual(settings.wake?'listen':'idle');return}if(type==='wake'){setVoiceLevel(0);setVisual('listen');$('#wakeState').textContent='WAKE: ERKANNT';toast('K.I.T.T. aktiviert');return}if(type==='command'){setVoiceLevel(0);addMessage('user',text);$('#systemStatus').textContent='THINKING';return}if(type==='reply'){addMessage('kitt',text);return}if(type==='status'){$('#wakeDiag').textContent=text;if(/IMMER AN|NATIV AKTIV|Befehl sagen|WAKE WORD/i.test(text)){$('#wakeState').textContent='WAKE: AKTIV';settings.wake=true}return}if(type==='error'){toast(text);$('#wakeDiag').textContent='FEHLER: '+text;setVoiceLevel(0);setVisual('idle')}};",
"native events"
)
html.write_text(s)

# version
p = root / "app/build.gradle"
s = p.read_text().replace("versionCode 2", "versionCode 3").replace("versionName '2.0.0'", "versionName '3.0.0'")
p.write_text(s)

# Service
p = root / "app/src/main/java/de/ferdi/jarvis/JarvisListeningService.java"
s = p.read_text()
s = s.replace("    private long lastHandledAt = 0L;\n", "    private long lastHandledAt = 0L;\n    private long lastAudioLevelAt = 0L;\n")
s = s.replace("        tts.setSpeechRate(0.90f);\n        tts.setPitch(0.74f);", "        tts.setSpeechRate(0.86f);\n        tts.setPitch(0.68f);")
old = """        tts.setOnUtteranceProgressListener(new UtteranceProgressListener() {
            @Override public void onStart(String utteranceId) {}
            @Override public void onDone(String utteranceId) {
                main.post(() -> {
                    speaking = false;
                    if (active) restartRecognition("PROMPT".equals(utteranceId) ? 300 : 450);
                });
            }
            @Override public void onError(String utteranceId) {
                main.post(() -> { speaking = false; if (active) restartRecognition(450); });
            }
        });"""
new = """        tts.setOnUtteranceProgressListener(new UtteranceProgressListener() {
            @Override public void onStart(String utteranceId) {
                lastAudioLevelAt = 0L;
                sendEvent("tts_start", utteranceId == null ? "" : utteranceId);
            }
            @Override public void onAudioAvailable(String utteranceId, byte[] audio) {
                long now = System.currentTimeMillis();
                if (now - lastAudioLevelAt < 28) return;
                lastAudioLevelAt = now;
                sendEvent("tts_level", String.format(Locale.US, "%.3f", pcmLevel(audio)));
            }
            @Override public void onDone(String utteranceId) {
                sendEvent("tts_level", "0");
                sendEvent("tts_end", utteranceId == null ? "" : utteranceId);
                main.post(() -> {
                    speaking = false;
                    if (active) restartRecognition("PROMPT".equals(utteranceId) ? 300 : 450);
                });
            }
            @Override public void onError(String utteranceId) {
                sendEvent("tts_level", "0");
                sendEvent("tts_end", utteranceId == null ? "" : utteranceId);
                main.post(() -> { speaking = false; if (active) restartRecognition(450); });
            }
        });"""
if old not in s: raise SystemExit("service listener target missing")
s = s.replace(old, new)
marker = "    private void sendEvent(String type, String text) {"
helper = """    private float pcmLevel(byte[] audio) {
        if (audio == null || audio.length < 2) return 0f;
        long sum = 0L;
        int samples = 0;
        for (int i = 0; i + 1 < audio.length; i += 2) {
            int lo = audio[i] & 0xff;
            int hi = audio[i + 1];
            short sample = (short) ((hi << 8) | lo);
            int a = Math.abs((int) sample);
            sum += (long) a * a;
            samples++;
        }
        if (samples == 0) return 0f;
        double rms = Math.sqrt((double) sum / samples) / 32768.0;
        double mapped = Math.pow(Math.min(1.0, rms * 7.0), 0.62);
        return (float) Math.max(0.0, Math.min(1.0, mapped));
    }

"""
if marker not in s: raise SystemExit("service send marker missing")
s = s.replace(marker, helper + marker)
p.write_text(s)

# MainActivity
p = root / "app/src/main/java/de/ferdi/jarvis/MainActivity.java"
s = p.read_text()
s = s.replace("    private boolean ttsReady = false;\n", "    private boolean ttsReady = false;\n    private long lastUiAudioLevelAt = 0L;\n")
old = """                ttsReady = true;
                appTts.setLanguage(Locale.GERMANY);
                configureTtsVoice();"""
new = """                ttsReady = true;
                appTts.setLanguage(Locale.GERMANY);
                configureTtsVoice();
                appTts.setOnUtteranceProgressListener(new android.speech.tts.UtteranceProgressListener() {
                    @Override public void onStart(String utteranceId) {
                        lastUiAudioLevelAt = 0L;
                        sendJsEvent("tts_start", utteranceId == null ? "" : utteranceId);
                    }
                    @Override public void onAudioAvailable(String utteranceId, byte[] audio) {
                        long now = System.currentTimeMillis();
                        if (now - lastUiAudioLevelAt < 28) return;
                        lastUiAudioLevelAt = now;
                        sendJsEvent("tts_level", String.format(Locale.US, "%.3f", pcmLevel(audio)));
                    }
                    @Override public void onDone(String utteranceId) {
                        sendJsEvent("tts_level", "0");
                        sendJsEvent("tts_end", utteranceId == null ? "" : utteranceId);
                    }
                    @Override public void onError(String utteranceId) {
                        sendJsEvent("tts_level", "0");
                        sendJsEvent("tts_end", utteranceId == null ? "" : utteranceId);
                    }
                });"""
if old not in s: raise SystemExit("main init target missing")
s = s.replace(old, new)
s = s.replace("        appTts.setSpeechRate(0.90f);\n        appTts.setPitch(0.74f);", "        appTts.setSpeechRate(0.86f);\n        appTts.setPitch(0.68f);")
marker = "    public String getVoiceListJson() {"
helper = """    private float pcmLevel(byte[] audio) {
        if (audio == null || audio.length < 2) return 0f;
        long sum = 0L;
        int samples = 0;
        for (int i = 0; i + 1 < audio.length; i += 2) {
            int lo = audio[i] & 0xff;
            int hi = audio[i + 1];
            short sample = (short) ((hi << 8) | lo);
            int a = Math.abs((int) sample);
            sum += (long) a * a;
            samples++;
        }
        if (samples == 0) return 0f;
        double rms = Math.sqrt((double) sum / samples) / 32768.0;
        double mapped = Math.pow(Math.min(1.0, rms * 7.0), 0.62);
        return (float) Math.max(0.0, Math.min(1.0, mapped));
    }

"""
if marker not in s: raise SystemExit("main list marker missing")
s = s.replace(marker, helper + marker)
p.write_text(s)
print("KITT v3 patch applied")
