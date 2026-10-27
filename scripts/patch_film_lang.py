"""Selector EN/ES dentro del film + sonido activado por defecto. Aplica a las dos homes."""
import re
ROOT = r"D:\Proyectos personales\personal branding\living_book_astro\src\pages"
T = {
  "es": dict(path=ROOT + r"\es\index.astro", on="Sonido: activo", off="Sonido: apagado", mute="Silenciar el film", unmute="Activar el sonido del film", grp="Idioma del film", lang="es"),
  "en": dict(path=ROOT + r"\index.astro", on="Sound: on", off="Sound: off", mute="Mute the film", unmute="Turn the film sound on", grp="Film language", lang="en"),
}
CSS = """.hero .flang{position:absolute;z-index:7;right:var(--m);top:1.2rem;display:flex;border:1px solid rgba(247,248,250,.45);background:rgba(7,8,9,.35)}
.hero .flang button{min-height:44px;min-width:44px;padding:0 .95rem;background:none;border:0;color:rgba(247,248,250,.65);font:500 max(11px,.66rem)/1 var(--grot);letter-spacing:.24em;cursor:pointer;transition:background .3s var(--ease),color .3s var(--ease)}
.hero .flang button:hover,.hero .flang button:focus-visible{color:#fff;background:rgba(0,87,217,.55)}
.hero .flang button[aria-pressed=true]{background:var(--cobalt);color:#fff}
.hero .flang[hidden]{display:none}
"""
def sub(s, a, b):
    assert s.count(a) == 1, (a[:70], s.count(a))
    return s.replace(a, b)
for k, t in T.items():
    s = open(t["path"], encoding="utf-8").read()
    s = sub(s, ".hero .snd[hidden]{display:none}\n", ".hero .snd[hidden]{display:none}\n" + CSS)
    s = sub(s, "@media (prefers-reduced-motion:reduce){.hero .film,.hero .skip,.hero .snd{display:none}}",
               "@media (prefers-reduced-motion:reduce){.hero .film,.hero .skip,.hero .snd,.hero .flang{display:none}}")
    s = re.sub(r'(<button class="snd" id="snd" type="button" aria-pressed=")false(" aria-label=")' + re.escape(t["unmute"]) + '(">)' + re.escape(t["off"]) + '</button>',
               lambda m: m.group(1) + "true" + m.group(2) + t["mute"] + m.group(3) + t["on"] + "</button>"
               + f'\n    <div class="flang" id="flang" role="group" aria-label="{t["grp"]}"><button type="button" data-l="en">EN</button><button type="button" data-l="es">ES</button></div>', s, count=1)
    assert 'id="flang"' in s
    a = s.index("<script is:inline>\n(function(){\n  if (matchMedia('(prefers-reduced-motion: reduce)').matches || !window.gsap) return;")
    b = s.index("})();\n</script>", a) + len("})();\n</script>")
    s = s[:a] + f"""<script is:inline>
(function(){{
  if (matchMedia('(prefers-reduced-motion: reduce)').matches || !window.gsap) return;
  var hero=document.getElementById('hero'), film=document.getElementById('film'), flang=document.getElementById('flang'),
      skip=document.getElementById('skip'), snd=document.getElementById('snd'), au=document.getElementById('fa'), replay=document.getElementById('replay'),
      lang='{t["lang"]}', want=true, armed=false, tl=null, ended=false;
  hero.classList.add('filming');
  /* ui(on): refleja si el audio suena de verdad; want = intencion del visitante (activado por defecto) */
  function ui(on){{ snd.setAttribute('aria-pressed',on); snd.textContent=on?'{t["on"]}':'{t["off"]}';
    snd.setAttribute('aria-label',on?'{t["mute"]}':'{t["unmute"]}'); }}
  function paintLang(){{ [].forEach.call(flang.querySelectorAll('button'),function(b){{ b.setAttribute('aria-pressed',b.dataset.l===lang); }}); }}
  /* los navegadores bloquean el audio sin gesto: si falla, se arma para sonar en el primer toque/tecla */
  function unlock(e){{ if(snd.contains(e.target)) return; disarm(); startAudio(); }}
  function arm(){{ if(armed) return; armed=true; ['pointerup','touchend','keydown'].forEach(function(ev){{ addEventListener(ev,unlock,true); }}); }}
  function disarm(){{ armed=false; ['pointerup','touchend','keydown'].forEach(function(ev){{ removeEventListener(ev,unlock,true); }}); }}
  function startAudio(){{ if(!want||ended) return; au.volume=1; au.currentTime=tl?tl.time():0; var pr=au.play();
    if(pr&&pr.then) pr.then(function(){{ ui(true); }}, function(){{ ui(false); arm(); }}); else ui(true); }}
  function fadeOut(){{ var v={{x:au.volume}}; gsap.to(v,{{x:0,duration:.8,onUpdate:function(){{ au.volume=Math.max(0,v.x); }},onComplete:function(){{ au.pause(); }}}}); }}
  snd.addEventListener('click',function(){{ disarm(); if(want&&!au.paused){{ want=false; ui(false); au.pause(); }} else {{ want=true; startAudio(); }} }});
  function build(){{ tl = buildFilm(film,lang); tl.eventCallback('onComplete', function(){{ setTimeout(finish,500); }}); }}
  /* cambiar de idioma reconstruye el film y sigue por el mismo instante: ambos idiomas duran lo mismo */
  flang.addEventListener('click',function(e){{ var b=e.target.closest('button'); if(!b||ended||b.dataset.l===lang) return;
    lang=b.dataset.l; paintLang(); var at=tl?tl.time():0; if(tl) tl.kill(); build(); tl.seek(at,false); tl.play(); }});
  function finish(){{
    if (ended) return; ended=true; disarm();
    if (tl) tl.pause();
    fadeOut(); snd.hidden=true; flang.hidden=true;
    film.classList.add('done'); skip.hidden=true; replay.hidden=false;
    hero.classList.remove('filming');
    removeEventListener('wheel',bail); removeEventListener('touchmove',bail); removeEventListener('keydown',bail);
  }}
  function bail(e){{ if(e.type==='keydown' && ['ArrowDown','PageDown','Space',' ','End'].indexOf(e.key)<0 && e.code!=='Space') return; finish(); }}
  function play(){{
    ended=false; hero.classList.add('filming'); film.classList.remove('done'); skip.hidden=false; snd.hidden=false; flang.hidden=false; replay.hidden=true; au.pause(); au.currentTime=0;
    scrollTo(0,0); paintLang();
    build(); tl.play(0); startAudio();
    addEventListener('wheel',bail,{{passive:true}}); addEventListener('touchmove',bail,{{passive:true}}); addEventListener('keydown',bail);
  }}
  skip.addEventListener('click',finish);
  replay.addEventListener('click',function(){{ hero.classList.add('filming'); play(); }});
  (document.fonts&&document.fonts.ready?document.fonts.ready:Promise.resolve()).then(play);
}})();
</script>""" + s[b:]
    open(t["path"], "w", encoding="utf-8").write(s)
    print("ok", k)
