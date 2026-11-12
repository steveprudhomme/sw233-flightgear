# 3 · Faire voler les nombres avant de faire voler l’image

Un joli modèle en carton ne connaît pas son poids. JSBSim a besoin d’une autre fiche, **src/SW233/sw233.xml**. Le programme suivant l’écrit. Il ne lit pas le fichier AC3D et ne devine pas la portance d’après les pixels.

**Fichier à écrire :** `dynamique.py`. Colle les blocs de ce fichier dans l’ordre, sans retirer les espaces du début des lignes.

## A · Prépare des étiquettes

XML ressemble à une boîte avec un nom sur le couvercle. `sub` ajoute une petite boîte, `loc` y range x, y et z. `table` écrit des couples de nombres : si la mesure est entre deux lignes, JSBSim peut interpoler. Garde les unités dans la fiche, même si Python ne t’y oblige pas.

<!-- atelier-fichier: dynamique.py -->
```python
from pathlib import Path
import xml.etree.ElementTree as E

root = Path('src/SW233')
def sub(parent, tag, text=None, **attrs):
    node = E.SubElement(parent, tag, attrs)
    if text is not None:
        node.text = str(text)
    return node
def loc(parent, name, xyz):
    n = sub(parent, 'location', name=name, unit='IN')
    for axis, val in zip('xyz', xyz): sub(n, axis, val)
def val(x): return ('value', x)
def prop(x): return ('property', x)
def expr(parent, spec):
    tag, body = spec
    n = sub(parent, tag)
    if isinstance(body, list):
        for s in body: expr(n, s)
    else: n.text = str(body)
    return n
def term(k, *properties): return ('product', [val(k)] + [prop(p) for p in properties])
def table(parent, independent, pairs):
    n = sub(parent, 'table')
    sub(n, 'independentVar', independent, lookup='row')
    sub(n, 'tableData', '\n' + '\n'.join(f'{x} {y}' for x, y in pairs) + '\n')
```

## B · Entre les dimensions et le chargement

Utilise la table des sources de la fiche 1 : surface 219,48 ft², envergure 51 ft. 219,48 ÷ 51 ≈ 4,30 ft donne une vérification de la corde de référence, pas la corde exacte de chaque tranche. Le scénario pèse 610 + 180 + 180 = 970 lb. Les positions en pouces et les inerties viennent du modèle historique, pas d’une mesure de ta photo. Ne change pas des pouces en mètres sans changer l’attribut unit.

<!-- atelier-fichier: dynamique.py -->
```python
fdm = E.Element('fdm_config', name='SW233', version='2.0', release='ALPHA')
fdm.append(E.Comment(' SPDX-License-Identifier: GPL-3.0-only. Original equations; numeric provenance: docs/sources.md. Experimental, not flight validated. '))
head = sub(fdm, 'fileheader')
for t, v in [('author','SW233 contributors'),('filecreationdate','2026-11-02'),('version','0.1.0-dev'),('description','Original SGS 2-33 experimental implementation; historical numeric inputs, not manufacturer coefficients.')]: sub(head,t,v)
metrics = sub(fdm,'metrics')
for tag,v,u in [('wingarea',219.48,'FT2'),('wingspan',51,'FT'),('chord',4.3,'FT')]: sub(metrics,tag,v,unit=u)
loc(metrics,'AERORP',(103.2,0,0))
loc(metrics,'EYEPOINT',(49,0,9))
loc(metrics,'VRP',(0,0,0))
mass = sub(fdm,'mass_balance')
for tag,v in [('ixx',1800),('iyy',850),('izz',1950)]: sub(mass,tag,v,unit='SLUG*FT2')
sub(mass,'emptywt',610,unit='LBS')
loc(mass,'CG',(103.2,0,-6.4))
for name,x in [('front-occupant',43),('rear-occupant',85)]:
    n=sub(mass,'pointmass',name=name)
    sub(n,'weight',180,unit='LBS')
    loc(n,'POINTMASS',(x,0,4))
```

## C · Dis où le sol peut toucher

Un contact de roue a un ressort et un amortisseur : le premier repousse, le second freine les rebonds. Ces réglages sont provisoires. Les roues dessinées et les points de contact sont deux représentations distinctes à raccorder ; changer un rayon dans fabrique.py ne déplace pas automatiquement la physique. Laisse la propulsion vide.

<!-- atelier-fichier: dynamique.py -->
```python
ground=sub(fdm,'ground_reactions')
ground.append(E.Comment(' Prototype contacts. Main wheel combines the two historical main contacts; no wheel brake. '))
for name,kind,xyz,k,c,rolling in [
    ('main-wheel','BOGEY',(108.36,0,-50),1400,280,.05),
    ('nose-skid','STRUCTURE',(33.54,0,-48),1000,1000,.5),
    ('tail','STRUCTURE',(271,0,-20),210,70,.5),
    ('left-wing','STRUCTURE',(103.2,-240,6),210,70,.5),
    ('right-wing','STRUCTURE',(103.2,240,6),210,70,.5)]:
    n=sub(ground,'contact',type=kind,name=name)
    loc(n,'CONTACT',xyz)
    for t,v in [('static_friction',.8),('dynamic_friction',.5),('rolling_friction',rolling)]: sub(n,t,v)
    sub(n,'spring_coeff',k,unit='LBS/FT')
    sub(n,'damping_coeff',c,unit='LBS/FT/SEC')
    if kind=='BOGEY':
        sub(n,'max_steer',0,unit='DEG'); sub(n,'brake_group','NONE'); sub(n,'retractable',0)
sub(fdm,'propulsion')
```

## D · Branche les commandes

Une commande normalisée utilise une petite règle : de −1 à +1 pour le manche, de 0 à 1 pour les aérofreins. `clipto` interdit de sortir de la règle. Des signes contraires pour les deux ailerons les font bouger en sens opposés dans la physique.

<!-- atelier-fichier: dynamique.py -->
```python
fcs=sub(fdm,'flight_control',name='SW233 original controls')
ch=sub(fcs,'channel',name='Pilot controls')
for name,inputs,lo,hi,out in [
    ('pitch-demand',['fcs/elevator-cmd-norm','fcs/pitch-trim-cmd-norm'],-1,1,'fcs/sw233-pitch'),
    ('airbrake-demand',['fcs/speedbrake-cmd-norm'],0,1,'fcs/speedbrake-pos-norm')]:
    n=sub(ch,'summer',name=name)
    for x in inputs: sub(n,'input',x)
    clip=sub(n,'clipto'); sub(clip,'min',lo);sub(clip,'max',hi)
    sub(n,'output',out)
for name,inp,gain,out in [
    ('pitch-surface','fcs/sw233-pitch',0.4014257279586958,'fcs/elevator-pos-rad'),
    ('roll-surface','fcs/aileron-cmd-norm',.35,'fcs/left-aileron-pos-rad'),
    ('opposite-roll-surface','fcs/aileron-cmd-norm',-.35,'fcs/right-aileron-pos-rad'),
    ('yaw-surface','fcs/rudder-cmd-norm',.35,'fcs/rudder-pos-rad')]:
    n=sub(ch,'pure_gain',name=name);sub(n,'input',inp);sub(n,'gain',gain)
    clip=sub(n,'clipto');sub(clip,'min',-abs(gain));sub(clip,'max',abs(gain));sub(n,'output',out)
```

La profondeur utilise maintenant **23 × pi / 180 = 0,4014257279586958 rad** à pleine commande, conformément au débattement nominal du manuel pour 1 040 lb (PDF 21/papier 41). Les coefficients par radian ne changent pas. Voir la [comparaison avant/après](10-profondeur.md).

## E · Calcule ce que fait l’air

La table CL donne la portance selon l’incidence α ; CD décrit la traînée. Les valeurs viennent des [réglages historiques et de leurs limites](../sources.md). Test au crayon : à α = 0 et profondeur nulle, CL = 0,25 avec freins rentrés ; la sortie complète enlève 0,05, donc reste 0,20. Les trois derniers axes font tourner le planeur. La pression dynamique, la surface et un coefficient donnent une force ; pour un moment, ajoute une longueur. Ne confonds pas une lettre majuscule L avec la minuscule l de roulis.

<!-- atelier-fichier: dynamique.py -->
```python
aero=sub(fdm,'aerodynamics')
aero.append(E.Comment(' Coefficients first, dimensional forces/moments second. Angles in radians; rate derivatives use reduced rates. '))
cl=sub(aero,'function',name='aero/sw233/CL')
s=sub(cl,'sum')
table(s,'aero/alpha-rad',[(-.2,-.85),(0,.25),(.21,1.32),(.6,.21)])
expr(s,term(.2,'fcs/elevator-pos-rad'))
expr(s,term(-.05,'fcs/speedbrake-pos-norm'))
cd=sub(aero,'function',name='aero/sw233/CD')
s=sub(cd,'sum')
table(s,'aero/alpha-rad',[(-1.57,1.5),(-.26,.034),(0,.017),(.26,.034),(1.57,1.5)])
expr(s,term(.05,'aero/sw233/CL','aero/sw233/CL'))
expr(s,val(.001));expr(s,term(.01,'fcs/speedbrake-pos-norm'))
expr(s,('product',[val(.024),('abs',[prop('fcs/elevator-pos-rad')])]))
table(s,'aero/beta-rad',[(-1.57,1.23),(-.26,.05),(0,0),(.26,.05),(1.57,1.23)])
equations={
    'CY':[term(-1,'aero/beta-rad')],
    'Cl':[term(-.1,'aero/beta-rad'),term(-.4,'aero/bi2vel','velocities/p-aero-rad_sec'),term(.15,'aero/bi2vel','velocities/r-aero-rad_sec'),term(.07,'fcs/left-aileron-pos-rad'),term(.01,'fcs/rudder-pos-rad')],
    'Cm':[term(-.4,'aero/alpha-rad'),term(-.6,'fcs/elevator-pos-rad'),term(-9,'aero/ci2vel','velocities/q-aero-rad_sec'),term(-12,'aero/ci2vel','aero/alphadot-rad_sec')],
    'Cn':[term(.12,'aero/beta-rad'),term(-.15,'aero/bi2vel','velocities/r-aero-rad_sec'),term(-.03,'fcs/rudder-pos-rad'),term(-.02,'fcs/left-aileron-pos-rad')],
}
for name,terms in equations.items():
    n=sub(aero,'function',name='aero/sw233/'+name);expr(n,terms[0] if len(terms)==1 else ('sum',terms))
for axis,coefficient,length in [('DRAG','CD',None),('SIDE','CY',None),('LIFT','CL',None),('ROLL','Cl','metrics/bw-ft'),('PITCH','Cm','metrics/cbarw-ft'),('YAW','Cn','metrics/bw-ft')]:
    n=sub(aero,'axis',name=axis)
    fun=sub(n,'function',name='aero/sw233/load-'+axis.lower())
    factors=['aero/qbar-psf','metrics/Sw-sqft']
    if length: factors.append(length)
    factors.append('aero/sw233/'+coefficient)
    expr(fun,('product',[prop(p) for p in factors]))
E.indent(fdm,space='    ')
E.ElementTree(fdm).write(root/'sw233.xml',encoding='utf-8',xml_declaration=True)
with (root/'sw233.xml').open('a',encoding='utf-8') as f: f.write('\n')
```

**Enregistre puis lance :** `.\.venv\Scripts\python.exe dynamique.py`. Ouvre *src/SW233/sw233.xml* : cherche les six noms DRAG, SIDE, LIFT, ROLL, PITCH et YAW. Si la maquette est visible mais reste immobile en altitude, commence par vérifier que la fiche de la séance suivante demande bien ce fichier. Ne corrige pas les coefficients pour réparer un mauvais nom de fichier.


**Vérification ultérieure :** la [séance de centrage](08-centrage.md) confronte ces valeurs historiques au manuel, au calcul indépendant et à FlightGear. Les bras de sièges et le datum ne sont pas encore réconciliés ; ne pas interpréter ce modèle comme un chargement validé du vrai appareil.
