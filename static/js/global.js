let ai = [{ url: "http://www.ubuntu.com", title:"Ubuntu" },
{ url: "https://community.ubuntu.com/", title:"Community" },
{ url: "https://askubuntu.com", title:"Ask!" },
{ url: "https://developer.ubuntu.com", title:"Developer" },
{ url: "https://design.ubuntu.com", title:"Design" },
{ url: "https://certification.ubuntu.com", title:"Hardware" },
{ url: "https://insights.ubuntu.com", title:"Insights" },
{ url: "https://jujucharms.com", title:"Juju" },
{ url: "http://maas.ubuntu.com", title:"MAAS" },
{ url: "http://partners.ubuntu.com", title:"Partners" },
{ url: "https://buy.ubuntu.com/", title:"Shop" }];

let more = [{ url: "https://help.ubuntu.com", title:"Help" },
{ url: "https://ubuntuforums.org", title:"Forum" },
{ url: "https://www.launchpad.net", title:"Launchpad" },
{ url: "https://shop.canonical.com", title:"Merchandise" },
{ url: "http://www.canonical.com", title:"Canonical" }];

const global = {};

global.setup = function () {
    this.addNav(this.getNav());
    this.trackClicks();
};

global.getNav = function() {
    let begin = '<nav role="navigation" id="nav-global"><div class="nav-global-wrapper"><ul class="nav-global-main">';
    let end = '</ul></div></nav>';
    let mu = '';
    let i = 0;
    while (i < ai.length) {
        mu += '<li><a href="' + ai[i].url + '" ' + this.getActive(ai[i].url) + '>' + ai[i].title + '</a></li>';
        i++;
    }
    i = 0;
    if (more.length > 0) {
    mu += '<li class="more"><a href="#">More <span>&rsaquo;</span></a><ul class="nav-global-more">';
    while (i < more.length) {
        mu += '<li><a href="'+ more[i].url +'">' + more[i].title + '</a></li>'; i++;
    }
    mu += '</ul>';
    }
    return begin + mu + end;
};

global.addNav = function(mu) {
    let gI = 'body';

    if (this.globalPrepend) {
        gI = this.globalPrepend;
    }
    document.querySelector(gI).innerHTML += mu;
    let ml = document.querySelector('#nav-global .more');
    if (ml){
        ml.addEventListener('click',function(e) {
            e.stopPropagation();
            e.preventDefault();
            ml.classList.toggle('open');
            return false;
        });

        ml.querySelector('span').addEventListener('click',function(e) {
            e.preventDefault();
            e.stopPropagation();
        });

        ml.querySelector('ul').addEventListener('click',function(e) {
             e.stopPropagation();
        });
    }

    document.body.addEventListener('click', function(e) {
        let ml = document.querySelector('#nav-global .more');
        if (ml.classList.contains('open')) {
            ml.classList.remove('open');
        }
    });
};

global.getActive = function(link) {
    let fullurl = this.getURL();
    let url = fullurl.substr(0,link.length);

    return (url == link)?'class="active"':'';
};


global.getURL = function(){
    let url = document.URL;
    url = url.replace('https://developer.ubuntu.com','http://developer.ubuntu.com');
    return url;
};

global.trackClicks = function() {
    document.querySelector('#nav-global a').addEventListener('click',function(e) {
        e.preventDefault();
        try {
            _gaq.push(['_trackEvent', 'Global bar click', e.target.get('text'), core.getURL()]);
        } catch(err) {}
        setTimeout(function() {
            document.location.href = e.target.get('href');
        }, 100);
    });
};

if (!global.globalPrepend) {
    global.setup();
}
