import requests

# Define the API endpoint URL
api_url = 'http://127.0.0.1:8000/pin'



Mon_Pilou_Pilou = "https://monpiloupilou.com/pilou-pilou-femme/ensemble-pyjama-chauffant-pilou-pilou/&pin_description=&pin_title=Ensemble%20pyjama%20chauffant%20pilou%20pilou&img_url=https://monpiloupilou.com/wp-content/uploads/2023/05/main-image-2-11-150x150.jpeg&website=mon%20pilou%20pilou&pin_table=Pyjama%20Pilou%20Pilou%20femme"
Applique_Murale = "https://appliquemurale.com/applique-murale-orientable/applique-murale-orientable-americaine/&pin_description=&pin_title=Applique%20murale%20orientable%20am%C3%A9ricaine&img_url=https://appliquemurale.com/wp-content/uploads/2023/04/Applique-murale-industrielle-am-ricaine-noir-argent-E27-lampe-rotative-Long-bras-avec-interrupteur-pour-chevet.jpg_Q90.jpg_-150x150.webp&website=applique%20murale&pin_table=Appliques%20Murales"
robe_princesse = "https://robeprincesse.com/robe-princesse-disney/robe-de-princesse-disney-bleue/&pin_description=&pin_title=Robe%20de%20princesse%20Disney%20bleue&img_url=https://robeprincesse.com/wp-content/uploads/2023/03/O1CN015ZI5ny1bgl2gE9jbE_2866793495-150x150.jpg&website=robe%20princesse&pin_table=Robe%20de%20princesse%20disney"
mon_tapis_priere = "https://montapispriere.com/tapis-de-priere-uni/tapis-de-priere-violet/tapis-de-priere-violet-argente/&pin_description=&pin_title=Tapis%20de%20pri%C3%A8re%20violet%20argent%C3%A9&img_url=https://montapispriere.com/wp-content/uploads/2023/04/Tapis-de-pri-re-Hexagonal-violet-110x77cm-appel-Dodya-pri-re-musulmane-islamique-tat-de-la.jpg_Q90.jpg_-wpp1680950543805-150x150.webp&website=mon%20tapis%20priere&pin_table=Tapis%20de%20Pri%C3%A8re%20Luxe"
esprit_polaire = "https://espritpolaire.com/polaire-femme/cape-polaire-femme/cape-polaire-femme-marron-a-col-en-fourrure/&pin_description=&pin_title=Cape%20polaire%20femme%20marron%20%C3%A0%20col%20en%20fourrure&img_url=https://espritpolaire.com/wp-content/uploads/2023/03/Cardigan-col-en-fourrure-pour-femme-v-tement-d-ext-rieur-ample-et-chaud-manteau-tricot.jpg_Q90.jpg_-4-wpp1679911251822-769x1024.webp&website=esprit%20polaire&pin_table=Cape%20Polaire%20Femme"



Couples_Amoureux = "https://couplesamoureux.com/bijoux-couple/collier-couple/collier-avec-medaillon-en-forme-de-coeur-avec-quatre-feuilles-de-trefle/&pin_description=&pin_title=Collier%20avec%20m%C3%A9daillon%20en%20forme%20de%20c%C5%93ur%20avec%20quatre%20feuilles%20de%20tr%C3%A8fle&img_url=https://couplesamoureux.com/wp-content/uploads/2023/06/Pendentif-cadre-photo-r-tro-en-forme-de-c-ur-quatre-feuilles-Everver-multicouche-bricolage-accessoires.jpg_Q90.jpg_-1-150x150.png&website=couples%20amoureux&pin_table=Collier%20couple"
ma_robe_boheme = "https://marobeboheme.com/robe-champetre/robe-champetre-dentelle/robe-champetre-dentelle-ourlet-rose/&pin_description=&pin_title=Robe%20champ%C3%AAtre%20dentelle%20ourlet%20rose&img_url=https://marobeboheme.com/wp-content/uploads/2023/03/165457976347ad644af6c18ec6f228820bff2d1160_thumbnail_900x-769x1024.webp&website=ma%20robe%20boheme&pin_table=Robe%20champ%C3%AAtre"
Pyjamas_dor = "https://pyjamador.com/pyjama-enfant/pyjama-enfant-garcon/univers-pyjama-enfant-garcon/pyjama-naruto-garcon/pyjama-naruto-garcon-bleu-ensemble/&pin_description=&pin_title=Pyjama%20Naruto%20gar%C3%A7on%20bleu%20ensemble&img_url=https://pyjamador.com/wp-content/uploads/2023/04/Naruto-pyjama-en-coton-pour-enfants-ensemble-2-pi-ces-pour-gar-ons-v-tements-de-150x150.png&website=pyjama%20d%27or&pin_table=Pyjama%20Enfants"
univers_peluche = "https://universpeluche.com/peluche-mangas/peluche-pokemon/peluche-bulbizarre/peluche-bulbizarre-noire-mignonne/&pin_description=&pin_title=Peluche%20Bulbizarre%20noire%20mignonne&img_url=https://universpeluche.com/wp-content/uploads/2023/05/S56b3af75c669442ea99017b3c41e101ct-removebg-preview_large-wpp1684836239169-150x150.jpg&website=Univers%20Peluche&pin_table=Peluche%20Pokemon"
retro_verso = "https://retro-verso.fr/style-annees-60/robes-annees-60/robe-jaune-annee-60-imprime-floral/&pin_description=&pin_title=Robe%20jaune%20ann%C3%A9e%2060%20imprim%C3%A9%20floral&img_url=https://retro-verso.fr/wp-content/uploads/2023/04/JHG-150x150.png&website=retro%20verso&pin_table=Robes%20Ann%C3%A9es%2020"



response = requests.get("http://127.0.0.1:8000/pin?pin_url="+ma_robe_boheme)

# Check the response
if response.status_code == 200:
    print('Pin posted successfully:', response.text)
else:
    print('Failed to post pin. Error:', response.text)
