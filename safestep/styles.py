"""SafeStep look & feel for Streamlit: design tokens, restyled widgets and CSS-only animations."""
import streamlit as st

CSS = r"""
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Sans+Devanagari:wght@400;500;600;700&display=swap');
:root{--teal:#0F5E4E;--teal-dark:#0B4A3D;--mint:#DCF0EA;--mint-line:#B9DFD4;--amber:#E39A2D;--amber-ink:#8F5A0B;--amber-bg:#FDECD2;--amber-line:#F3D39D;
--red:#B4432F;--red-bg:#FBE6E1;--red-ink:#8C2F1F;--green:#2C7A55;--green-bg:#E3F2EA;--cream:#F8F5EF;--card:#fff;--ink:#16302B;--muted:#56645F;--line:#E3DDD0;--field:#BFB8A8;--sand:#EFE9DE;
--ease:cubic-bezier(.2,.8,.2,1);--r:22px}
html,body,.stApp,button,input,textarea,select,[data-testid="stMarkdownContainer"],[data-testid="stChatInput"] textarea{font-family:"Inter","Noto Sans Devanagari",system-ui,sans-serif!important}
.stApp{background:var(--cream);color:var(--ink)}
[data-testid="stMarkdownContainer"] p,[data-testid="stMarkdownContainer"] li{font-size:1.06rem;line-height:1.55}
h1,h2,h3{color:var(--ink);letter-spacing:-.01em}
header[data-testid="stHeader"]{background:transparent}
[data-testid="stMainMenu"],.stAppDeployButton,[data-testid="stStatusWidget"] svg+div{display:none!important}
.block-container,[data-testid="stMainBlockContainer"]{padding-top:2.2rem;padding-bottom:4rem;max-width:1180px}
section[data-testid="stSidebar"]{background:#fff;border-right:1px solid var(--line)}
section[data-testid="stSidebar"] .block-container,section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"]{padding-top:1.2rem}
.ico{display:inline-block;vertical-align:middle;flex:none}

/* ---- buttons ---- */
.stButton>button,.stFormSubmitButton>button,.stLinkButton>a{border-radius:999px;min-height:3rem;padding:.4rem 1.3rem;font-weight:600;border:1.5px solid var(--teal);color:var(--teal);background:#fff;transition:transform .15s var(--ease),box-shadow .2s,background .2s}
.stButton>button:hover,.stFormSubmitButton>button:hover,.stLinkButton>a:hover{transform:translateY(-2px);box-shadow:0 10px 22px -14px rgba(15,94,78,.6);border-color:var(--teal);color:var(--teal-dark);background:var(--mint)}
.stButton>button:active,.stFormSubmitButton>button:active{transform:scale(.97)}
.stButton>button[kind="primary"],.stFormSubmitButton>button[kind="primary"],.stButton>button[data-testid="stBaseButton-primary"],.stFormSubmitButton>button[data-testid="stBaseButton-primaryFormSubmit"]{background:var(--teal);color:#fff;border-color:var(--teal);box-shadow:0 8px 20px -10px rgba(15,94,78,.7)}
.stButton>button[kind="primary"]:hover,.stButton>button[data-testid="stBaseButton-primary"]:hover,.stFormSubmitButton>button[data-testid="stBaseButton-primaryFormSubmit"]:hover{background:var(--teal-dark);color:#fff}
.stButton>button p,.stFormSubmitButton>button p{font-size:1.02rem}
.st-key-helpbtn button{border-color:var(--amber)!important;color:var(--ink)!important}
.st-key-helpbtn button:hover{background:var(--amber-bg)!important}
.st-key-call1930 a{background:var(--red)!important;color:#fff!important;border-color:var(--red)!important;position:relative;overflow:visible}
.st-key-call1930 a::after{content:"";position:absolute;inset:-5px;border-radius:999px;border:2px solid var(--red);animation:ringpulse 1.6s infinite}
@keyframes ringpulse{from{opacity:.8;transform:scale(.96)}to{opacity:0;transform:scale(1.12)}}

/* let button labels wrap instead of being cut off with "…" */
.stButton button div,.stButton button p,.stButton button span{white-space:normal!important;overflow:visible!important;text-overflow:clip!important}
/* tiles = big card buttons (key starts with tile_) */
[class*="st-key-tile_"] button>div{justify-content:flex-start!important;width:100%}
[class*="st-key-tile_"] button{width:100%;min-height:6.4rem;border-radius:var(--r)!important;border:1px solid var(--line)!important;background:#fff!important;color:var(--ink)!important;justify-content:flex-start;padding:1.1rem 1.4rem!important;text-align:left}
[class*="st-key-tile_"] button:hover{border-color:var(--mint-line)!important;box-shadow:0 16px 32px -20px rgba(22,48,43,.45)!important;transform:translateY(-4px)!important;background:#fff!important}
[class*="st-key-tile_"] button p{text-align:left;color:var(--muted);font-size:.98rem!important;line-height:1.45}
[class*="st-key-tile_"] button p strong{color:var(--ink);font-size:1.18rem;display:inline-block;margin-bottom:.2rem}
[class*="st-key-tile_"] [data-testid="stIconMaterial"]{background:var(--mint);color:var(--teal);border-radius:16px;padding:.7rem;font-size:1.7rem!important;margin-right:.5rem}

/* built-in page navigation */
[data-testid="stSidebarNav"]{padding-top:.4rem}
[data-testid="stSidebarNavLink"]{border-radius:14px;padding:.55rem .8rem;margin:.1rem 0;transition:background .2s,transform .2s}
[data-testid="stSidebarNavLink"] span{font-size:1.02rem!important;color:var(--ink)}
[data-testid="stSidebarNavLink"]:hover{background:var(--cream);transform:translateX(3px)}
[data-testid="stSidebarNavLink"][aria-current="page"]{background:var(--mint);position:relative}
[data-testid="stSidebarNavLink"][aria-current="page"] span{color:var(--teal-dark);font-weight:700}
[data-testid="stSidebarNavLink"][aria-current="page"]::before{content:"";position:absolute;left:0;top:9px;bottom:9px;width:4px;border-radius:4px;background:var(--teal);animation:barIn .35s var(--ease)}
[data-testid="stSidebarNavLink"] [data-testid="stIconMaterial"]{color:var(--muted)}
[data-testid="stSidebarNavLink"][aria-current="page"] [data-testid="stIconMaterial"]{color:var(--teal)}
[data-testid="stLogo"]{height:2.6rem!important;max-width:14rem}
/* sidebar navigation buttons (older layout) */
[class*="st-key-nav_"] button,[class*="st-key-navon_"] button{width:100%;justify-content:flex-start;border:none!important;background:transparent!important;color:var(--ink)!important;border-radius:14px!important;min-height:2.9rem;box-shadow:none!important;font-weight:500}
[class*="st-key-nav_"] button:hover{background:var(--cream)!important;transform:translateX(3px)!important}
[class*="st-key-navon_"] button{background:var(--mint)!important;color:var(--teal-dark)!important;font-weight:700;position:relative}
[class*="st-key-navon_"] button::before{content:"";position:absolute;left:0;top:9px;bottom:9px;width:4px;border-radius:4px;background:var(--teal);animation:barIn .35s var(--ease)}
[class*="st-key-nav_"] [data-testid="stIconMaterial"],[class*="st-key-navon_"] [data-testid="stIconMaterial"]{color:var(--muted)}
[class*="st-key-navon_"] [data-testid="stIconMaterial"]{color:var(--teal)}
@keyframes barIn{from{transform:scaleY(0)}to{transform:scaleY(1)}}

/* choices in quizzes / scenarios (keys choice_*) */
[class*="st-key-choice_"] button{width:100%;justify-content:flex-start;text-align:left;border-radius:26px!important;border:1.5px solid var(--field)!important;color:var(--ink)!important;min-height:3.6rem;padding:.8rem 1.2rem!important}
[class*="st-key-choice_"] button:hover{border-color:var(--teal)!important;background:#FBFEFD!important}
[class*="st-key-choice_"] button p{text-align:left}

/* inputs */
.stTextInput input,.stTextArea textarea{font-size:1.15rem!important;border-radius:16px!important}
.stTextArea textarea{background:var(--cream)}
[data-testid="stTextInputRootElement"],[data-baseweb="textarea"]{border-radius:16px!important}
[data-testid="stWidgetLabel"] p{font-weight:600!important;font-size:1rem!important}

/* chat */
[data-testid="stChatMessage"]{background:#fff;border:1px solid var(--line);border-radius:20px;padding:1rem 1.1rem;animation:msgIn .35s var(--ease) backwards}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]){background:var(--mint);border-color:var(--mint-line)}
@keyframes msgIn{from{opacity:0;transform:translateY(10px) scale(.98)}to{opacity:1;transform:none}}

/* page entrance: every page lives in a container keyed page_<name>, so switching page re-plays this */
[class*="st-key-page_"]>div>[data-testid="stElementContainer"],[class*="st-key-page_"]>div>[data-testid="stHorizontalBlock"],[class*="st-key-page_"]>div>[data-testid="stLayoutWrapper"]{animation:rise .5s var(--ease) backwards}
[class*="st-key-page_"]>div>*:nth-child(2){animation-delay:.05s}[class*="st-key-page_"]>div>*:nth-child(3){animation-delay:.1s}[class*="st-key-page_"]>div>*:nth-child(4){animation-delay:.15s}
[class*="st-key-page_"]>div>*:nth-child(5){animation-delay:.2s}[class*="st-key-page_"]>div>*:nth-child(6){animation-delay:.25s}[class*="st-key-page_"]>div>*:nth-child(n+7){animation-delay:.3s}
@keyframes rise{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}

/* ---- HTML blocks ---- */
.ss-title h1{font-size:2.1rem;margin:0;padding:0}.ss-title p{color:var(--muted);margin:.25rem 0 0;font-size:1.05rem}
.brand{display:flex;align-items:center;gap:.55rem;font-weight:700;font-size:1.45rem;color:var(--ink);padding:.2rem .4rem 1rem}
.card{background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:1.4rem 1.6rem}
.eyebrow{font-size:.8rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--teal-dark)}
.deva .eyebrow{letter-spacing:0;text-transform:none;font-size:.9rem}
.muted{color:var(--muted)}
.ibox{width:3.6rem;height:3.6rem;border-radius:18px;display:grid;place-items:center;flex:none;background:var(--mint);color:var(--teal)}
.ibox.amber{background:var(--amber-bg);color:var(--amber-ink)}.ibox.red{background:var(--red-bg);color:var(--red)}
.pill{display:inline-flex;align-items:center;gap:.35rem;border-radius:999px;padding:.28rem .8rem;font-size:.85rem;font-weight:600}
.pill.green{background:var(--green-bg);color:var(--green)}.pill.amber{background:var(--amber-bg);color:var(--amber-ink)}.pill.sand{background:var(--sand);color:var(--muted)}.pill.red{background:var(--red-bg);color:var(--red-ink)}
.row{display:flex;gap:1rem;align-items:center;flex-wrap:wrap}
.streak{background:var(--amber-bg);border:1px solid var(--amber-line);border-radius:var(--r);padding:1.5rem 1.7rem;display:flex;gap:1.2rem;align-items:center}
.streak h2{font-size:1.5rem;margin:0 0 .4rem;display:flex;gap:.8rem;align-items:center}
.week{display:flex;gap:.8rem;flex-wrap:wrap;margin-top:.8rem}
.day{display:grid;gap:.25rem;justify-items:center;font-size:.85rem;color:var(--muted)}
.day i{width:1.9rem;height:1.9rem;border-radius:50%;border:2px solid var(--amber-line);background:#fff;display:block}
.day.on i{background:var(--teal);border-color:var(--teal);animation:popDot .5s var(--ease) backwards;animation-delay:calc(var(--d)*90ms + 200ms)}
.day.today{color:var(--ink);font-weight:700}
@keyframes popDot{0%{transform:scale(.3)}70%{transform:scale(1.15)}100%{transform:scale(1)}}
.ring{width:6.4rem;height:6.4rem;flex:none;position:relative;display:grid;place-items:center;text-align:center}
.ring svg{position:absolute;inset:0;transform:rotate(-90deg)}
.ring circle{fill:none;stroke-width:9}.ring .bg{stroke:#fff}
.ring .fg{stroke:var(--teal);stroke-linecap:round;stroke-dasharray:263.9;stroke-dashoffset:263.9;animation:ringDraw 1.4s var(--ease) .2s forwards}
@keyframes ringDraw{to{stroke-dashoffset:var(--off)}}
.ring b{font-size:1.5rem;display:block;line-height:1}.ring small{font-size:.7rem;color:var(--muted)}
.wotd{background:var(--mint);border:1px solid var(--mint-line);border-radius:var(--r);padding:1.4rem 1.5rem;height:100%}
.wotd h3{font-size:1.8rem;margin:.3rem 0}
.banner{background:var(--teal);color:#fff;border-radius:var(--r);padding:1.3rem 1.6rem;display:flex;gap:1rem;align-items:center}
.banner .ibox{background:var(--teal-dark);color:#fff}.banner p{color:var(--mint);margin:0}.banner b{font-size:1.15rem}
.alert{background:var(--red-bg);border:1px solid #F1C4B9;border-radius:var(--r);padding:1rem 1.3rem;display:flex;gap:1rem;align-items:center}
.alert .ibox{background:#fff;color:var(--red);border-radius:50%;width:3rem;height:3rem}
.alert .ibox .ico{animation:bell 1.6s ease-in-out infinite;transform-origin:50% 10%}
@keyframes bell{0%,60%,100%{transform:rotate(0)}10%,30%{transform:rotate(14deg)}20%,40%{transform:rotate(-14deg)}}
.tipcard{background:var(--amber-bg);border-radius:16px;padding:.9rem 1rem;font-size:.95rem;animation:rise .4s var(--ease)}
.tipcard b{color:var(--amber-ink);display:flex;gap:.4rem;align-items:center;margin-bottom:.25rem}
.me{display:flex;align-items:center;gap:.7rem;padding:.6rem .3rem}
.avatar{width:2.6rem;height:2.6rem;border-radius:50%;background:var(--teal);color:#fff;display:grid;place-items:center;font-weight:700;flex:none}
.me small{display:block;color:var(--muted)}
/* checker */
.how{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1rem}
.how div{background:var(--sand);border-radius:20px;padding:1.2rem}
.num{width:2.2rem;height:2.2rem;border-radius:50%;background:#fff;display:grid;place-items:center;font-weight:700;color:var(--teal);margin-bottom:.5rem}
.verdict{background:#fff;border:1px solid var(--line);border-left:6px solid var(--red);border-radius:var(--r);padding:1.4rem 1.6rem;display:grid;gap:1rem;animation:rise .5s var(--ease) backwards}
.verdict.mid{border-left-color:var(--amber)}.verdict.low{border-left-color:var(--green)}
.verdict h2{margin:0;font-size:1.75rem;color:var(--red-ink)}.verdict.mid h2{color:var(--amber-ink)}.verdict.low h2{color:var(--green)}
.meter{display:grid;gap:.35rem}
.track{position:relative;height:14px;border-radius:7px;background:linear-gradient(90deg,#3C8C63,#E39A2D 55%,#B4432F)}
.knob{position:absolute;top:50%;left:0;width:28px;height:28px;border-radius:50%;background:var(--ink);border:4px solid #fff;box-shadow:0 2px 8px rgba(0,0,0,.25);transform:translate(-50%,-50%);animation:knob 1.1s var(--ease) .25s forwards}
@keyframes knob{to{left:var(--pos)}}
.ends{display:flex;justify-content:space-between;font-size:.85rem;font-weight:600}.ends span:first-child{color:var(--green)}.ends span:last-child{color:var(--red)}
.flag{display:flex;gap:.7rem;align-items:flex-start;animation:rise .45s var(--ease) backwards;animation-delay:calc(var(--i)*140ms + 300ms)}
.flag .ico{color:var(--red);margin-top:.15rem}.flag b{display:block}
.quote{background:var(--cream);border-radius:16px;padding:.9rem 1.1rem;line-height:1.75;word-break:break-word}
.quote mark{background:var(--red-bg);color:var(--red-ink);border-radius:6px;padding:.05em .25em;font-weight:600;box-shadow:inset 0 -2px 0 var(--red);animation:markIn .6s var(--ease) backwards;animation-delay:calc(var(--i,0)*140ms + 350ms)}
@keyframes markIn{from{background:transparent;box-shadow:none;color:inherit}}
.next{background:var(--mint);border:1px solid var(--mint-line);border-radius:var(--r);padding:1.2rem 1.5rem;display:flex;gap:1rem;align-items:center;animation:rise .5s var(--ease) .6s backwards}
.next h3{margin:.2rem 0 0;font-size:1.2rem}
.lab{font-size:.78rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.deva .lab{letter-spacing:0;text-transform:none;font-size:.9rem}
/* words */
.term{background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:1.2rem 1.3rem;min-height:12.5rem;display:flex;flex-direction:column;gap:.35rem;transition:transform .2s var(--ease),box-shadow .2s;animation:rise .45s var(--ease) backwards;animation-delay:calc(var(--i)*60ms)}
.term:hover{transform:translateY(-4px) rotate(-.4deg);box-shadow:0 16px 32px -18px rgba(22,48,43,.4)}
.term h3{margin:0;font-size:1.2rem}.term .top{display:flex;justify-content:space-between;align-items:flex-start}
.box{border-radius:16px;padding:.9rem 1.05rem;display:flex;gap:.7rem;align-items:flex-start;margin:.25rem 0 .7rem}
.box.ex{background:var(--cream);border-left:4px solid var(--amber-line)}.box.tip{background:var(--mint)}.box.tip .ico{color:var(--teal)}.box.rem{background:var(--amber-bg);font-weight:600}.box.rem .ico{color:var(--amber-ink)}
.dots{display:flex;gap:.45rem;align-items:center}
.dots i{width:12px;height:12px;border-radius:50%;border:1.5px solid var(--field);background:#fff;display:block;transition:all .3s}
.dots i.ans{background:var(--teal);border-color:var(--teal)}.dots i.cur{border:2.5px solid var(--teal);transform:scale(1.2)}
.qprog{height:6px;border-radius:3px;background:var(--sand);overflow:hidden;margin:.4rem 0 .8rem}
.qprog i{display:block;height:100%;background:var(--teal);border-radius:3px;animation:grow .6s var(--ease) backwards}
@keyframes grow{from{width:0}}
.qtype{background:var(--sand);color:var(--teal-dark);border-radius:999px;padding:.28rem .8rem;font-size:.85rem;font-weight:600;display:inline-block;margin-bottom:.5rem}
.fb{display:flex;gap:.8rem;align-items:flex-start;border-radius:16px;padding:1rem 1.2rem;border-left:6px solid;animation:drop .4s var(--ease) backwards;margin:.4rem 0}
.fb.ok{background:var(--green-bg);border-color:var(--green)}.fb.ok b{color:var(--green)}.fb.ok .ico{color:var(--green)}
.fb.no{background:var(--amber-bg);border-color:var(--amber)}.fb.no b{color:var(--amber-ink)}.fb.no .ico{color:var(--amber-ink)}
.fb b{display:block;font-size:1.08rem}
.fb.ok{animation:drop .4s var(--ease) backwards,okPulse .8s var(--ease) .1s}
@keyframes okPulse{0%{box-shadow:0 0 0 0 rgba(44,122,85,.45)}100%{box-shadow:0 0 0 16px rgba(44,122,85,0)}}
.fb.no{animation:drop .4s var(--ease) backwards,wobble .45s ease .1s}
@keyframes wobble{0%,100%{transform:translateX(0)}20%{transform:translateX(-7px)}40%{transform:translateX(6px)}60%{transform:translateX(-3px)}80%{transform:translateX(2px)}}
@keyframes drop{from{opacity:0;transform:translateY(-8px)}to{opacity:1;transform:none}}
.picked{border-radius:26px;padding:.9rem 1.2rem;font-weight:600;display:flex;gap:.8rem;align-items:center;margin:.3rem 0;border:2px solid}
.picked.correct{background:var(--green-bg);border-color:var(--green)}.picked.wrong{background:var(--amber-bg);border-color:var(--amber)}.picked.safer{background:var(--mint);border-color:var(--teal)}.picked.dim{opacity:.5;border:1.5px solid var(--field);background:#fff}
.picked .L{font-weight:700;color:var(--teal)}
.done{background:var(--green-bg);border-radius:20px;padding:1.6rem;display:grid;gap:.6rem;justify-items:center;text-align:center;animation:popIn .4s var(--ease)}
@keyframes popIn{from{opacity:0;transform:translateY(18px) scale(.97)}to{opacity:1;transform:none}}
/* scenarios */
.situation{background:var(--mint);border:1px solid var(--mint-line);border-radius:var(--r);padding:1.5rem 1.7rem;display:flex;gap:1.2rem;align-items:flex-start}
.situation .ibox{background:#fff;border-radius:50%}
.situation p{font-weight:600;font-size:1.25rem!important;line-height:1.5;margin:.3rem 0 0}
.badge-won{display:flex;gap:1rem;align-items:center;background:var(--amber-bg);border:1px solid var(--amber-line);border-radius:20px;padding:1.1rem 1.3rem;animation:popIn .5s var(--ease) .2s backwards}
.medal{width:3.8rem;height:3.8rem;border-radius:50%;background:#fff;border:2px solid var(--amber);display:grid;place-items:center;color:var(--amber-ink);flex:none;animation:spinIn .8s var(--ease) .3s backwards}
@keyframes spinIn{from{transform:rotate(-180deg) scale(.3)}to{transform:none}}
.medals{display:grid;grid-template-columns:repeat(auto-fill,minmax(6rem,1fr));gap:.9rem}
.medals div{display:grid;justify-items:center;gap:.35rem;text-align:center;font-size:.85rem;font-weight:600}
.medals .medal{animation-delay:calc(var(--i)*120ms + 200ms)}
.medals .off .medal{border-color:var(--line);color:var(--field);background:var(--cream);animation:none}
.medals .off{color:var(--muted);font-weight:500}
.safer-box{display:flex;gap:1rem;align-items:center;border:1.5px solid var(--teal);border-radius:18px;padding:1rem 1.2rem;background:#fff;animation:drop .4s var(--ease) backwards}
/* recap */
@property --num{syntax:'<integer>';initial-value:0;inherits:false}
.count{animation:count 1.2s var(--ease) forwards;counter-reset:num var(--num)}
.count::after{content:counter(num)}
@keyframes count{to{--num:var(--to)}}
.stat{background:#fff;border:1px solid var(--line);border-radius:20px;padding:1.1rem 1.2rem;display:flex;gap:.9rem;align-items:center}
.stat b{font-size:2rem;line-height:1;display:block;color:var(--teal);font-variant-numeric:tabular-nums}
.stat.amber b{color:var(--amber-ink)}
.dyk{background:var(--amber-bg);border:1px solid var(--amber-line);border-radius:var(--r);padding:1.3rem 1.4rem}
/* help */
.step{background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:1.3rem 1.4rem;min-height:15rem;transition:background .3s,border-color .3s}
.step.isdone{background:var(--green-bg);border-color:#BFE0CE}
.bignum{width:3rem;height:3rem;border-radius:50%;display:grid;place-items:center;font-weight:700;font-size:1.3rem;background:var(--mint);color:var(--teal)}
.bignum.r{background:var(--red-bg);color:var(--red-ink)}
.step h3{margin:.7rem 0 .3rem;font-size:1.3rem}
/* login hero */
.hero{background:var(--teal);color:#fff;border-radius:28px;padding:2.4rem 2.4rem;position:relative;overflow:hidden;min-height:34rem;display:flex;flex-direction:column;gap:1.1rem}
.hero::before,.hero::after{content:"";position:absolute;border-radius:50%;filter:blur(40px);pointer-events:none}
.hero::before{width:300px;height:300px;background:#1F8A72;opacity:.5;top:-80px;right:-90px;animation:float 9s ease-in-out infinite}
.hero::after{width:220px;height:220px;background:var(--amber);opacity:.18;bottom:-80px;left:-60px;animation:float 11s ease-in-out infinite reverse}
.hero>*{position:relative;z-index:1}
@keyframes float{0%,100%{transform:translate(0,0)}50%{transform:translate(-30px,40px)}}
.hero h1{color:#fff!important;font-size:2.7rem!important;line-height:1.1!important;margin:1rem 0 0!important}
.hero p{color:var(--mint)!important;font-size:1.15rem!important}
.hero ul{list-style:none;padding:0;margin:0;display:grid;gap:.6rem}.hero li{display:flex;gap:.6rem;align-items:center}
.demo-sms{margin-top:auto;background:var(--teal-dark);border-radius:20px;padding:1.1rem 1.2rem;display:grid;gap:.6rem}
.demo-sms .bubble{background:#fff;color:var(--ink);border-radius:16px 16px 16px 4px;padding:.8rem 1rem;font-size:.95rem;overflow:hidden;white-space:nowrap;width:0;animation:type 2.4s steps(60) .3s forwards}
@keyframes type{to{width:100%;white-space:normal}}
.demo-sms .tag{display:inline-flex;gap:.4rem;align-items:center;background:var(--red-bg);color:var(--red-ink);border-radius:999px;padding:.22rem .8rem;font-size:.82rem;font-weight:600;width:max-content;opacity:0;animation:tagIn .5s var(--ease) forwards}
.demo-sms .tag:nth-of-type(1){animation-delay:2.8s}.demo-sms .tag:nth-of-type(2){animation-delay:3.4s}.demo-sms .tag:nth-of-type(3){animation-delay:4s}
@keyframes tagIn{from{opacity:0;transform:translateX(-10px)}to{opacity:1;transform:none}}
.stamp{justify-self:end;border:2.5px solid #FFB4A3;color:#FFD5CB;border-radius:10px;padding:.2rem .7rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase;font-size:.82rem;opacity:0;animation:stamp .4s var(--ease) 4.6s forwards}
@keyframes stamp{from{opacity:0;transform:rotate(-8deg) scale(1.8)}to{opacity:1;transform:rotate(-8deg)}}
.stepbar{display:flex;gap:.6rem;align-items:center;font-weight:600;color:var(--muted);font-size:.92rem}
.stepbar span{display:flex;gap:4px}.stepbar i{width:26px;height:5px;border-radius:3px;background:var(--line);display:block}.stepbar i.on{background:var(--teal)}
.success{display:grid;justify-items:center;gap:.6rem;text-align:center;padding:1rem 0;animation:popIn .4s var(--ease)}
.success circle{stroke:var(--green);stroke-width:3;fill:var(--green-bg);stroke-dasharray:160;stroke-dashoffset:160;animation:draw .6s var(--ease) forwards}
.success path{stroke:var(--green);stroke-width:4;fill:none;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:40;stroke-dashoffset:40;animation:draw .4s var(--ease) .45s forwards}
@keyframes draw{to{stroke-dashoffset:0}}
/* dialogs */
div[role="dialog"]{border-radius:28px!important}
@media (max-width:760px){.how{grid-template-columns:1fr}.hero{min-height:auto;padding:1.6rem}.hero h1{font-size:2rem!important}.demo-sms{display:none}.streak{flex-wrap:wrap}.ss-title h1{font-size:1.7rem}}
@media (prefers-reduced-motion:reduce){*,*::before,*::after{animation-duration:.01ms!important;animation-delay:0ms!important;transition-duration:.01ms!important}}
"""


def inject(scale: float, deva: bool) -> None:
    font = '"Noto Sans Devanagari","Inter",system-ui,sans-serif' if deva else '"Inter","Noto Sans Devanagari",system-ui,sans-serif'
    css = "\n".join(l for l in CSS.splitlines() if l.strip())
    st.markdown(f"<style>{css}\nhtml{{font-size:{16 * scale:.2f}px}}\n"
            f"html,body,.stApp,button,input,textarea,[data-testid=\"stMarkdownContainer\"]{{font-family:{font}!important}}"
            + (".eyebrow,.lab{letter-spacing:0!important;text-transform:none!important;font-size:.92rem!important}" if deva else "") + "</style>", unsafe_allow_html=True)
