# -*- coding:UTF-8 -*-
import requests
from multiprocessing import Pool
import time
import treelib
import os

url_base_1 = 'https://api.github.com/users/'
function_url_follower = '/followers'
function_url_repo = '/repos'
# token = "b358a2a08900b4b8c5134e817546ec4c89b76696"
user = "dRl-l"

initial_node = 0
usr_tree = treelib.Tree()
usr_result = []
repo_result = []
repo_list_merge = []

file_token = open(r'token.txt', 'r')
token = file_token.read()

# ===========================================
# function 01  GITHUB API get Function   (username) (first url) (second url)-> (json)
# FOLDED (used in repo search and follower search)


def get_json_from_username(usr, url1, url2):
    url = url1 + str(usr) + url2
    r = requests.get(url,auth=(user,token))  # response
    info_json = r.json()                     # json -> list of json
    return info_json


# Example
"""
print get_follower_from_username("toohuman")
>>> return
[{u'following_url': u'https://api.github.com/users/nathanmelenbrink/following{/other_user}', 
u'events_url': u'https://api.github.com/users/nathanmelenbrink/events{/privacy}', 
u'organizations_url': u'https://api.github.com/users/nathanmelenbrink/orgs', 
u'url': u'https://api.github.com/users/nathanmelenbrink', 
u'gists_url': u'https://api.github.com/users/nathanmelenbrink/gists{/gist_id}', 
u'html_url': u'https://github.com/nathanmelenbrink', 
u'subscriptions_url': u'https://api.github.com/users/nathanmelenbrink/subscriptions', 
u'avatar_url': u'https://avatars1.githubusercontent.com/u/10489972?v=4', 
u'repos_url': u'https://api.github.com/users/nathanmelenbrink/repos', 
u'received_events_url': u'https://api.github.com/users/nathanmelenbrink/received_events', 
u'gravatar_id': u'', 
u'starred_url': u'https://api.github.com/users/nathanmelenbrink/starred{/owner}{/repo}', 
u'site_admin': False, 
u'login': u'nathanmelenbrink', 
u'type': u'User', 
u'id': 10489972, 
u'followers_url': u'https://api.github.com/users/nathanmelenbrink/followers'}, 
{u'following_url': u'https://api.github.com/users/tomekent/following{/other_user}', 
u'events_url': u'https://api.github.com/users/tomekent/events{/privacy}', 
u'organizations_url': u'https://api.github.com/users/tomekent/orgs', 
u'url': u'https://api.github.com/users/tomekent', 
u'gists_url': u'https://api.github.com/users/tomekent/gists{/gist_id}', 
u'html_url': u'https://github.com/tomekent', 
u'subscriptions_url': u'https://api.github.com/users/tomekent/subscriptions', 
u'avatar_url': u'https://avatars3.githubusercontent.com/u/2988777?v=4', 
u'repos_url': u'https://api.github.com/users/tomekent/repos', 
u'received_events_url': u'https://api.github.com/users/tomekent/received_events', 
u'gravatar_id': u'', 
u'starred_url': u'https://api.github.com/users/tomekent/starred{/owner}{/repo}', 
u'site_admin': False, 
u'login': u'tomekent', 
u'type': u'User', 
u'id': 2988777, 
u'followers_url': u'https://api.github.com/users/tomekent/followers'}]"""

# ===========================================
# function 02  find "looking for" from JSON data   (json) -> (list)
# FOLDED (used in repo search and follower search)
# follower: 'login'
# repo: 'full_name'


def get_info_from_json(l, looking_for):
    result_list = []
    for i in l:
        new_str = str(i[looking_for])
        result_list.append(new_str)
    return result_list

# ===========================================
# function 03  username -> followers name (list)
# (function 01 + function 02)


def followers(usr):
    follower_list = get_info_from_json(get_json_from_username(usr, url_base_1, function_url_follower), 'login')
    return follower_list


# ===========================================
# function 04  username -> repo name (list)
# (function 01 + function 02)


def repos(usr):
    j_s_o_n = get_json_from_username(usr, url_base_1, function_url_repo)
    repo_list = get_info_from_json(j_s_o_n, 'full_name')
    time_list = get_info_from_json(j_s_o_n, "created_at")
    update_list = get_info_from_json(j_s_o_n, "updated_at")
    count = 0
    new_list = []
    for a in time_list:
        if a != update_list[count] and ((a[0:4] == "2016" and int(a[5:7]) > 9) or (a[0:4] == "2017" and int(a[5:7]) < 9)):
            new_list.append(repo_list[count])
            count = count + 1
        else:
            count = count + 1
    return new_list


# USER TREE GENERATE FUNCTION

def generate_usr_tree(usr,stop):
    global initial_node
    global usr_tree
    if initial_node >= stop:
        return
    usr=str(usr)
    try:
        usr_tree.create_node(usr, usr)
    except treelib.exceptions.DuplicatedNodeIdError:
        pass
    current_follower = followers(usr)
    follower_length = len(current_follower)
    if follower_length == 0:
        pass
    elif follower_length > 0:
        while initial_node < stop:
            for i in current_follower:
                try:
                    if initial_node < stop:
                        usr_tree.create_node(i, i, parent=usr)
                        initial_node = initial_node + 1
                        print (time.clock(), "捕获用户", initial_node, i)
                    elif initial_node >= stop:
                        break
                except treelib.exceptions.DuplicatedNodeIdError:
                    pass
            children_node = usr_tree.children(usr)
            # >> children_node <<  <type 'list'>
            # [Node(tag=nathanmelenbrink, identifier=nathanmelenbrink, data=None)]
            children = []
            for i in children_node:
                children.append(i.tag)
                # print time.clock(), "loop1"
            for i in children:
                generate_usr_tree(i, stop)  # Natural Recursion
                # print time.clock(), "loop2"
                # print len(children)


# ===========================================
# function MAIN


def main(starting_node, node_num):
    global initial_node
    global usr_tree
    global usr_result
    global repo_result
    global repo_list_merge
    t1 = time.clock()                           # clock start
    f0 = open(r'log.txt', 'a')                  # start logging file
    f0.truncate()                               # empty logging file

    print ("===== Stage 1 Launched ")
    f0.write("1")
    generate_usr_tree(starting_node, node_num)  # generate a tree
    usr_tree.show()                             # print the tree structure

    print ("===== Stage 2 Launched ")
    f0.write("2")
    for i in usr_tree.expand_tree():
        usr_result.append(i)                    # Traverse, Generate a list of the user (RESULT)

    print ("===== Stage 3 Launched ")
    f0.write("3")
    for i in usr_result:
        repo_result.append(repos(i))            # Generate a list of repos
        print (time.clock(), "检索用户中...", i)
    for i in repo_result:                      # Generate a merged list of repositories
        repo_list_merge.extend(i)

    t2 = time.clock()                           # clock end
    t = t2 - t1

    # output modules
    print ("===== Stage 4 Launched ")
    f0.write("4")
    j_son = usr_tree.to_json(with_data=True)    # generate a copy of user tree structure
    f1 = open(r'json_user.txt', 'a')
    f1.write(j_son)                             # send tree structure copy
    f2 = open(r'list_user.txt', 'a')
    result_str = ','.join(usr_result)
    f2.write(result_str)                        # send user list (converted into string) copy
    f3 = open(r'repo_lists.txt', 'a')
    result_str_merged = ','.join(repo_list_merge)
    f3.write(result_str_merged)

    print ("\n")
    print ("================== ANALYSIS FINISHED ==================")
    print ("TIME USED:", t)
    print (initial_node, "Users have been analyzed: ")
    print (usr_result)
    # print repo_result
    print (len(repo_list_merge), "Repo have been analyzed: ")
    print (repo_list_merge)


if __name__ == '__main__':
    main("tomekent", 30)

