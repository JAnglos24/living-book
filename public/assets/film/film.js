/* Film de apertura v3 — primero en inglés, luego en español, cierre "Conoce +".
   Guion base del agente copywriter de Symbios, curado por Claude (primera persona, sin inventar nada).
   Cifras = las de su home. Uso: const tl = buildFilm(rootEl); tl.play()  |  render determinista: tl.seek(t) */
(function(){
  var L = function(t){ return '<span class="ln"><span class="wd">'+t+'</span></span>'; };
  /* *palabra* -> resaltada en cobalto; ~texto~ -> tachado animado */
  var mk = function(t){ return t.replace(/\*(.+?)\*/g,'<span class="hot">$1</span>').replace(/~(.+?)~/g,'<span class="stk">$1<i></i></span>'); };
  var lines = function(a){ return a.map(function(x){ return L(mk(x)); }).join(''); };

  var COPY = {
    en: {
      tag:'EN',
      role:'Transformation Portfolio / Product & Project Management',
      ts:[
        { id:'t1', kick:'From the living book · chapter 4', a:['A refrigerator','doesn’t sell ~a cold box~.'], strike:true, dur:2.9 },
        { id:'t2', a:['It sells preserving,','keeping, reusing,','freezing and *convenience.*'], dur:3.6 },
        { id:'t3', a:['A cigarette pack','doesn’t sell tobacco.'], b:['It sells a','visual promise.'], dur:3.8 },
        { id:'t4', a:['A product doesn’t sell','what it is.'], b:['It sells what','it promises you’ll *feel.*'], dur:4.0 }
      ],
      verbs:[['Portfolio','I lead portfolios.'],['Product','I design product.'],['Feeling','I make it felt.'],['Influence','I lead without imposing.']],
      head:['Horizontal leadership =','<span class="hot">influence with purpose.</span>'],
      cap:'Horizontal tree, with matrix crossings',
      kick5:'What’s behind it',
      h5:['Sixteen years','<span class="hot">of craft, not of title.</span>'],
      labels:['Years of experience','Projects across industries','Ideas still in progress','Worldwide products'],
      h6a:['What’s done well','is felt.'], h6b:'With heart.'
    },
    es: {
      tag:'ES',
      role:'Portafolio de Transformación / Gestión de Producto y Proyectos',
      ts:[
        { id:'t1', kick:'Del libro vivo · capítulo 4', a:['Un refrigerador','no vende ~una caja fría~.'], strike:true, dur:2.9 },
        { id:'t2', a:['Vende conservar,','mantener, reutilizar,','congelar y *comodidad.*'], dur:3.6 },
        { id:'t3', a:['Una cajetilla','no vende tabaco.'], b:['Vende una','promesa visual.'], dur:3.8 },
        { id:'t4', a:['Un producto no vende','lo que es.'], b:['Vende lo que','promete *sentir.*'], dur:4.0 }
      ],
      verbs:[['Portafolio','Dirijo portafolios.'],['Producto','Diseño producto.'],['Sentir','Hago que se sienta.'],['Influir','Lidero sin imponer.']],
      head:['Liderazgo horizontal =','<span class="hot">influencia con propósito.</span>'],
      cap:'Árbol horizontal, con cruces de matriz',
      kick5:'Lo que hay detrás',
      h5:['Dieciséis años','<span class="hot">de oficio, no de cargo.</span>'],
      labels:['Años de experiencia','Proyectos en distintas industrias','Ideas aún en desarrollo','Productos a nivel mundial'],
      h6a:['Lo que se hace bien,','se siente.'], h6b:'Con el corazón.'
    }
  };

  function blockHtml(p){
    var C = COPY[p];
    var ts = C.ts.map(function(s){
      return '<section class="sc '+s.id+'">'+(s.kick?'<p class="kick k">'+s.kick+'</p>':'')+
        '<h2 class="big a">'+lines(s.a)+'</h2>'+(s.b?'<h2 class="big hot b">'+lines(s.b)+'</h2>':'')+'</section>';
    }).join('');
    var cy = C.verbs.map(function(v){ return '<div class="cy"><span class="ln"><b>'+v[0]+'</b></span><span class="sub">'+v[1]+'</span></div>'; }).join('');
    var met = [['16','+'],['50','+'],['inf',''],['10','+']].map(function(m, i){
      return '<div><b '+(m[0]==='inf'?'data-inf="1"':'data-to="'+m[0]+'" data-sfx="'+m[1]+'"')+'>0</b><span>'+C.labels[i]+'</span></div>';
    }).join('');
    return '<div class="blk blk-'+p+'">'+ts+
      '<section class="sc s3"><div class="pan"></div><div class="cyc">'+cy+'</div><div class="idx"><span class="ix">01</span> / 04</div></section>'+
      '<section class="sc s4"><h2 class="big head">'+L(C.head[0])+L(C.head[1])+'</h2>'+
        '<svg class="tree" viewBox="0 0 1000 300" aria-hidden="true">'+
          '<path class="tr" d="M60 150 H300"/>'+
          '<path class="tr" d="M300 150 V40 H560 M300 150 H560 M300 150 V260 H560"/>'+
          '<path class="tr" d="M560 40 H900 M560 150 H900 M560 260 H900"/>'+
          '<path class="cr" d="M700 40 V150 M820 150 V260 M760 40 V260"/>'+
          '<circle class="root" cx="60" cy="150" r="17"/>'+
          '<circle cx="300" cy="150" r="11"/><circle cx="560" cy="40" r="11"/><circle cx="560" cy="150" r="11"/><circle cx="560" cy="260" r="11"/>'+
          '<circle cx="900" cy="40" r="11"/><circle cx="900" cy="150" r="11"/><circle cx="900" cy="260" r="11"/>'+
        '</svg><p class="cap">'+C.cap+'</p></section>'+
      '<section class="sc s5"><p class="kick k">'+C.kick5+'</p><h2 class="big a">'+L(C.h5[0])+L(C.h5[1])+'</h2><div class="met">'+met+'</div></section>'+
      '<section class="sc s6"><h2 class="big serif a">'+L(C.h6a[0])+L(C.h6a[1])+'</h2><h2 class="big serif hot b">'+L('<em>'+C.h6b+'</em>')+'</h2></section>'+
    '</div>';
  }

  var HTML =
    '<div class="ltag" aria-hidden="true"></div>'+
    '<section class="sc s0"><h2 class="big nm">'+L('J. ANGEL')+L('SOSA')+'</h2><p class="kick role">'+COPY.en.role+'</p></section>'+
    blockHtml('en')+blockHtml('es')+
    '<section class="sc s7"><h2 class="big cta">'+L('Conoce <span class="plus">+</span>')+'</h2>'+
      '<div class="lock"><strong>J. ANGEL SOSA</strong><small>'+COPY.es.role+'</small></div></section>'+
    '<div class="bar"></div>';

  var INTRO = 3.2;
  window.FILM_DURATION = 67.9; /* se recalcula al construir la timeline */

  window.buildFilm = function(root){
    root.innerHTML = HTML;
    var $$ = function(s){ return Array.prototype.slice.call(root.querySelectorAll(s)); };
    var m = gsap.timeline({ paused:true, defaults:{ ease:'power3.out' } });
    var OUT = { yPercent:-112, duration:.5, ease:'power3.in', stagger:.04 };
    var show = function(sc, t){ m.set(sc, { visibility:'visible' }, t); }, hide = function(sc, t){ m.set(sc, { visibility:'hidden' }, t); };
    var words = function(sel, t, st){ m.fromTo(sel, { yPercent:112 }, { yPercent:0, duration:.95, ease:'expo.out', stagger: st||.09 }, t); };
    var kick = function(sc, t){ m.fromTo(sc+' .k', { opacity:0, '--kx':0 }, { opacity:1, '--kx':1, duration:.8 }, t); };

    /* S0 · quién escribe */
    show('.s0', 0);
    m.fromTo('.s0 .nm .wd', { yPercent:112 }, { yPercent:0, duration:1.1, ease:'expo.out', stagger:.14 }, .25);
    m.fromTo('.s0 .role', { opacity:0 }, { opacity:1, duration:.8 }, 1.3);
    m.to('.s0 .nm .wd', { yPercent:-112, duration:.5, ease:'power3.in', stagger:.05 }, 2.55);
    m.to('.s0 .role', { opacity:0, duration:.35 }, 2.5);
    hide('.s0', INTRO);

    var t = INTRO;
    ['en','es'].forEach(function(p){
      var C = COPY[p], B = '.blk-'+p+' ';
      var q = function(s){ return s.split(',').map(function(x){ return B + x.trim(); }).join(', '); };
      var langStart = t;
      m.call(function(){ var el = root.querySelector('.ltag'); el.textContent = C.tag; }, null, langStart);
      m.fromTo('.ltag', { opacity:0 }, { opacity:1, duration:.5 }, langStart + .1);

      /* escenas de texto */
      C.ts.forEach(function(s){
        var sc = B + '.' + s.id, end = t + s.dur;
        show(sc, t);
        if (s.kick) kick(sc, t + .1);
        words(sc+' .a .wd', t + .2);
        if (s.strike) m.to(sc+' .stk i', { scaleX:1, duration:.55, ease:'power2.inOut' }, t + 1.55);
        if (s.b) { m.to(sc+' .a', { opacity:.32, duration:.5 }, t + 1.55); words(sc+' .b .wd', t + 1.65); }
        m.to(sc+' .wd', OUT, end - .6);
        if (s.kick) m.to(sc+' .k', { opacity:0, duration:.3 }, end - .65);
        hide(sc, end); t = end;
      });

      /* S3 · panel cobalto y cuatro verbos */
      var s3 = t, S3 = B + '.s3'; show(S3, s3);
      m.to(S3+' .pan', { scaleX:1, duration:.75, ease:'expo.inOut' }, s3);
      var cys = $$(S3+' .cy'), ixs = ['01','02','03','04'];
      m.set(cys, { opacity:0 }, 0);
      cys.forEach(function(cy, i){
        var c = s3 + .65 + i*.98, b = cy.querySelector('b'), sub = cy.querySelector('.sub');
        m.set(cy, { opacity:1 }, c - .01);
        m.fromTo(b, { yPercent:115 }, { yPercent:0, duration:.7, ease:'expo.out' }, c);
        m.fromTo(sub, { opacity:0, y:18 }, { opacity:1, y:0, duration:.55 }, c + .22);
        m.call(function(){ root.querySelector(S3+' .ix').textContent = ixs[i]; }, null, c);
        if (i < cys.length - 1) {
          m.to(b, { yPercent:-115, duration:.4, ease:'power3.in' }, c + .78);
          m.to(sub, { opacity:0, duration:.25 }, c + .72);
          m.set(cy, { opacity:0 }, c + .98);
        }
      });
      var s3e = s3 + 4.6;
      m.to(S3+' .cy:last-child b', { yPercent:-115, duration:.4, ease:'power3.in' }, s3e - 1.0);
      m.to(q('.s3 .cy:last-child .sub, .s3 .idx'), { opacity:0, duration:.3 }, s3e - 1.0);
      m.to(S3+' .pan', { scaleX:0, transformOrigin:'right', duration:.6, ease:'expo.inOut' }, s3e - .6);
      hide(S3, s3e); t = s3e;

      /* S4 · liderazgo horizontal + árbol */
      var s4 = t, S4 = B + '.s4'; show(S4, s4);
      words(S4+' .head .wd', s4 + .1, .14);
      var trs = $$(S4+' path.tr'), crs = $$(S4+' path.cr'), cir = $$(S4+' circle');
      trs.concat(crs).forEach(function(pa){ var len = pa.getTotalLength(); pa.style.strokeDasharray = pa.classList.contains('cr') ? '3 9' : len + ' ' + len; pa.dataset.len = len; });
      cir.forEach(function(c){ c.dataset.r = c.getAttribute('r'); c.setAttribute('r', 0); });
      m.fromTo(trs, { strokeDashoffset:function(i, el){ return el.dataset.len; } }, { strokeDashoffset:0, duration:1, ease:'power2.inOut', stagger:.28 }, s4 + .55);
      m.fromTo(crs, { opacity:0 }, { opacity:1, duration:.7, stagger:.15 }, s4 + 1.8);
      cir.forEach(function(c, i){ m.fromTo(c, { attr:{ r:0 } }, { attr:{ r:+c.dataset.r }, duration:.5, ease:'back.out(2.4)' }, s4 + .65 + i*.07); });
      m.fromTo(S4+' .cap', { opacity:0 }, { opacity:1, duration:.6 }, s4 + 2.05);
      var s4e = s4 + 3.8;
      m.to(S4+' .wd', OUT, s4e - .7); m.to(q('.s4 .tree, .s4 .cap'), { opacity:0, duration:.5 }, s4e - .7);
      hide(S4, s4e); t = s4e;

      /* S5 · cifras */
      var s5 = t, S5 = B + '.s5'; show(S5, s5); kick(S5, s5 + .1);
      words(S5+' .a .wd', s5 + .25, .1);
      m.fromTo(S5+' .met > div', { opacity:0, y:34 }, { opacity:1, y:0, duration:.7, stagger:.1 }, s5 + .8);
      $$(S5+' .met b').forEach(function(b, i){
        if (b.dataset.inf) {
          m.call(function(){ b.textContent = '∞'; }, null, s5 + 1.3 + i*.1);
          m.fromTo(b, { scale:.4 }, { scale:1, duration:.7, ease:'back.out(2)', transformOrigin:'0 60%' }, s5 + 1.3 + i*.1);
        } else {
          var o = { v:0 }, to = +b.dataset.to, sfx = b.dataset.sfx || '';
          m.to(o, { v:to, duration:1.3, ease:'power2.out', onUpdate:function(){ b.textContent = Math.round(o.v) + sfx; } }, s5 + .9 + i*.12);
        }
      });
      var s5e = s5 + 3.6;
      m.to(S5+' .wd', OUT, s5e - .7); m.to(q('.s5 .met, .s5 .k'), { opacity:0, duration:.5 }, s5e - .7);
      hide(S5, s5e); t = s5e;

      /* S6 · lo que se hace bien, se siente */
      var s6 = t, S6 = B + '.s6'; show(S6, s6);
      words(S6+' .a .wd', s6 + .1, .14);
      words(S6+' .b .wd', s6 + 1.5);
      var s6e = s6 + 4.1;
      m.to(S6+' .wd', OUT, s6e - .65); hide(S6, s6e); t = s6e;
    });
    m.to('.ltag', { opacity:0, duration:.4 }, t - .5);

    /* S7 · cierre: Conoce + */
    var s7 = t; show('.s7', s7);
    words('.s7 .cta .wd', s7 + .1);
    m.fromTo('.s7 .plus', { rotation:-180, scale:.2, opacity:0 }, { rotation:0, scale:1, opacity:1, duration:1, ease:'back.out(1.8)', transformOrigin:'50% 55%' }, s7 + .55);
    m.fromTo('.s7 .lock', { opacity:0, y:22 }, { opacity:1, y:0, duration:.9 }, s7 + 1.9);
    t = s7 + 3.9;
    m.to({}, { duration:.01 }, t - .01);
    window.FILM_DURATION = t;
    m.fromTo('.bar', { scaleX:0 }, { scaleX:1, duration:t, ease:'none' }, 0);
    return m;
  };
})();
