# -*- coding: utf-8 -*-


import os
from splinter.browser import Browser
import time
import getpass
from dataBase.dataBase import get_cursor
from dataBase.dataBase import insert_user
from dataBase.dataBase import fetch_pwd
from dataBase.dataBase import fetch_username


c = get_cursor()
username = fetch_username()
pwd = fetch_pwd()

if (username is None) | (pwd is None):
    # 输入信息
    username = raw_input('please input userName:')
    pwd = getpass.getpass('please input password:')


dir = raw_input('please input project dir:')


# 判断目录路径是否存在
def file_name(file_dir):
    for roots, dirs, files in os.walk(file_dir):

        for child_file in files:
            if os.path.splitext(child_file)[1] == '.podspec':
                return os.path.join(roots, child_file)


filename = file_name(dir)

while filename is None:
    print 'invalid path'
    dir = raw_input('please input project dir:')
    filename = file_name(dir)

print(filename)


env = raw_input('please input code-branch(dev or test or release):')
detail = raw_input('please input publish content:')


# 判断发布分支
def judge_branch_exist(judge_env):

    if judge_env == 'dev':
        return 'devEnv'
    elif judge_env == 'test':
        return 'testEnv'
    elif judge_env == 'release':
        return 'produceEnv'
    else:
        print 'error：invalid branch'
        new_env = raw_input('please input code-branch(dev or test or release):')
        judge_branch_exist(new_env)


# 判断分支存在
env_id = judge_branch_exist(env)


f = open(filename, 'r')

lines = f.readlines()
# 版本号
versionNo = ''
# 组件名
component_name = ''

for line in lines:
    if ("s.name" in line) & (line.find("{") == -1):
        tempList = line.split('"')
        component_name = tempList[1]
        print component_name

    if ("s.version" in line) & (line.find("{") == -1):
        tempList = line.split('"')
        for str2 in tempList:
            if ("." in str2) & (str2.find('=') == -1):
                versionNo = str2
                print versionNo

    if "s.homepage" in line:
        tempList = line.split('"')
        for str1 in tempList:
            if "http://" in str1:
                url = str1
                print url


f.close()

# 版本标签
b = Browser("chrome")


def add_version_tag(input_name, input_pwd):
    b.visit(url + '/tags/new')
    time.sleep(1)
    b.fill('username', input_name)
    b.fill('password', input_pwd)
    b.find_by_name('remember_me').click()
    b.find_by_name('button').click()
    if b.find_by_id('tag_name').__len__() == 0:
        print 'invalid userName or password'
        input_name = raw_input('please input userName:')
        input_pwd = getpass.getpass('please input password:')
        add_version_tag(input_name, input_pwd)
        print 'login fail'
        return
    else:
        insert_user(input_name, input_pwd)
        return 1


login_success = add_version_tag(username, pwd)


if env_id == 'devEnv':
    versionNo = versionNo + '-TEST'


b.fill('tag_name', versionNo)
b.find_by_name('button').click()


# 发布
b.visit('http://sdp.nd/main.html')
time.sleep(0.5)
b.find_by_id('login').click()


username = fetch_username()
pwd = fetch_pwd()

b.find_by_id('object_id').fill(username)
b.find_by_id('password').fill(pwd)
b.find_by_name('keep_pwd')
b.find_by_id('confirmLogin').click()
time.sleep(1)
b.visit('http://sdp.nd/main.html')

b.find_by_id('appSearchTxt').fill(component_name)


while b.find_link_by_partial_href('/modules/mobileComponent/detail.html?appId') is []:
    print '.'

b.find_link_by_partial_href('/modules/mobileComponent/detail.html?appId').click()


# 选择分支
time.sleep(0.5)
b.find_by_xpath('/html/body/div[4]/a[2]').first.click()

b.find_by_xpath('//*[@id="appDeatil"]/div[1]/span[2]/span').first.click()
b.find_by_id(env_id).first.find_by_tag('a').click()
b.find_by_id('publish').first.click()

# 版本号
b.find_by_id('version').fill(versionNo)
b.find_by_id('versionDesc').fill(detail)

# b.find_by_xpath('//*[@id="gitlist"]/div').first.click()
# b.find_by_id('publishConfirm').click()
