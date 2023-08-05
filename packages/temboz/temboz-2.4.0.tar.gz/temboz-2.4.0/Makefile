VERSION= 	2.2.0
TAR_VERSION=	$(VERSION)
PAGES= 		view error opml feeds temboz_css rules catch_up
DATE:sh=	date +'%Y-%m-%d'

JSMIN=		jsmin

all: changelog

init:
	@if [ `hostname` != "mordac" ]; then true; else echo "Will not run make init on mordac"; false; fi
	-rm -f rss.db
	sqlite3 rss.db < tembozapp/ddl.sql > /dev/null
	temboz --import me.opml
	temboz --refresh

sync:
	-mv feedparser.py feedparser.old
	wget http://feedparser.googlecode.com/svn/trunk/feedparser/feedparser.py

JUI=	spool/jquery-ui/*
sync-js:
	../src/scripts/vcheck --verbose -d --file etc/vcheck
	(cd spool; wget -N http://malsup.github.io/jquery.form.js)
	(cd spool; wget -N https://raw.githubusercontent.com/jeresig/jquery.hotkeys/master/jquery.hotkeys.js)
	(cd spool; wget -N https://unpkg.com/dexie@latest/dist/dexie.js)
	(cd spool; wget -N https://raw.githubusercontent.com/janl/mustache.js/master/mustache.js)

js: $(JUI)/external/jquery/jquery*.js spool/jquery.form.js $(JUI)/jquery-ui.js spool/jquery.hotkeys.meta.js tembozapp/static/specific.js #spool/dexie.js
	cat $^ \
	| $(JSMIN) > tembozapp/static/temboz.js
	cp spool/mustache.js tembozapp/static
	#./temboz --kill
	(svcadm restart temboz:fazal;svcadm restart nginx)
changelog:
	cvs2cl.pl --tags -g -q

cvsdist :=  TAR_VERSION = CVS
cvsdist :=  VERSION = CVS-$(DATE)
cvsdist:: cvsupdate
cvsupdate:
	cvs -q update -A -d -P
cvsdist disttar:: distclean changelog
	-rm -rf temboz-$(VERSION)
	mkdir temboz-$(VERSION)
	-rm -f .*~ *~
	cp README INSTALL NEWS LICENSE UPGRADE ChangeLog temboz *.py temboz-$(VERSION)
	cp tembozapp/ddl.sql me.opml .ht* temboz-$(VERSION)
	cp -r templates images etc tiny_mce static temboz-$(VERSION)
	(cd temboz-$(VERSION); mv param.py param.py.sample; mv transform.py transform.py.sample; find . -name \*.pyc -exec rm {} \;; find . -name \*.pyo -exec rm {} \;; find pages -name \*.py -exec rm {} \;)
	-rm -f temboz-$(VERSION)/etc/.cvsignore
	-rm -rf temboz-$(VERSION)/*/CVS
	# expurgate password
	sed -e 's/auth_dict.=.*/auth_dict = {"login": "password"}/g' param.py > temboz-$(VERSION)/param.py
	gtar zcvf temboz-$(TAR_VERSION).tar.gz temboz-$(VERSION)
	zip -9r temboz-$(TAR_VERSION).zip temboz-$(VERSION)
	-rm -rf temboz-$(VERSION)
	-mv temboz-$(TAR_VERSION).tar.gz $$HOME/web/root/temboz
	-mv temboz-$(TAR_VERSION).zip $$HOME/web/root/temboz

dist: disttar
	-$${EDITOR} ../mylos/data/stories/2004/03/29/temboz.html

opml:
	wget -c https://majid.info/temboz/temboz.opml
	mv temboz.opml me.opml

sdist:
	python setup.py sdist

distclean:
	-rm -f core *.pyc *~ pages/*~ *.old pages/*.py pages/*.pyc ChangeLog*
	-find . -name .\#\* -exec rm {} \;
	-find . -name .\#~ -exec rm {} \;
	-rm -f pages/*~

clean: distclean
	-rm -rf temboz-$(VERSION) temboz-$(VERSION).tar.gz
	-rm -f pages/*.py pages/*.pyc pages/*.pyo pages/*.py.bak *.js

realclean: clean
	-rm -rf rss.db
