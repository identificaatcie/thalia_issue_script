ALL:
	mkdir -p tmp/
	rm -f tmp/*-cred.xml
	python issue.py
	cd tmp && silvia_issuer -i issueScript.xml
	rm -f tmp/*-cred.xml
	
