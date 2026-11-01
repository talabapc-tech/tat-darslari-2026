    // Jonli sana (hero va muqova)
    (function () {
      var now = new Date();
      var months = ['yanvar','fevral','mart','aprel','may','iyun','iyul','avgust','sentyabr','oktyabr','noyabr','dekabr'];
      var days = ['Yakshanba','Dushanba','Seshanba','Chorshanba','Payshanba','Juma','Shanba'];
      var str = now.getFullYear() + '-yil ' + now.getDate() + '-' + months[now.getMonth()] + ', ' + days[now.getDay()];
      var ids = ['hero-live-date', 'splash-date-text'];
      for (var i = 0; i < ids.length; i++) {
        var el = document.getElementById(ids[i]);
        if (el) el.textContent = str;
      }
    })();

    // Muqovadan darsga o'tish
    function scrollToLesson() {
      var target = document.getElementById('lesson-start');
      if (target) target.scrollIntoView({ behavior: 'smooth' });
    }

    // ======================================================================
    // MATN BILAN O'RASH LABORATORIYASI
    // ======================================================================
    (function () {
      var page = document.getElementById('wl-page');
      if (!page) return;
      var pic = document.getElementById('wl-pic');
      var para = document.getElementById('wl-text');
      var info = document.getElementById('wl-info');
      var MODES = {
        inline: ['Matn qatorida', 'In Line with Text / В тексте',
          'Rasm <b>bitta katta harf</b> kabi qatorda turadi. Word’da rasm qo‘yilganda <b>shu holat o‘z-o‘zidan</b> bo‘ladi. Rasmni sudrab qo‘yib bo‘lmaydi — faqat Enter, probel va tekislash bilan siljitiladi.',
          'Matn orasida kichik belgi yoki sarlavha oldidagi kichik rasm kerak bo‘lsa.', 'Rasm “qimirlamayapti” — talabalar eng ko‘p aynan shu haqda so‘raydi. Yechim: <b>Matn bilan o‘rash</b> ni o‘zgartiring.'],
        square: ['Kvadrat', 'Square / Вокруг рамки',
          'Matn rasmning <b>to‘rtburchak ramkasini</b> aylanib o‘tadi. Rasmni abzats ichida istalgan joyga sudrab qo‘yish mumkin.',
          'Eng ko‘p ishlatiladi: e’lon, byulleten, referat. <b>Bizning amaliy ishda ham shu.</b>', 'Rasm matn bilan juda yaqin turib qolsa — Maket → Matn bilan o‘rash → Boshqa maket parametrlari → masofa (0,3 sm).'],
        tight: ['Qattiq (kontur bo‘yicha)', 'Tight / По контуру',
          'Matn rasmning <b>konturi</b> bo‘ylab o‘tadi. Rasm fonsiz (shaffof) yoki dumaloq bo‘lsa, chiroyli ko‘rinadi.',
          'Dumaloq yoki murakkab shakldagi fonsiz rasmlar uchun.', 'Oddiy to‘rtburchak rasmda “Kvadrat” dan farqi sezilmaydi.'],
        topbottom: ['Tepa va past', 'Top and Bottom / Сверху и снизу',
          'Matn rasm <b>tepasida va pastida</b> turadi, yon tomonlari bo‘sh qoladi. Rasm butun qatorni egallaydi.',
          'Kenglikda katta rasm yoki sxema uchun: matn aralashmasin.', 'Rasm kichik bo‘lsa yon tomonlar bo‘sh qolib, varaq “yirtiq” ko‘rinadi.'],
        behind: ['Matn orqasida', 'Behind Text / За текстом',
          'Rasm matn <b>orqasida</b> turadi, matn rasm ustidan o‘qiladi. Matn joyidan siljimaydi.',
          'Fon rasm, suv belgisi, bezak uchun. Rasmni och qilish kerak (Rasm formati → Tuzatishlar → Yorqinlik).', 'Rasm to‘q bo‘lsa, matn o‘qilmaydi.'],
        front: ['Matn oldida', 'In Front of Text / Перед текстом',
          'Rasm matn <b>ustida</b> turadi va matnni <b>yopib qo‘yadi</b>. Matn joyidan siljimaydi.',
          'Deyarli kerak bo‘lmaydi: faqat rasm ustiga yozuv yoki belgi (masalan, shtamp) qo‘yish uchun.', 'Rasm matnni yopib qo‘yishi mumkin — shuning uchun amaliy ishda tekshirish mezoni bor.']
      };
      function setMode(m) {
        var d = MODES[m];
        page.setAttribute('data-mode', m);
        if (m === 'inline') para.insertBefore(pic, para.firstChild);
        else page.insertBefore(pic, para);
        var btns = document.querySelectorAll('#wl-modes button');
        for (var i = 0; i < btns.length; i++) btns[i].classList.toggle('on', btns[i].getAttribute('data-m') === m);
        info.innerHTML = '<h4>' + d[0] + '</h4><p class="wl-en" style="font-size:0.78rem;color:var(--text-subtle)">' + d[1] + '</p><p>' + d[2] + '</p>' +
          '<p><span class="wl-tag good">Qachon</span>' + d[3] + '</p><p><span class="wl-tag bad">Ehtiyot bo‘ling</span>' + d[4] + '</p>';
      }
      document.getElementById('wl-modes').addEventListener('click', function (e) {
        var b = e.target.closest('button[data-m]');
        if (b) setMode(b.getAttribute('data-m'));
      });
      setMode('inline');
    })();

    // ======================================================================
    // KOLONTITUL LABORATORIYASI
    // ======================================================================
    (function () {
      var wrap = document.getElementById('kl-pages');
      if (!wrap) return;
      var info = document.getElementById('kl-info');
      var mode = 'same', num = 'auto', added = false;
      var pages;
      function reset() { pages = [1, 2, 3, 4]; added = false; document.getElementById('kl-add').disabled = false; }
      function cell(p, total, orig) {
        // p — haqiqiy tartib raqami (1..total); orig — qo'lda yozilgan raqam (null — yangi bet, raqam yo'q)
        var shown, wrong = false;
        if (num === 'auto') shown = String(p);
        else if (orig === null) { shown = '?'; wrong = true; }
        else { shown = String(orig); wrong = (orig !== p); }
        var h = '', f = '', blank = false;
        var head = 'Hamshiralik tarixi';
        if (mode === 'first' && p === 1) blank = true;
        if (mode === 'oddeven') {
          if (p % 2 === 1) { h = '<span></span><span></span><span>Hisobot</span>'; f = '<span></span><span></span><span class="n' + (wrong ? ' bad' : '') + '">' + shown + '</span>'; }
          else { h = '<span>Texnikum</span><span></span><span></span>'; f = '<span class="n' + (wrong ? ' bad' : '') + '">' + shown + '</span><span></span><span></span>'; }
        } else {
          h = '<span></span><span>' + head + '</span><span></span>';
          f = '<span></span><span class="n' + (wrong ? ' bad' : '') + '">' + shown + '</span><span></span>';
        }
        if (blank) { h = ''; f = ''; }
        return '<div class="kl-page' + (blank ? ' titul' : '') + '"><div class="kh">' + h + '</div><div class="kb"></div><div class="kf">' + f + '</div><div class="kn">' + p + '-bet</div></div>';
      }
      function draw() {
        var html = '';
        var list = pages.slice();
        if (added) list.splice(2, 0, null);
        list.forEach(function (orig, i) { html += cell(i + 1, list.length, orig); });
        wrap.innerHTML = html;
        var bm = document.querySelectorAll('#kl-modes button'), bn = document.querySelectorAll('#kl-num button[data-n]');
        for (var i = 0; i < bm.length; i++) bm[i].classList.toggle('on', bm[i].getAttribute('data-m') === mode);
        for (var j = 0; j < bn.length; j++) bn[j].classList.toggle('on', bn[j].getAttribute('data-n') === num);
        var t = {
          same: '<b>Hamma betda bir xil.</b> Bir marta yoziladi — Word uni barcha betlarga qo‘yadi. Referat va oddiy hujjatlar uchun.',
          first: '<b>Birinchi bet alohida.</b> Titul varag‘ida kolontitul va raqam ko‘rinmaydi (<b>Konstruktor › Birinchi sahifa uchun alohida kolontitul</b>). 2-betda raqam «2» bo‘ladi.',
          oddeven: '<b>Toq va juft betlar har xil.</b> Toq betda matn va raqam o‘ngda, juft betda chapda — raqam doim <b>tashqi chetda</b> (<b>Konstruktor › Toq va juft sahifalar uchun har xil</b>).'
        }[mode];
        var n = num === 'auto'
          ? '<p><span class="wl-tag good">Avtomatik raqam</span> Yangi bet qo‘shilsa, raqamlar <b>o‘zi</b> tartibga tushadi.' + (added ? ' Rasmda: 1, 2, <b>3</b> (yangi), 4, 5 — hammasi to‘g‘ri.' : ' «Yangi bet qo‘shish» tugmasini bosib ko‘ring.') + '</p>'
          : '<p><span class="wl-tag bad">Qo‘lda yozilgan raqam</span> ' + (added ? 'Yangi betda raqam yo‘q (<b>?</b>), keyingi betlarda esa eski raqamlar qolib, tartib <b>buzildi</b> (qizil). Bu xato aynan qo‘lda yozilgani uchun.' : 'Hozircha to‘g‘ri ko‘rinadi, lekin «Yangi bet qo‘shish»ni bosing — tartib buziladi.') + '</p>';
        info.innerHTML = '<p>' + t + '</p>' + n;
      }
      document.getElementById('kl-modes').addEventListener('click', function (e) { var b = e.target.closest('button[data-m]'); if (b) { mode = b.getAttribute('data-m'); draw(); } });
      document.getElementById('kl-num').addEventListener('click', function (e) {
        var b = e.target.closest('button');
        if (!b) return;
        if (b.getAttribute('data-n')) { num = b.getAttribute('data-n'); draw(); }
        else if (b.id === 'kl-add') { added = true; b.disabled = true; draw(); }
        else if (b.id === 'kl-reset') { reset(); draw(); }
      });
      reset();
      draw();
    })();

    // ======================================================================
    // "QAYSI VOSITA?" TRENAJYORI
    // ======================================================================
    (function () {
      var ITEMS = /*QUIZ*/[];
      var NAMES = { rasm: 'Rasm', shakl: 'Shakl', kolontitul: 'Kolontitul', wordart: 'WordArt', hech: 'Hech biri' };
      var list = document.getElementById('qz-list');
      if (!list) return;
      var bar = document.getElementById('qz-bar');
      var score = document.getElementById('qz-score');
      var status = document.getElementById('qz-status');
      var answered, right;

      function render() {
        answered = 0; right = 0;
        var html = '';
        ITEMS.forEach(function (it, i) {
          html += '<li class="fx-item" data-i="' + i + '"><div class="qz-text">' + it[0] + '</div><div class="qz-btns">';
          Object.keys(NAMES).forEach(function (k) { html += '<button type="button" data-a="' + k + '">' + NAMES[k] + '</button>'; });
          html += '</div><div class="fx-exp" hidden></div></li>';
        });
        list.innerHTML = html;
        update();
      }
      function update() {
        bar.style.width = Math.round(answered / ITEMS.length * 100) + '%';
        score.textContent = right + ' / ' + ITEMS.length;
        if (answered === ITEMS.length) {
          status.textContent = 'Natija: ' + right + ' / ' + ITEMS.length + (right === ITEMS.length ? ' — a’lo! Vositalarni to‘g‘ri ajratyapsiz.' : ' — xato javoblarning izohini o‘qib chiqing.');
          status.classList.toggle('win', right === ITEMS.length);
        } else {
          status.textContent = 'Javob berilgan: ' + answered + ' ta, to‘g‘ri: ' + right + ' ta';
          status.classList.remove('win');
        }
      }
      list.addEventListener('click', function (e) {
        var btn = e.target.closest('button[data-a]');
        if (!btn) return;
        var li = btn.closest('.fx-item');
        if (li.classList.contains('done')) return;
        var it = ITEMS[+li.getAttribute('data-i')];
        var ok = btn.getAttribute('data-a') === it[1];
        li.classList.add('done', ok ? 'ok' : 'bad');
        btn.classList.add('picked');
        var exp = li.querySelector('.fx-exp');
        exp.innerHTML = '<b>' + (ok ? 'To‘g‘ri.' : 'Noto‘g‘ri.') + '</b> Javob: <b>' + NAMES[it[1]] + '</b>. ' + it[2];
        exp.hidden = false;
        answered++;
        if (ok) right++;
        update();
      });
      document.getElementById('qz-reset').addEventListener('click', render);
      render();
    })();

    // ======================================================================
    // BAHOLASH MEZONLARI JADVALI
    // ======================================================================
    (function () {
      var body = document.getElementById('crit-body');
      if (!body) return;
      var C = /*CRIT*/[];
      body.innerHTML = C.map(function (c, i) {
        return '<tr><td>' + (i + 1) + '</td><td><strong>' + c[0] + '</strong></td><td>' + c[1] + '</td><td>0,5</td></tr>';
      }).join('') + '<tr><td></td><td><strong>Jami</strong></td><td></td><td><strong>5</strong></td></tr>';
    })();

    // ======================================================================
    // NAMUNANI KO'RISH (A4 varaq, oynaga sig'diriladi)
    // ======================================================================
    (function () {
      var modal = document.getElementById('var-modal');
      var body = document.getElementById('var-modal-body');
      var title = document.getElementById('var-modal-title');
      var pdf = document.getElementById('var-modal-pdf');
      if (!modal) return;
      var last = null;

      function fit() {
        var sheet = body.querySelector('.sheet');
        if (!sheet) return;
        var w = body.clientWidth - 8;
        var s = w > 100 ? Math.min(1, w / sheet.offsetWidth) : 1;
        sheet.style.transform = 'scale(' + s + ')';
        body.querySelector('.sheet-holder').style.height = Math.ceil(sheet.offsetHeight * s) + 'px';
      }
      function open(card, btn) {
        var n = btn.getAttribute('data-variant');
        title.textContent = n + '-variant: ' + card.querySelector('h3').textContent + ' — namuna (A4)';
        pdf.setAttribute('href', './tarqatma/' + n + '-variant.pdf');
        body.innerHTML = '<div class="sheet-holder"></div>';
        body.firstChild.appendChild(card.querySelector('template.var-sample').content.cloneNode(true));
        last = btn;
        modal.hidden = false;
        document.body.style.overflow = 'hidden';
        fit();
        var imgs = body.querySelectorAll('img');
        for (var i = 0; i < imgs.length; i++) imgs[i].addEventListener('load', fit);
        document.getElementById('var-modal-close').focus();
      }
      function close() {
        modal.hidden = true;
        document.body.style.overflow = '';
        body.innerHTML = '';
        if (last) last.focus();
      }
      document.addEventListener('click', function (e) {
        var btn = e.target.closest('.var-preview-btn');
        if (btn) { open(btn.closest('.var-card'), btn); return; }
        if (e.target === modal || e.target.closest('#var-modal-close')) close();
      });
      document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !modal.hidden) close(); });
      window.addEventListener('resize', function () { if (!modal.hidden) fit(); });
    })();

    // ======================================================================
    // NAZORAT SAVOLLARI VA JAVOBLARI (faqat o'qituvchi rolida ko'rinadi)
    // ======================================================================
    var QA = /*QA*/[];

    (function () {
      var list = document.getElementById('qa-list');
      if (!list) return;
      var chevron = '<svg class="qa-chevron" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg>';
      var html = '';
      for (var i = 0; i < QA.length; i++) {
        html += '<details class="qa-item"><summary><span class="qa-num">' + (i + 1) + '</span><span class="qa-q">' + QA[i][0] + '</span>' + chevron + '</summary>' +
                '<div class="qa-a"><span class="qa-label">Javob</span>' + QA[i][1] + '</div></details>';
      }
      list.innerHTML = html;
      var el = document.getElementById('qa-count');
      if (el) el.textContent = QA.length + ' ta savol';
    })();

    function toggleAllAnswers() {
      var items = document.querySelectorAll('#qa-list .qa-item');
      var anyClosed = false;
      for (var i = 0; i < items.length; i++) {
        if (!items[i].open) { anyClosed = true; break; }
      }
      for (var j = 0; j < items.length; j++) items[j].open = anyClosed;
      var label = document.querySelector('#qa-toggle span');
      if (label) label.textContent = anyClosed ? 'Barcha javoblarni yopish' : 'Barcha javoblarni ochish';
    }
