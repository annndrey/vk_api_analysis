# -*- coding: utf-8 -*-
import vk_api
import pickle
import pandas as pd 

login, password = 'your@email.com', 'yourpass'
vk_session = vk_api.VkApi(login, password)

try:
    vk_session.auth()
except vk_api.AuthError as error_msg:
    print(error_msg)
vk = vk_session.get_api()



def get_user_ids():
    # найти все скалолазные группы, найти всех пользователей для каждой группы,
    # посмотреть, сколько непересекающихся, сколько пересекающихся
    
    all_groups = ['https://vk.com/skalatoria',
                  'https://vk.com/sport_activator',
                  'https://vk.com/childrensclimbing', 
                  'https://vk.com/xclimbholds',
                  'https://vk.com/staybrut',
                  'https://vk.com/limewall',
                  'https://vk.com/igelsclub',
                  'https://vk.com/bahchisattva',
                  'https://vk.com/fatcatoutdoor',
                  'https://vk.com/scarparussia',
                  'https://vk.com/smileholds',
                  'https://vk.com/public78061409',
                  'https://vk.com/oskalclub',
                  'https://vk.com/lu4su',
                  'https://vk.com/public80247712',
                  'https://vk.com/rzclimbing',
                  'https://vk.com/climblife',
                  'https://vk.com/boulderbrothers',
                  'https://vk.com/challengeclimbing',
                  'https://vk.com/russiaclimbing',
                  'https://vk.com/skalodrom8ka',
                  'https://vk.com/climbingvk',
                  'https://vk.com/gustavclimbingteam',
                  'https://vk.com/elcapitanclimbing',
                  'https://vk.com/russia_madrock',
                  'https://vk.com/uspesnyi_skalolaz',
                  'https://vk.com/x8climb',
                  'https://vk.com/nvkz1950',
                  'https://vk.com/climbing32',
                  'https://vk.com/ks_ekb',
                  'https://vk.com/ropes_n_tops',
                  'https://vk.com/birdsandblokes',
                  'https://vk.com/funclimb',
                  'https://vk.com/lietlahti_park',
                  'https://vk.com/visbor4810',
                  'https://vk.com/lmstn',
                  'https://vk.com/ksgekkon',
                  'https://vk.com/tramontana_climb',
                  'https://vk.com/iskraclimb',
                  'https://vk.com/redpoint_msk',
                  'https://vk.com/gravitacia_club',
                  'https://vk.com/clubvorgol'
                  ]
    
    moscow_climbing = ['https://vk.com/skalatoria',
                  'https://vk.com/sport_activator',
                  'https://vk.com/oskalclub',
                  'https://vk.com/public80247712',
                  'https://vk.com/rzclimbing',
                  'https://vk.com/gustavclimbingteam',
                  'https://vk.com/x8climb',
                  'https://vk.com/lmstn',
                  'https://vk.com/redpoint_msk',
                  'https://vk.com/gravitacia_club',
                  ]
    moscow_gyms = ['https://vk.com/skalatoria',
                  'https://vk.com/rzclimbing',
                  'https://vk.com/lmstn',
                  'https://vk.com/gravitacia_club',
                   'https://vk.com/climbin',
                  ]

    groups_id = [x.replace('https://vk.com/', '') for x in moscow_gyms]
    group_members = {}
    for gr in groups_id:
        offset = 0
        try:
            response = vk.groups.getMembers(group_id=gr)
        except:
            response = vk.groups.getMembers(group_id=gr.replace('public', ''))

        if response['count'] > 1000:
            offsetrange = int(response['count']/1000) + 1
            for r in range(offsetrange):
                try:
                    response = vk.groups.getMembers(group_id=gr, offset=r*1000)
                except:
                    response = vk.groups.getMembers(group_id=gr.replace('public', ''), offset=r*1000)

                if gr in group_members.keys():
                    group_members[gr].extend(response['items'])
                else:
                    group_members[gr] = response['items']
        else:
            group_members[gr] = response['items']

    # в итоге получаем группы и всех ее пользователей
    # и сохранняем
    with (open("groupmembers.p", 'wb')) as f:
        pickle.dump(group_members, f)

def chunk(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i+n]

def analyse_groups():
    groups = pickle.load(open("groupmembers.p", 'rb'))
    for k,v in groups.items():
        print(k, len(groups[k]))

    # DATA
    # group userid username sex bdate city relationrelation 
    df = pd.DataFrame(columns=["group", "id", "name", "lastseen", "sex", "bdate", "city", 'deactivated', 'verified'])
    print(df)
    #sets = map(set, group_members.values())

    for gr in groups.keys():
        offset = 0
        # >>> 
        # вот тут надо делить groups[gr]
        # на куски и кусками по 1000 скармливать
        for inds in chunk(groups[gr], 1000):
            response = vk.users.get(user_ids=",".join(map(str,groups[gr])), fields="lastseen,sex,bdate,city,verified")
            for u in response:
            # update DF
                print(u)
                u['name'] = "%s %s" %(u['first_name'], u['last_name'])
                del u['first_name']
                del u['last_name']
                u['group'] = gr

                if not 'deactivated' in u:
                    if 'last_seen' in u:
                        u['last_seen'] = u['last_seen']['time']
                    if 'city' in u:
                        u['city'] = u['city']['title']
                
                df = df.append(u, ignore_index=True)

    df.to_csv('groups.csv', sep=';')

    #print("TOTAL", sum([len(i) for i in group_members.values()]))
    #common_users = set.intersection(*sets)
    #print("TOTAL COMMON", len(common_users))
    # user_ids не более 1000!
    # поля
    # photo_id, verified, sex, bdate, city, country, home_town, relation
    # has_photo, photo_50, photo_100, photo_200_orig, photo_200, photo_400_orig, 
    # photo_max, photo_max_orig, online, domain, has_mobile, contacts, 
    # site, education, universities, schools, status, last_seen, 
    # followers_count, common_count, occupation, nickname, relatives, relation, 
    # personal, connections, exports, wall_comments, activities, interests, 
    # music, movies, tv, books, games, about, quotes, can_post, 
    # can_see_all_posts, can_see_audio, can_write_private_message, 
    # can_send_friend_request, is_favorite, is_hidden_from_feed, 
    # timezone, screen_name, maiden_name, crop_photo, is_friend, 
    # friend_status, career, military, blacklisted, blacklisted_by_me. 
    #resp = vk.users.get(user_ids=",".join(map(str,common_users)), fields="nickname")
    #print(["%s %s" % (u['first_name'], u['last_name']) for u in resp])
    #for k in group_members.keys():
    #    print(k, len(group_members[k]))

if __name__ == '__main__':
    #get_user_ids()
    analyse_groups()
