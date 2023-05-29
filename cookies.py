import Levenshtein

def find_closest_urls(urls, num_closest=3):
    closest_urls = []
    url_distances = {}
    for i in range(len(urls)):
        for j in range(i + 1, len(urls)):
            distance = Levenshtein.distance(urls[i], urls[j])
            url_distances[(i, j)] = distance

    sorted_distances = sorted(url_distances.items(), key=lambda x: x[1])

    for (i, j), distance in sorted_distances:
        if len(closest_urls) == num_closest:
            break
        if i not in closest_urls:
            closest_urls.append(i)
        if j not in closest_urls:
            closest_urls.append(j)

    return [urls[i] for i in closest_urls]

url_list = [
    'https://montapispriere.com/wp-content/uploads/2023/04/Tapisserie-de-pri-re-argent-e-Ikhwan-rouge-musulman-arabe-duba-Turquie-Pakistan-Inde-tapis-de.jpg_Q90.jpg_-wpp1680949749893-150x150.webp',
    'https://montapispriere.com/wp-content/uploads/2023/04/Tapisserie-de-pri-re-argent-e-Ikhwan-rouge-musulman-arabe-duba-Turquie-Pakistan-Inde-tapis-de.jpg_Q90.jpg_-wpp1680949749893.webp',
    'https://montapispriere.com/wp-content/uploads/2023/04/Tapisserie-de-pri-re-argent-e-Ikhwan-rouge-musulman-arabe-duba-Turquie-Pakistan-Inde-tapis-de.jpg_Q90.jpg_-wpp1680949749893-768x768.webp',
    'https://montapispriere.com/wp-content/uploads/2023/04/Tapis-de-pri-re-Hexagonal-violet-110x77cm-appel-Dodya-pri-re-musulmane-islamique-tat-de-la.jpg_Q90.jpg_-wpp1680950543805-300x225.webp',
    'https://montapispriere.com/wp-content/uploads/2023/03/MON-TAPIS-PRIERE-2.png'
]

closest_urls = find_closest_urls(url_list, num_closest=3)

for url in closest_urls:
    print(url)




