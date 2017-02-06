Question:
   echo portal-root-war ott-portal-root-war | grep portal-root-war 

   just print portal-root-war,ignore ott-portal-root-war
 
Answer:

   echo portal-root-war ott-portal-root-war| tr ' ' '\n'|grep ^portal-root-war

tr --help
Usage: tr [OPTION]... SET1 [SET2]
Translate, squeeze, and/or delete characters from standard input,
writing to standard output.