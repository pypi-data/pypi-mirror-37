#!/usr/bin/env python
# -*- coding=utf-8 -*-


"以下是创建的具体思路"
# 1. pod lib create LJCache
# 2. cd LJcache
# 3. git remote add origin ssh://handa@gerrit.lianjia.com:29418/mobile_ios/LJCache
# 4. 添加changeID scp -p -P 29418 handa@gerrit.lianjia.com:hooks/commit-msg  .git/hooks/
# 5. 添加 review.sh,  versionHistory.md 更新文档
# 6. git add .
# 7. git commit --amend --no-edit
# 8. 创建develop 分支并同步到远端  暂时用户行为
# 9. 修改podspec文件  用户行为
# 10. pod update  用户行为
# 11. 写代码   用户行为
# 12. 修改podspec文件到最新版，创建新版本，并生成静态库。把静态库文件移动到放到二进制文件。binary, 目前只打静态库framework。


import getopt
import importlib
import json
import os
import re
import shutil
import subprocess
import urllib
import yaml

__author__ = "handa"
__version__ = "0.0.32"

# DEBUG = True
DEBUG = False

import sys
reload(sys) # Python2.5 初始化后删除了 sys.setdefaultencoding 方法，我们需要重新载入
sys.setdefaultencoding('utf-8')


"""
初始化模板的的时候全局变量
"""
emailSuffix = "@lianjia.com"
platform = "iOS"
language = "ObjC"
demo = "Yes"
testing = "None"
based = "No"
prefix = "LJ"


"""
标准模板示例Example中需要忽略的内容
"""
ignoreFileString = "Pods/"


"提交脚本，即review.sh  想要提交的时候，主要在命令行运行： sh review.sh 就能提交gerrit"
reviewInfo = """

#bin/bash

git_prefix=".git"

install_commit_msg(){ 
    if [ ! -f ".git/hooks/commit-msg" ]; then
        echo "请输入用户名(不需要加后缀)"
        read username
        gitdir=$(git rev-parse --git-dir); 
        scp -p -P 29418 ${username}@gerrit.lianjia.com:hooks/commit-msg ${gitdir}/hooks/
        if [ ! $? -eq 0 ]; then
            echo "commit-msg下载错误"
            exit 1
        else
            echo "已经存在"
        fi
    fi
}

if [ ! -d "$git_prefix" ]; then
	echo "! [Illegal git repository directory]"
	echo "  移动脚本到git仓库根目录"
	exit 1
fi


if [ ! -d ".git/hooks" ]; then
    mkdir ".git/hooks"
	echo "mkdir successfull"
fi

while getopts "m:c" arg
do
	case $arg in
		m)
		  echo "git commit -a -m ..."
          install_commit_msg
          git commit -a -m "$OPTARG"
          ;;
		c)
		  echo "git commit -a --amend -C HEAD"
          install_commit_msg
          git commit -a --amend -C HEAD;
          ;;
	esac
done


if [ -f ".git/HEAD" ]; then
    head=$(< ".git/HEAD")
    if [[ $head = ref:\ refs/heads/* ]]; then
        git_branch="${head#*/*/}"
    else
        echo "无法获取当前分支"
	    exit 1
    fi

else
    echo "没有git中的HEAD文件"
	exit 1
fi


reviewers=("handa, zhangyansong, yuanyueguang001, zhaohongwei002, songhongri001, lixiangyu004, zhaoxiaomeng001")

echo "当前分支为:$git_branch"

pushUrl="HEAD:refs/for/$git_branch%"
for reviewer in ${reviewers[@]}; do 

    echo "reviewer人员为${reviewer}"    
    pushUrl="${pushUrl}r=${reviewer},"
done
pushUrl="${pushUrl%,*}"
echo "pushUrl为:$pushUrl"
git push origin $pushUrl
if [ $? -eq 0 ]; then
	exit 0
else
	exit 1
fi


"""

noSubSpec = """
  s.preserve_paths = "#{s.name}/Classes/**/*", "#{s.name}/Assets/**/*", "#{s.name}/Framework/**/*", "#{s.name}/Archive/**/*", "#{s.name}/Dependencies/**/*"

  configuration = "Release"
  if ENV["IS_DEBUG"] || ENV["#{s.name}_DEBUG"]
    configuration = "Debug"
  elsif ENV["IS_RELEASE"] || ENV["#{s.name}_Relase"]
    configuration = "Release"
  end
  
  if ENV['IS_SOURCE'] || ENV["#{s.name}_SOURCE"]
    # 源码部分，请在这里写上必要的。
    s.source_files = "#{s.name}/Classes/**/*.{h,m,mm,c,cpp,cc}"
    s.public_header_files = "#{s.name}/Classes/**/*.h"
    # 如果有自己依赖的库，请写在这里，并且把依赖的.a 或者 .framework 放到Classes 同级别的Dependencies目录下
    # s.source_files = "#{s.name}/Classes/**/*.{h,m,mm,c,cpp,cc}", "#{s.name}/Dependencies/**/*.{h,m,mm,c,cpp,cc}"
    # s.public_header_files = "#{s.name}/Classes/**/*.h", "#{s.name}/Dependencies/**/*.h"
    # ...
  elsif ENV['IS_ARCHIVE'] || ENV["#{s.name}_ARCHIVE"]
    s.public_header_files = "#{s.name}/Archive/#{configuration}/*.h"
    s.source_files = "#{s.name}/Archive/#{configuration}/*.h"
    s.vendored_libraries = "#{s.name}/Archive/#{configuration}/lib#{s.name}.a"
    # 如果源码有依赖的库，上面这一行需要换成下面的
    # s.public_header_files = "#{s.name}/Archive/#{configuration}/*.h", "#{s.name}/Dependencies/**/*.h"
    # s.source_files = "#{s.name}/Archive/#{configuration}/*.h", "#{s.name}/Dependencies/**/*.h"
    # s.vendored_libraries = "#{s.name}/Archive/#{configuration}/lib#{s.name}.a","#{s.name}/Dependencies/**/*.a"
    # s.vendored_frameworks= "#{s.name}/Dependencies/**/*.framework"
  else
    s.public_header_files = "#{s.name}/Framework/#{configuration}/*.h"
    s.source_files = "#{s.name}/Framework/#{configuration}/*.h"
    s.vendored_frameworks = "#{s.name}/Framework/#{configuration}/#{s.name}.framework"
    # 如果源码有依赖的库，上面的一行酌情换成下面的语句
    # s.public_header_files = "#{s.name}/Framework/#{configuration}/*.h", "#{s.name}/Dependencies/**/*.h"
    # s.source_files = "#{s.name}/Framework/#{configuration}/*.h", "#{s.name}/Dependencies/**/*.h"
    # s.vendored_frameworks = "#{s.name}/Framework/#{configuration}/#{s.name}.framework","#{s.name}/Dependencies/**/*.framework"
    # s.vendored_libraries = "#{s.name}/Dependencies/**/*.a"
  end
  # 公共部分，比如公共资源类。framework等
  # s.resources        = "#{s.name}/Assets/**/*.{bundle,lic,png,jpg,plist}"
  # 或者
  # s.resource_bundle = {
  #   "#{s.name}" => "#{s.name}/Assets/*.{storyboard,xib,json,xcassets,png,html}"
  # }

"""


packageBySubspec = """

  s.preserve_paths = "#{s.name}/Classes/**/*", "#{s.name}/Assets/**/*", "#{s.name}/Framework/**/*", "#{s.name}/Archive/**/*", "#{s.name}/Dependencies/**/*"
  
  # :spec_name => 名字
  _Core = {:spec_name => "Core"}
  # :sub_dependency => 内部依赖的数组, 变量是subspec形式的。
  # :resources => 指向资源的路径字符串
  _Foundation = {:spec_name => "Foundation", :resources => "#{s.name}/Assets/**/*.{bundle,lic,png,jpg,plist}" , :sub_dependency => [_Core]}
  # :dependency => 字典元素的数组， 里面每个字典包含两个元素 :name=> 第三方库名字， :version => 版本号(如果不指定，不写)
  _UIKit = {:spec_name => "UIKit", :dependency => [{:name => "AFNetworking", :version => "3.2.0"}]}

  #subspec 的集合
  _subspecs = [_Core, _Foundation, _UIKit]

  configuration = "Release"
  if ENV["IS_DEBUG"] || ENV["#{s.name}_DEBUG"]
    configuration = "Debug"
  elsif ENV["IS_RELEASE"] || ENV["#{s.name}_Relase"]
    configuration = "Release"
  end
  
  _subspecs.each do |spec|
    if spec.delete(:noSource)
      next
    end
    if ENV["#{s.name}_#{spec[:spec_name]}_SOURCE"] || ENV['IS_SOURCE']
      #源码部分
      spec[:source_files] = "#{s.name}/Classes/#{spec[:spec_name]}/**/*.{h,m,mm,c,cpp,cc}"
      spec[:public_header_files] = "#{s.name}/Classes/#{spec[:spec_name]}/**/*.h"
    elsif ENV["#{s.name}_#{spec[:spec_name]}_ARCHIVE"] || ENV['IS_ARCHIVE']
      spec[:source_files] = "#{s.name}/Archive/#{spec[:spec_name]}/#{configuration}/*.h"
      spec[:public_header_files] = "#{s.name}/Archive/#{spec[:spec_name]}/#{configuration}/*.h"
      spec[:vendored_libraries] = "#{s.name}/Archive/#{spec[:spec_name]}/#{configuration}/*.a"
      # 如果源码有依赖的库，上面这一行需要换成下面的
      # s.public_header_files = "#{s.name}/Archive/#{configuration}/*.h", "#{s.name}/Dependencies/**/*.h"
      # s.source_files = "#{s.name}/Archive/#{configuration}/*.h", "#{s.name}/Dependencies/**/*.h"
      # s.vendored_libraries = "#{s.name}/Archive/#{configuration}/lib#{s.name}.a","#{s.name}/Dependencies/**/*.a"
      # s.vendored_frameworks= "#{s.name}/Dependencies/**/*.framework"
    else
      spec[:source_files] = "#{s.name}/Framework/#{spec[:spec_name]}/#{configuration}/*.h"
      spec[:public_header_files] = "#{s.name}/Framework/#{spec[:spec_name]}/#{configuration}/*.h"
      spec[:vendored_frameworks] = "#{s.name}/Framework/#{spec[:spec_name]}/#{configuration}/*.framework"
      # 有外部依赖的静态库的话请注释上面一行，换下面的
      # s.public_header_files = "#{s.name}/Framework/#{configuration}/*.h", "#{s.name}/Dependencies/**/*.h"
      # s.source_files = "#{s.name}/Framework/#{configuration}/*.h", "#{s.name}/Dependencies/**/*.h"
      # s.vendored_frameworks = "#{s.name}/Framework/#{configuration}/#{s.name}.framework","#{s.name}/Dependencies/**/*.framework"
      # s.vendored_libraries = "#{s.name}/Dependencies/**/*.a"
    end
  end

  _subspecs.each do |spec|
    s.subspec spec[:spec_name] do |ss|
      if spec[:source_files]
        ss.source_files = spec[:source_files]
      end

      if spec[:public_header_files]
        ss.public_header_files = spec[:public_header_files]
      end

      if spec[:vendored_libraries]
        ss.vendored_libraries = spec[:vendored_libraries]
      end

      if spec[:vendored_frameworks]
        ss.vendored_frameworks = spec[:vendored_frameworks]
      end

      if spec[:resources]
        ss.resources = spec[:resources]
      end

      if spec[:sub_dependency]
        spec[:sub_dependency].each do |dep|
          ss.dependency "#{s.name}/#{dep[:spec_name]}"
        end
      end

      if spec[:dependency]
        spec[:dependency].each do |dep|
          if dep.has_key?(:version)
            ss.dependency dep[:name], dep[:version]
          else
            ss.dependency dep[:name]
          end
        end
      end

      if spec[:frameworks]
        spec[:frameworks].each do |f|
          ss.framework = "#{f}"
        end
      end
    end
  end
  # 公共部分
  # ――― Resources ―――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――― #
  #
  #  A list of resources included with the Pod. These are copied into the
  #  target bundle with a build phase script. Anything else will be cleaned.
  #  You can preserve files from being cleaned, please don't preserve
  #  non-essential files like tests, examples and documentation.
  #

  # s.resource  = "icon.png"
  # s.resources = "Resources/*.png"
    
  # ――― Project Linking ―――――――――――――――――――――――――――――――――――――――――――――――――――――――――― #
  #
  #  Link your library with frameworks, or libraries. Libraries do not include
  #  the lib prefix of their name.
  #
  # 公共部分，比如公共资源类。framework等
  # s.framework  = "SomeFramework"
  # s.frameworks = "SomeFramework", "AnotherFramework" 
  # s.library   = "iconv"
  # s.libraries = "iconv", "xml2" 
  # ――― Project Settings ――――――――――――――――――――――――――――――――――――――――――――――――――――――――― #
  #
  #  If your library depends on compiler flags you can set them in the xcconfig hash
  #  where they will only apply to your library. If you depend on other Podspecs
  #  you can include multiple dependencies to ensure it works.
  
"""

def excommand(cmd):
    """
    子线程执行脚本
    Arguments:
        cmd {str} -- cmd命令
    Returns:
        Pipe -- 管道
    """
    return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

def excommandUntilDone(cmd):
    """
    子线程执行脚本，直到结束，并输出
    Arguments:
        cmd {str} -- cmd命令
    Returns:
        Pipe -- 管道
    """
    p=subprocess.Popen(args="export LANG=en_US.UTF-8;"+cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=False)
    outPut=""
    for line in iter(p.stdout.readline, ''):
        outPut+=line
        print line.rstrip()
    p.wait()
    return (p.returncode,outPut)


def fileExist(path):
    """
    检测模块是否已经安装
    Arguments:
        path {str} -- 模块路径
    Returns:
        Bool -- 是否已经安装
    """
    if os.path.isdir(path) or os.path.isfile(path):
        return True
    return False


def excommandWithProgress(cmd):
    return os.popen(cmd)


def initTemplate(cmd, user):
    """
    初始化spec模板并交互
    Arguments:
        cmd {str} -- 命令
    Returns:
        Popen -- 管道
    """
    formatPrint("正在初始化工程模板...")
    pexpect = importlib.import_module('pexpect')
    pexpect.logfile = sys.stdout
    q0 = "What is your name?"
    q1 = "What is your email?"
    q2 = "What platform do you want to use"
    q3 = "What language do you want to use?"
    q4 = "Would you like to include a demo application with your library?"
    q5 = "Which testing frameworks will you use?"
    q6 = "Would you like to do view based testing?"
    q7 = "What is your class prefix?"
    email = user + emailSuffix
    child = pexpect.spawn(cmd)
    isRuning = True
    while isRuning:
        index = child.expect([q0, q1, q2, q3, q4, q5, q6, q7, pexpect.EOF, pexpect.TIMEOUT])
        if index == 0:
            formatPrint(q0)
            formatPrint(user)
            child.sendline(user)
        elif index == 1:
            formatPrint(q1)
            formatPrint(email)
            child.sendline(email)
        elif index == 2:
            formatPrint(q2)
            formatPrint(platform)
            child.sendline(platform)
        elif index == 3:
            formatPrint(q3)
            formatPrint(language)
            child.sendline(language)
        elif index == 4:
            formatPrint(q4)
            formatPrint(demo)
            child.sendline(demo)
        elif index == 5:
            formatPrint(q5)
            formatPrint(testing)
            child.sendline(testing)
        elif index == 6:
            formatPrint(q6)
            formatPrint(based)
            child.sendline(based)
        elif index == 7:
            formatPrint(q7)
            formatPrint(prefix)
            child.sendline(prefix)
        elif index == 8:
            formatPrint("初始化模板成功")
            isRuning = False
        elif index == 9:
            formatPrint("模板初始化超时，")
            isRuning = False
            returnError()
        else:
            formatPrint("脚本出错，请检查")
            returnError()
    return not isRuning


def formatPrint(printString, separator=""):
    """
    格式化输出格式
    Arguments:
        printString {str} -- 要输出的内容
    """
    if separator:
        print (separator) * 40 + '\n'
    print str(printString)
    if separator:
        print (separator) * 40 + '\n'


def formatInput(tips):
    """有提示的输入

    Arguments:
        tips {str} -- 输入提示

    Returns:
        str -- 输入的值
    """

    return str(raw_input(tips + '\n'))


def writeToFile(string, filePath):
    """把内容写进文件
    Arguments:
        string {string} -- 文件内容
        filePath {string} -- 文件路径
    """
    with open(filePath, "w+") as fileWriter:
        fileWriter.write(str(string))


def appendToFile(string, filePath):
    with open(filePath, "a+") as fileWriter:
        fileWriter.write(str(string))

def readFile(filePath):
    """读文件

    Arguments:
        filePath {str} -- 文件路径

    Returns:
        str -- 文件内容
    """
    with open(filePath, "r+") as fileReader:
        return fileReader.read()


def readFileLines(filePath):
    """读文件成行
    Arguments:
        filePath {str} -- 文件路径
    Returns:
        str -- 文件内容
    """
    with open(filePath, "r+") as fileReader:
        return fileReader.readlines()


def matchList(pattern, string, byLine=False):
    """正则匹配

    Arguments:
        pattern {str} -- 正则表达式
        string {str} -- 要匹配的全量字符串

    Keyword Arguments:
        byLine {bool} -- 是不是一行一样匹配 (default: {False})

    Returns:
        [list] -- 匹配成功的列表
    """
    if string == "未知消息类型":
        formatPrint("没有匹配到相应的内容")
        returnError()
    if byLine:
        pattern = re.compile(pattern)
    else:
        pattern = re.compile(pattern, re.S)
    matchList = pattern.findall(string)
    if isinstance(matchList, list):
        return matchList
    else:
        formatPrint("没有匹配到相应的内容")
        returnError()


def printTips():
    formatPrint("""脚本参数错误，请参考以下提示：

        需要先看看相关python环境有没有安装好。请运行
            > specCreator env
        参数：
            --gerritUser            gerrit用户名
            --projectPath           工程地址
            --podName               pod库名（需要再根目录)
            --version               要打包的版本
            --subPackage            打包的时候是否要每个subspec单独打包。（默认为False)
            --commitId              打包的时候依照哪个commit开始打包（这个commitId必须已经push到远程）  
            --debug                 打debug还是release（默认是false，即打release包)
            --dependencyJSON        依赖的库的JSON（字典）,可以是JSON文件的路径
            
            下面的是只在 autoPackage 中起作用，只要有参数就可
            --branch                在哪个分支上打包
            --check                 打包前要检查podspec书写是否规范
            --framework             要打Framework静态库
            --archive               要打Archive静态库
            --debugPackage          打debug包
            --releasePackage        打release包
            --autoPush              打完包后自动commit并push
            --autoPushRepo          提交后自动更新repo发布。如果已经在repo白名单不需要此操作
            --repoSource            repo仓库的url，地址发布到哪个仓库
            --resultPath            必要信息会以JSON格式追加到这个文件
            --subspecs              字符串，需要打的subspec，多个用逗号隔开。前提是subPackage为True.（如果只提供部分subspec，其他的subspec不处理（即如果其他的subspec有静态库，不删除，如果没有，也不会重新打)，适用于做subspec的部分更新，而不需要把没变化的subspec也打静态库，节省时间）


                   
        本脚本的功能：
            1：从0开始创建一个spec标准库模板（暂不支持从一个已经存在的工程创建）
                > specCreator init 
                    --gerritUser=handa 
                    --projectPath=/Users/handa/Documents/LJABCD
            2：spec标准库检查。
                > specCreator check
                    --projectPath=/Users/handa/Documents/LJCache 
                    --podName=LJCache 
                    --dependencyJSON="{\"LJHTTPService\":\"0.2.2\",\"AFNetworking\":\"3.2.1\"}"
            3：创建spec标准库的静态库（.framework)
            前提是：有spec工程，且工程里改了spec文件，并检查通过
                > specCreator package
                    --projectPath=/Users/handa/Documents/LJCache
                    --podName=LJCache
                    --version=0.1.25
                    --commitId=ffa72511e6166222f294ddd874fd54247e82b369
                    --debug=false
                    --dependencyJSON="{\"LJHTTPService\":\"0.2.2\",\"AFNetworking\":\"3.2.1\"}"
            4：创建spec标准库的静态库（.a）（暂不支持生成非标准模板的静态库）
            前提是：有spec工程，且工程里改了spec文件，并检查通过
                > specCreator packageA
                    --projectPath=/Users/handa/Documents/LJCache
                    --podName=LJCache
                    --version=0.1.25
                    --subPackage=false
                    --commitId=ffa72511e6166222f294ddd874fd54247e82b369
                    --debug=false
                    --dependencyJSON="{\"LJHTTPService\":\"0.2.2\",\"AFNetworking\":\"3.2.1\"}"
            5：对已经存在的podspec文件进行源码和静态库的适配。
                > specCreator initSpec
                    --projectPath=/Users/handa/Documents/LJABCD
                    --podName=LJABCD
        
        对服务端如果完全自动化，请运行：
                > specCreator autoPackage
                    --projectPath=/Users/handa/Documents/LJCache
                    --podName=LJCache
                    --branch=master
                    --version=0.1.27
                    --subPackage=false
                    --commitId=a6c064311553a38d543d7944c07d4643388b0444
                    --dependencyJSON="{\"LJHTTPService\":\"0.2.2\",\"AFNetworking\":\"3.2.1\"}"
                    --resultPath=/Users/handa/Documents/LJCache/result.txt
                    --repoSource=http://git.lianjia.com/mobile_ios/Lianjia_component_Podspec.git
                    --framework
                    --archive
                    --check
                    --debugPackage
                    --releasePackage
                    --autoPush
                    --autoPushRepo
                    --subspecs=Foundation,UIKit,Core

        init 运行前提：
            1：先从张岩松那里申请创建一个girrit项目，从那里获取工程名，如：LJCache

        运行前提灰常重要
    """)


def getProjectName(projectPath):
    """获取项目名字

    Arguments:
        projectPath {str} -- 项目目录

    Returns:
        str -- 项目名
    """

    projectName = projectPath.split('/')[-1]
    if not projectName:
        # 防止出现 x/xxxx/ 工程名后有/的情况
        projectPath.split('/')[-2]
    return projectName


def checkEnv():
    if not fileExist("/usr/local/bin/pip"):
        formatPrint("正在安装pip组件（一个类似于gem的安装器）")
        excommandUntilDone("sudo -H easy_install pip")
    if not fileExist("/Library/Python/2.7/site-packages/tornado") and not fileExist("/usr/local/lib/python2.7/site-packages/tornado"):
        formatPrint("正在安装tornado组件")
        excommandUntilDone("sudo -H pip install tornado")
    if not fileExist("/Library/Python/2.7/site-packages/nose") and not fileExist("/usr/local/lib/python2.7/site-packages/nose"):
        formatPrint("正在安装nose组件")
        excommandUntilDone("sudo -H pip install nose")
    if not fileExist("/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python/matplotlib") and not fileExist("/usr/local/lib/python2.7/site-packages/matplotlib"):
        formatPrint("正在安装matplotlib组件")
        excommandUntilDone("sudo -H pip install matplotlib")
    if not fileExist("/Library/Python/2.7/site-packages/pexpect") and not fileExist("/usr/local/lib/python2.7/site-packages/pexpect"):
        formatPrint("初始化pexpect组件")
        excommandUntilDone("sudo -H pip install pexpect")
    if not fileExist("/Library/Ruby/Gems/2.3.0/gems/cocoapods-packager-1.5.0"):
        formatPrint("正在安装打包脚本cocoapods-packager")
        excommandUntilDone("sudo -H gem install cocoapods-packager")
    if not fileExist("/Library/Python/2.7/site-packages/yaml"):
        formatPrint("正在安装打包脚本PyYAML")
        excommandUntilDone("sudo -H pip install PyYAML")


def packageA(projectPath,podName, subSpecName, version, commitId, debug, dependencyJSON, subspecs):
    "打包.a"
    return package(projectPath, podName, subSpecName, version, commitId, debug, dependencyJSON, subspecs, isFrameWork=False)


def create_tmp_podspec(podName, subSpecName, version, commitId, dependencyJSON):
    if not commitId:
        formatPrint("subspec 打包必须要commitId")
        returnError()
    createPodspec(podName + subSpecName, "Tmp", version, commitId, dependencyJSON)
    userPath = os.path.expanduser('~')
    repoName = "lianjia-mobile_ios-LJComponentPodSpecs"
    repoPath = userPath + "/.cocoapods/repos/" + repoName
    repoSource = "http://gerrit.lianjia.com/mobile_ios/LJComponentPodSpecs"
    if not fileExist(repoPath):
        returnCode, content = excommandUntilDone("pod repo add " + repoName + " " + repoSource)
        if returnCode > 0:
            formatPrint(repoSource + "添加repo失败，请确认是否再内网。", " *")
            returnError()
    tmpPodspecFileName = podName + subSpecName + "Tmp.podspec"
    tmpPodspecPath = repoPath + "/" + podName + subSpecName + "Tmp/" + version
    if fileExist(tmpPodspecPath):
        formatPrint("可能存在已经有的podspec，请检查" + tmpPodspecPath, " -")

    returnCode, content = excommandUntilDone("mkdir -p " + tmpPodspecPath)
    if returnCode > 0:
        formatPrint("创建文件夹失败", " *")
        returnError()
    returnCode, content = excommandUntilDone("mv ./" + tmpPodspecFileName + " " + tmpPodspecPath + "/" + tmpPodspecFileName)
    if returnCode > 0:
        formatPrint("移动临时podspec失败", " *")
        returnError()


def clean_tmp_podspec(projectPath):
    userPath = os.path.expanduser('~')
    repoName = "lianjia-mobile_ios-LJComponentPodSpecs"
    repoPath = userPath + "/.cocoapods/repos/" + repoName
    if not fileExist(repoPath):
        excommandUntilDone("pod repo add " + repoName + " http://gerrit.lianjia.com/mobile_ios/LJComponentPodSpecs")
        excommandUntilDone("pod repo update " + repoName)
    os.chdir(repoPath)
    excommandUntilDone("git add .")
    excommandUntilDone("git reset --hard")
    os.chdir(projectPath)


def redirectSubSpec(originSpecPath):
    formatPrint(" 正在重定向subspec的dependency，为打包做准备", " -")
    if not fileExist(originSpecPath):
        formatPrint(originSpecPath + "需要重定向的文件不存在，请检查工程名或者podName是否正确")
        returnError()
    content = readFile(originSpecPath)
    contentList = []
    for lineStr in readFileLines(originSpecPath):
        tmpLineStr = lineStr.strip(" ")
        if str(tmpLineStr).startswith("#"):
            contentList.append(lineStr)
            continue
        tmpLineStr = tmpLineStr.replace("\n", "")
        if tmpLineStr.startswith("ss.dependency ") > -1 and tmpLineStr.find("/#{dep[:spec_name]}") > -1:
            originLine = tmpLineStr
            replaceLine = "ss.dependency \"#{s.name}Tmp/#{dep[:spec_name]}\""
            formatPrint("把" + lineStr + "替换成" + replaceLine, "-")
            lineStr = lineStr.replace(originLine, replaceLine)
        contentList.append(lineStr)
    replaceContent = "".join(contentList)
    # 把原podspec重命名
    writeToFile(replaceContent, originSpecPath)


def package(projectPath, podName, subSpecName, version, commitId, debug, dependencyJSON, subspecs, isFrameWork=True):
    """
    打包
    :param projectPath: 项目路径
    :param podName: pod库的名字
    :param subSpecName: 要打包的subspecName 为空表示整体打包
    :param commitId: 从哪个commitId打包
    :param debug:
    :param dependencyJSON:
    :param subspecs 所有的subspec
    :param isFrameWork:
    :return: content
    """
    podspecName = podName + subSpecName + ".podspec"
    # createSpec(podName, subSpecName, version, commitId, dependencyJSON)
    replacePodSpec(podName, subSpecName, version, commitId, dependencyJSON)
    if subSpecName:
        # 创建测试podspec
        redirectSubSpec(podName + subSpecName + ".podspec")
        create_tmp_podspec(podName, subSpecName, version, commitId, dependencyJSON)
    cmd = ""
    if subspecs:
        for subspec in subspecs:
            cmd += podName + "_" + subspec + "_SOURCE=1 "
    else:
        cmd += podName + "_SOURCE=1 "
    # cmd = "IS_SOURCE=1 "
    prefixString = ''
    suffixString = ''
    productDir = ''
    descFileName = ''
    if isFrameWork:
        cmd += "pod package " + podspecName + " --force --no-mangle --verbose --exclude-deps --spec-sources=http://gerrit.lianjia.com/mobile_ios/LJComponentPodSpecs,http://gerrit.lianjia.com/mobile_ios/Lianjia_component_Podspec.git,https://github.com/CocoaPods/Specs.git "
        suffixString = ".framework"
        productDir = podName + "/Framework"
    else:
        cmd += "pod package " + podspecName + " --library --force --verbose --no-mangle --exclude-deps --spec-sources=http://gerrit.lianjia.com/mobile_ios/LJComponentPodSpecs,http://gerrit.lianjia.com/mobile_ios/Lianjia_component_Podspec.git,https://github.com/CocoaPods/Specs.git "
        productDir = podName + "/Archive"
        prefixString = "lib"
        suffixString = ".a"

    destFileName = prefixString + podName + suffixString
    if len(subSpecName) > 0:
        productDir += "/" + subSpecName
        destFileName = prefixString + podName + subSpecName + suffixString
        cmd += "--subspecs=" + subSpecName
    productPath = ""
    if debug:
        productDir += "/Debug"
        productPath = productDir + "/" + destFileName
        cmd += " --configuration=DEBUG "
    else:
        productDir += "/Release"
        productPath = productDir + "/" + destFileName
    print cmd
    returnCode, content = excommandUntilDone(cmd)
    if returnCode > 0:
        formatPrint("打包失败，请检查。", "* ")
        returnError()
    podspecString = readFile(podspecName)
    versionMathList = matchList(r"s.version.*= [\'\"]([0-9]+\.[0-9]+\.[0-9]+)[\'\"]", podspecString)
    if not versionMathList:
        formatPrint("找不到版本信息，请检查podspec里的 s.version 字段")
    version = str(versionMathList[0])
    formatPrint(version)
    buildPath = podName + subSpecName + "-" + version
    binaryFilePath = buildPath + "/ios/" + prefixString + podName + subSpecName + suffixString
    formatPrint(binaryFilePath)
    if not fileExist(buildPath):
        formatPrint("没找到静态库的目录，请检查spec版本是否符合 x.x.x  规范或这其他")
        returnError()
    if not fileExist(binaryFilePath) and not subSpecName:
        formatPrint("没有打出静态库，可能库本身就没有源码部分。请检查。", " *")
    if not fileExist(productDir):
        excommandUntilDone("mkdir -p " + productDir)
    else:
        excommandUntilDone("rm -r -f " + productDir)
        excommandUntilDone("mkdir -p " + productDir)
    # backupPath =  productPath + suffixString
    # if fileExist(backupPath):
    #     formatPrint("备份上个版本信息到" + backupPath)
    #     excommandUntilDone("cp -R -f " + productPath + " " + backupPath)
    formatPrint("即将把" + descFileName + "放入发布目录：" + productDir)
    excommandUntilDone("cp -R " + binaryFilePath + " " + productPath)
    formatPrint("即将把静态库的头文件移动到目标目录：" + productDir)
    # 移动头文件

    sourcePath = os.path.join(binaryFilePath, "Headers")
    cpHeaders(sourcePath, productDir)
    formatPrint("即将删除临时文件")
    excommandUntilDone("rm -r -f " + buildPath)
    excommandUntilDone("rm -r -f " + podspecName)
    renamePodspec(podName + ".podspec.old", podName + ".podspec")
    clean_tmp_podspec(projectPath)
    formatPrint("成功生成静态库")
    print "- " * 30 + '\n'
    return content


def changePodSpec(podName, version, commitId=""):
    originSpecPath = podName + ".podspec"
    contentList = []
    for lineStr in readFileLines(originSpecPath):
        if str(lineStr).startswith("#"):
            contentList.append(lineStr)
            continue
        tmpLine = lineStr.replace("\n", "")
        tmpLine = tmpLine.replace("\t", "").strip(" ")
        if str(tmpLine).startswith("s.version"):
            originLine = tmpLine
            if version:
                replaceVersion = "s.version          = \'" + version + "\'"
                formatPrint("正在把" + originLine  + "替换为：" + replaceVersion)
                lineStr = lineStr.replace(originLine, replaceVersion)
        elif tmpLine.find("s.source") > -1 and tmpLine.find(":git") > -1:
            formatPrint("找到要替换的source行：" + tmpLine + ",\n")
            originSourceLine = tmpLine
            tmpLine = tmpLine.replace("git.lianjia.com", "gerrit.lianjia.com")
            sourceStr = str(tmpLine).strip("\n").strip("").split(",")[0].strip("}")
            replaceSource = ""
            if commitId:
                commitId = commitId.strip("\n")
                if tmpLine.find(":commit") > -1 or tmpLine.find(":tag"):
                    replaceSource = sourceStr + ", :commit => \"" + commitId + "\" }"
            else:
                if tmpLine.find(":commit") > -1 or tmpLine.find(":tag"):
                    replaceSource = sourceStr + ", :tag => s.name.to_s + \"-\" + s.version.to_s }"
            if replaceSource:
                formatPrint("正在把" + originSourceLine + "替换为：" + replaceSource)
                lineStr = lineStr.replace(originSourceLine, replaceSource)
        contentList.append(lineStr)
    writeToFile("".join(contentList), originSpecPath)


def cpHeaders(sourcePath, targetPath):
    if not os.path.exists(sourcePath):
        return
    if not os.path.exists(targetPath):
        os.makedirs(targetPath)
    # 遍历文件夹
    for fileName in os.listdir(sourcePath):
        # 拼接原文件或者文件夹的绝对路径
        absourcePath = os.path.join(sourcePath, fileName)
        # 拼接目标文件或者文件加的绝对路径
        abstargetPath = os.path.join(targetPath, fileName)
        if os.path.isdir(absourcePath):
            cpHeaders(absourcePath, abstargetPath)
        # 是文件就进行复制
        if os.path.isfile(absourcePath) and absourcePath.endswith(".h"):
            shutil.copyfile(absourcePath, abstargetPath)

def replacePodSpec(podName, subspecName, version, commitId, dependencyJSON):
    # 把原podspec重命名
    podspecName = podName + subspecName
    originSpecPath = podName + ".podspec"
    podspec = createPodSpecContent(podName, subspecName, version, commitId, dependencyJSON)
    renamePodspec(originSpecPath, originSpecPath+".old")
    writeToFile(podspec, podspecName + ".podspec")


def createPodspec(podName, subspecName, version, commitId, dependencyJSON):
    podspecName = podName + subspecName
    podspec = createPodSpecContent(podName, subspecName, version, commitId, dependencyJSON)
    writeToFile(podspec, podspecName + ".podspec")


def createPodSpecContent(podName, subspecName, version, commitId, dependencyJSON):
    dependencyDict = getDependencyDict(dependencyJSON)
    podspecName = podName + subspecName
    originSpecPath = podName + ".podspec"
    if not fileExist(originSpecPath):
        formatPrint(originSpecPath + "文件不存在，请检查工程名或者podName是否正确")
        returnError()
    content = readFile(originSpecPath)
    contentList = []
    for lineStr in readFileLines(originSpecPath):
        tmpLineStr = lineStr.replace("\t", "").strip(" ")
        if str(tmpLineStr).startswith("#"):
            contentList.append(lineStr)
            continue
        tmpLineStr = tmpLineStr.replace("\n", "")
        if str(tmpLineStr).startswith("s.name") and tmpLineStr.find(podName) > -1:
            originLine = tmpLineStr
            replaceSpecName = tmpLineStr.replace(podName, podspecName, 1)
            formatPrint("把" + lineStr + "替换成" + replaceSpecName, "-")
            lineStr = lineStr.replace(originLine, replaceSpecName)
        elif str(tmpLineStr).startswith("s.version"):
            originLine = tmpLineStr
            if version:
                replaceVersion = "s.version          = \'" + version + "\'"
                formatPrint("把" + lineStr + "替换成" + replaceVersion, "-")
                lineStr = lineStr.replace(originLine, replaceVersion)
        elif tmpLineStr.startswith("s.source") and tmpLineStr.find(":git") > -1:
            originSourceLine = tmpLineStr
            tmpLineStr = tmpLineStr.replace("git.lianjia.com", "gerrit.lianjia.com")
            sourceStr = str(tmpLineStr).strip("\n").strip("").split(",")[0].strip("}")
            replaceSource = ""
            if commitId:
                commitId = commitId.strip("\n")
                if tmpLineStr.find(":commit") > -1 or tmpLineStr.find(":tag"):
                    replaceSource = sourceStr + ", :commit => \"" + commitId + "\" }"
            else:
                if tmpLineStr.find(":commit") > -1 or tmpLineStr.find(":tag"):
                    replaceSource = sourceStr + " }"
            if replaceSource:
                formatPrint("把" + tmpLineStr + "替换成" + replaceSource, "-")
                lineStr = lineStr.replace(originSourceLine, replaceSource)
        elif tmpLineStr.find(":dependency =>") > -1:
            originLine = tmpLineStr
            propertyLine = str(tmpLineStr).split(":dependency =>")[-1].replace("[", "").replace("{","").\
                replace("}", "").replace("]", "")
            nameList = matchList(r":name +=> +\"(\w+?)\"", propertyLine)
            if nameList and nameList[0] in dependencyDict.keys():
                specName = nameList[0]
                versionList = matchList(r":version +=> +\"(.+?)\"", propertyLine)
                if len(versionList) == 1:
                    if not isinstance(dependencyDict[specName], list):
                        formatPrint("给的字典值必须是数组")
                        returnError()
                    replaceLine = dependencyDict[specName][-1]
                    formatPrint("把依赖：" + versionList[0] + "\n变成：   " + replaceLine + "\n", "-")
                    lineStr = lineStr.replace(versionList[0], replaceLine)
        elif tmpLineStr.find("#{s.name}") > -1:
            originLine = tmpLineStr
            replaceLine = tmpLineStr.replace("#{s.name}", podName)
            formatPrint("把库名：" + tmpLineStr + "\n变成：   " + replaceLine + "\n", "-")
            lineStr = lineStr.replace(originLine, replaceLine)
        elif tmpLineStr.find(".dependency ") > -1:
            originLine = tmpLineStr
            specName = tmpLineStr.split(" ")[-1].strip("\"").strip("\'").split("/")[0]
            if specName in dependencyDict.keys() and str.isalnum(specName[0]):
                if not isinstance(dependencyDict[specName], list):
                    formatPrint("给的字典值必须是数组")
                    returnError()
                versionString = ""
                for version in dependencyDict[specName]:
                    versionString += ", \"" + version + "\""
                replaceLine = tmpLineStr + versionString
                formatPrint("把" + lineStr + "替换成" + replaceLine, "-")
                lineStr = lineStr.replace(originLine, replaceLine)
        contentList.append(lineStr)
    # 去掉最后一个end
    endString = ""
    while(endString!="end"):
        endString = contentList.pop().strip("\n").strip("")
        print endString
    for key, versionList in dependencyDict.items():
        versionString = ""
        for vString in versionList:
            versionString += "\"" + vString + "\", "
        versionString = versionString.strip(" ").rstrip(",")
        dependencyString = "  s.dependency  \"" + str(key) + "\""
        if versionString:
            dependencyString += ", " + versionString
        contentList.append(dependencyString + "\n")
    contentList.append("end")
    replaceContent = "".join(contentList)
    return replaceContent


def renamePodspec(originSpecName, destinationSpecName):
    if fileExist(originSpecName) and not fileExist(destinationSpecName):
        excommandUntilDone("mv -f " + originSpecName + " " + destinationSpecName)

def checkSpec(podName, dependencyJSON):
    podspecName = podName + ".podspec"
    formatPrint("正在检测" + podspecName + "是否配置正确（前提是远程已经有写好的Spec文件）。")
    # createSpec(podName, "", "", "", dependencyJSON)
    replacePodSpec(podName, "", "", "", dependencyJSON)
    cmd = "IS_SOURCE=1 pod lib lint " + podspecName + " --allow-warnings --verbose --use-libraries --sources=http://gerrit.lianjia.com/mobile_ios/LJComponentPodSpecs,http://gerrit.lianjia.com/mobile_ios/Lianjia_component_Podspec.git,https://github.com/CocoaPods/Specs.git --fail-fast --no-clean"
    # pexpect = importlib.import_module('pexpect')
    # pexpect.run(cmd)
    returnCode, message = excommandUntilDone(cmd)
    if returnCode > 0:
        formatPrint("podspec 检测不通过，请检查podspec或者提供的dependencyJSON是否有问题。", " *")
        returnError()
    excommandUntilDone("rm " + podspecName)
    renamePodspec(podspecName + ".old", podspecName)


def returnError():
    # excommandUntilDone("git add . ;git reset --hard")
    exit(1)


def initProject(user, projectPath, subPackage):
    """初始化整个工程

    Arguments:
        user {str} -- 用户名
        projectPath {str} -- 项目路径
    """
    projectName = getProjectName(projectPath)
    parentPath = os.path.dirname(projectPath)
    if not fileExist(parentPath):
        formatPrint("父目录" + parentPath + "不存在，即将创建此目录")
        excommandUntilDone(r"sudo mkdir -p " + parentPath)
    os.chdir(parentPath)
    if fileExist(projectPath):
        formatPrint("文件已经存在，请确保这个工程是第一次初始化")
        # excommandUntilDone("rm -r -f LJCache")
        returnError()
    success = initTemplate(r"pod lib create " + projectName, user)
    if not success:
        formatPrint("模板初始化失败")
        returnError()
    formatPrint("切换到工程目录")
    excommandUntilDone("chmod +x " + projectName)
    os.chdir(projectPath)
    gerritUrl = "ssh://" + user + "@gerrit.lianjia.com:29418/mobile_ios/" + projectName
    formatPrint("项目gerrit地址是：" + gerritUrl)
    excommandUntilDone("git remote add origin " + gerritUrl)
    changeIDHookUrl = user + "@gerrit.lianjia.com:hooks/commit-msg"
    formatPrint("拉取gerrit的产生changID的脚本")
    excommandUntilDone("gitdir=$(git rev-parse --git-dir); scp -p -P 29418 " + changeIDHookUrl + " ${gitdir}/hooks/")
    formatPrint("添加提交脚本review.sh")
    writeToFile(reviewInfo, projectPath + "/review.sh")
    if fileExist("review.sh"):
        formatPrint("给提交脚本设置运行权限")
        excommandUntilDone("chmod +x review.sh")
    formatPrint("添加文档更新文件VersionHistory.md")
    excommandUntilDone("touch VersionHistory.md")
    # 更改podSpec文件
    initPodspecFile(projectPath, projectName, subPackage)
    formatPrint("git ignore Example/Pods 文件夹")
    excommandUntilDone("touch Example/.gitignore")
    writeToFile(ignoreFileString, "Example/.gitignore")
    formatPrint("初始化git相关")
    excommandUntilDone("git add .")
    excommandUntilDone("git commit --amend --no-edit")

    "切换分支因为涉及到需要远端先创建分支，一般没有push权限"
    # formatPrint("创建develop分支并同步到远端")
    # excommandUntilDone("git branch develop")
    # excommandUntilDone("git push origin develop")
    # formatPrint("切换到develop 分支")
    # excommandUntilDone("git checkout develop")


def processDependency(podName, contentDict={}):
    dependencyDict = {} # 支持subspec的时候，需要处理key
    if not contentDict:
        formatPrint("打包失败，请查看打包返回结果")
        exit(1)
    for key, content in contentDict.items():
        dependency = {}
        contentList = content.split("\n")
        # -> Installing LJGravityImageView (0.1.6)
        for line in contentList:
            if not str(line).startswith("-> Installing "):
                continue
            contentAndVersionList = line.split(" Installing ")[-1].split(" ")
            if len(contentAndVersionList) != 2:
                formatPrint(line + "\n解析库和版本失败。", " *")
                exit(1)
            name = contentAndVersionList[0]
            if podName in name:
                continue
            version = contentAndVersionList[-1].strip(")").strip("(")
            dependency[name] = version
        if dependency:
            dependencyDict[key] = dependency
    return dependencyDict


def realBranchs(commitId):
    returnCode, content = excommandUntilDone("git branch -r --contains " + commitId)
    if returnCode > 0:
        formatPrint(" 请确认commtid是否正确", " *")
        exit(1)
    branchs = content.strip("\n").split("\n")
    branchList = []
    for branch in branchs:
        if "-> origin/master" in branch:
            continue
        branch = str(branch).strip("\n").strip(" ").replace("origin/", "")
        branchList.append(branch)
    return branchList


def cleanDeprecatedStaticLibraries(framework, archive, debugPackage, releasePakcage, frameWorkPath, archivePath,
                                   subPackage, subspecs):
    formatPrint("正在清理陈旧的库")

    if framework or archive or debugPackage or releasePakcage:
        if subPackage:
            if subspecs:
                for subspec in subspecs:
                    excommandUntilDone("rm -r -f " + frameWorkPath + "/" + subspec)
                    excommandUntilDone("rm -r -f " + archivePath + "/" + subspec)
            else:
                excommandUntilDone("rm -r -f " + frameWorkPath)
                excommandUntilDone("rm -r -f " + archivePath)
        else:
            excommandUntilDone("rm -r -f " + frameWorkPath)
            excommandUntilDone("rm -r -f " + archivePath)


def canPackage(podName):
    specDict = getSpecDict(podName)
    sourcePathList = []
    if "source_files" in specDict.keys():
        sourcePath = specDict["source_files"]
        if isinstance(sourcePath, str):
            sourcePath = [sourcePath]
        sourcePathList.extend(sourcePath)
    elif "subspecs" in specDict.keys():
        subspecs = specDict["subspecs"]
        for subspec in subspecs:
            if "source_files" in subspec.keys():
                sourcePath = subspec["source_files"]
                if isinstance(sourcePath, str):
                    sourcePath = [sourcePath]
                sourcePathList.extend(sourcePath)
    else:
        return False
    for sourcePath in sourcePathList:
        splitString = ""
        if "/**/" in sourcePath:
            splitString = "/**/"
        elif "/*" in sourcePath:
            splitString = "/*"
        else:
            splitString = "/"
        sourcePath = sourcePath.split(splitString)[0]
        fileList = []
        for suffix in [".m", ".c", ".mm", ".cpp", ".cc"]:
            files = findfiles(sourcePath, suffix, True)
            if not files:
                continue
            return True
        if not fileList:
            continue
        return True
    return False


def findfiles(dirname, suffix, recursion=False):
    result = []
    for fileName in os.listdir(dirname):
        filePath = os.path.join(dirname, fileName)
        if os.path.isfile(filePath):
            if filePath.endswith(suffix):
                result.append(filePath)
        elif recursion and os.path.isdir(filePath):
            result.extend(findfiles(filePath, suffix, recursion))
    return result

def autoPackage(projectPath, podName, branch, version, subPackage=False, commitId="", dependencyJSON="", framework=True,
                archive=False, check=True, debugPackage=False, releasePackage=True, autoPush=False, autoPushRepo=False,
                repoSource="", resultPath="", whiteListPath="", subspecs=""):
    if not projectPath or not podName or not version:
        formatPrint("缺少必备的参数，请检查", "- ")
        returnError()
    resultDict = {}
    formatPrint("正在清理现场","- ")
    cleanEnv()
    formatPrint("正在拉取远程代码", "- ")
    excommandUntilDone("git pull")
    # 判断branch和commit
    if commitId:
        realBranchList = realBranchs(commitId)
        if branch and branch not in realBranchList:
            formatPrint("commit 所在分支并非提供的分支" + branch + "，而是在" + str(realBranchList), " *")
            returnError()
        if not branch:
            if realBranchList and len(realBranchList) == 1:
                realBranch = realBranchList[0]
                formatPrint("即将用在commitID" + commitId + "所在的分支" + realBranch + "进行打包", " -")
                branch = realBranch
            else:
                formatPrint("提供的commitID在如下的branch里：" + str(realBranchList) + ",请用--branch指定一个", " *")
                returnError()
    else:
        if not branch:
            formatPrint("commitID 或者 branch 至少提供一种", " *")
            exit(1)
        else:
            formatPrint("即将用在分支" + branch + "上用最新的commit进行打包", " -")
            returnCode, content = excommandUntilDone("git cherry")
            count = 0
            if content:
                count = len(content.strip("").strip("\n").split("\n"))
            returnCode, newCommitId = excommandUntilDone("git rev-parse " + branch + "~" + str(count))
            if returnCode > 0:
                formatPrint("不能获取当前分支的最新commit", " *")
                returnError()
            commitId = newCommitId
    formatPrint("正在切换到分支" + branch, "- ")
    excommandUntilDone("git checkout " + branch)
    # 检查是否符合规范
    subspecList = []
    if subspecs:
        for subspec in subspecs.strip(" ").split(","):
            subspecList.append(subspec.strip(" "))
    checkParams(podName, subPackage, whiteListPath, version, subspecList, autoPushRepo)
    podPath = os.path.join(projectPath, podName)
    frameWorkPath = os.path.join(podName, "Framework")
    archivePath = os.path.join(podName, "Archive")
    # 清理过期的库
    cleanDeprecatedStaticLibraries(framework, archive, debugPackage, releasePackage, frameWorkPath, archivePath,
                                   subPackage, subspecList)
    versionHistory = "## " + podName + " " + version + "\n\n"
    resultDict["projectPath"] = projectPath
    resultDict["podName"] = podName
    resultDict["branch"] = branch
    resultDict["version"] = version
    resultDict["subPackage"] = subPackage
    versionHistory += "- podName: " + podName + "\n"
    versionHistory += "- branch: " + branch + "\n"
    versionHistory += "- version: " + version + "\n"
    versionHistory += "- subPackage: " + str(subPackage) + "\n"
    examplePath = os.path.join(projectPath, "Example")

    if commitId:
        versionHistory += "- commitId: " + str(commitId) + "\n"
        resultDict["commitId"] = commitId

    if not fileExist(podPath):
        formatPrint("正在创建" + podPath, "- ")
        excommandUntilDone("mkdir -p " + podPath)
    if check:
        formatPrint("执行打包前检测","- ")
        checkSpec(podName, dependencyJSON)
        # checkSource(projectPath,podName,projectPath, examplePath)
        resultDict["checkSuccess"] = True
    versionHistory += "- 打的静态库包有：\n\n"
    versionHistory += "| \ | Framework | Archive  |\n"
    versionHistory += "| :---------: | :---------:| :---------:|\n"
    formatPrint("正在处理静态库目标文件","- ")
    dependencyDict = {}
    # 看有没有源码~
    haveSourceFile = canPackage(podName)
    if framework and debugPackage and haveSourceFile:
        formatPrint("正在打 framework debug 二进制库", "- ")
        versionHistory += "| Debug | ✔️️ |"
        contentDict = packageFramework(projectPath, podName, version, subPackage, commitId, True, dependencyJSON, subspecList)
        if len(dependencyDict.keys()) == 0:
            dependencyDict = processDependency(podName, contentDict)
        resultDict["debugFrameworkPath"] = os.path.join(frameWorkPath, "Debug")
    else:
        versionHistory += "| Debug | ️ |"
    if archive and debugPackage and haveSourceFile:
        formatPrint("正在打 archive debug 二进制库","- ")
        versionHistory += "✔️ | \n"
        contentDict = packageArchive(projectPath, podName, version, subPackage, commitId, True, dependencyJSON, subspecList)
        if len(dependencyDict.keys()) == 0:
            dependencyDict = processDependency(podName, contentDict)
        resultDict["debugArchivePath"] = os.path.join(archivePath, "Debug")
    else:
        versionHistory += " ️ |\n"
    if framework and releasePackage and haveSourceFile:
        formatPrint("正在打 framework release 二进制库","- ")
        versionHistory += "|Release | ✔️ |"
        contentDict = packageFramework(projectPath, podName, version, subPackage, commitId, False, dependencyJSON, subspecList)
        if len(dependencyDict.keys()) == 0:
            dependencyDict = processDependency(podName, contentDict)
        resultDict["releaseFrameworkPath"] = os.path.join(frameWorkPath, "Release")
    else:
        versionHistory += "| Release | ️ |"

    if archive and releasePackage and haveSourceFile:
        formatPrint("正在打 archive release 二进制库","- ")
        versionHistory += "✔️ | \n"
        contentDict = packageArchive(projectPath, podName, version, subPackage, commitId, False, dependencyJSON, subspecList)
        if len(dependencyDict.keys()) == 0:
            dependencyDict = processDependency(podName, contentDict)
        resultDict["releaseArchivePath"] = os.path.join(archivePath, "Release")
    else:
        versionHistory += " ️|\n"
    versionHistory += "\n"
    if dependencyDict:
        realDepencencyJson = json.dumps(dependencyDict)
        versionHistory += "- dependency :\n" + realDepencencyJson + "\n"
        resultDict["dependency"] = dependencyDict
    versionHistory += "    \n\n"
    formatPrint("将打包信息写入VersionHistory文件","- ")
    formatPrint(versionHistory)
    appendToFile(versionHistory, os.path.join(projectPath, "VersionHistory.md"))
    # 打包好后的本地检查, 暂时不处理
    if check and fileExist(examplePath) and False:
        os.chdir(examplePath)
        if framework:
            formatPrint("正在验证打的framework是否有问题", "- ")
            returnCode, content = excommandUntilDone("pod update --verbose --no-repo-update")
            if returnCode > 0:
                formatPrint("测试framework 库失败，可能原因：\n" +
                            "1: demo里或者源码部分头文件请用 #import <xxx/xxx.h> ,杜绝用 #import \"xxx.h\" 形式" +
                            "2: 请检查podsepc s.framework或者其他部分\n", "**")
                exit(1)
            formatPrint("正在用framework进行编译", "- ")
            buildworkspec(projectPath, podName)
        if archive:
            formatPrint("正在验证 .a 库是否有问题", "- ")
            returnCode, content = excommandUntilDone("IS_ARCHIVE=1 pod update --verbose --no-repo-update")
            if returnCode > 0:
                formatPrint("测试.a 库失败，可能原因：\n" +
                            "1: demo里或者源码部分头文件请用 #import <xxx/xxx.h> ,杜绝用 #import \"xxx.h\" 形式" +
                            "2: 请检查podsepc s.framework或者其他部分\n", "* ")
                exit(1)
            formatPrint("正在用.a进行编译", "- ")
            buildworkspec(projectPath, podName)
        formatPrint("正在验证源码是否有问题", "- ")
        returnCode, content = excommandUntilDone("IS_SOURCE=1 pod update --verbose --no-repo-update")
        if returnCode > 0:
            formatPrint("源码本身就编译不通过。请检查。", "* ")
            exit(1)
        formatPrint("正在用源码进行编译", "- ")
        buildworkspec(projectPath, podName)
        os.chdir(projectPath)
    else:
        formatPrint(examplePath + "没有检查或者本地测试目录不存在，即将跳过编译后检查", "* ")

    if autoPush:
        formatPrint("正在自动提交","- ")
        commitMessage = "自动打静态库:" + podName + " " + version
        returnCode, content = excommandUntilDone("git status")
        if "nothing to commit, working tree clean" not in content:
            excommandUntilDone("git add .")
            excommandUntilDone("git commit -m \'" + commitMessage + "\'")
        returnCode, newCommitId = excommandUntilDone("git rev-parse " + branch)
        changePodSpec(podName, version)
        returnCode, content = excommandUntilDone("git status")
        if "nothing to commit, working tree clean" not in content:
            excommandUntilDone("git add . ")
            excommandUntilDone("git commit -m \'发布" + podName + "-" + version + "\'")
        returnCode, content = excommandUntilDone("git push origin")
        if returnCode > 0:
            formatPrint("git push 失败，请确认你是否有权限","* ")
            returnError()
        resultDict["autoPushSuccess"] = True
    if autoPush and autoPushRepo:
        if not repoSource:
            formatPrint("自动发布请指定发布源参数：--repoSource","* ")
            returnError()
        formatPrint("正在自动发布","- ")
        tagVersion = podName + "-" + version
        excommandUntilDone("git tag " + tagVersion)
        returnCode, content = excommandUntilDone("git push origin  " + tagVersion)
        # 最好先清空下repo，防止repo污染
        pushRepo(podName, version, repoSource)
        resultDict["autoPushRepoSuccess"] = True
    if resultPath:
        if not fileExist(resultPath):
            parentDir = os.path.dirname(resultPath)
            formatPrint("文件不存在，正在创建输出文件","- ")
            excommandUntilDone("mkdir -p " + parentDir)
            excommandUntilDone("touch " + resultPath)
        writeToFile(json.dumps(resultDict), resultPath)
        formatPrint("结果写入成功","- ")
    clean_tmp_podspec(projectPath)
    formatPrint("二进制打包成功", "- ")


def pushRepo(podName, version, repoUrl):
    # 获取用户目录
    repoDict = getRepoDict()
    repoPath = repoPathByURL(repoDict, repoUrl)
    if not repoPath:
        addRepo(repoUrl)
        repoDict = getRepoDict()
        repoPath = repoPathByURL(repoDict, repoUrl)
    if not repoPath:
        formatPrint("找不到repoPath", " *")
        returnError()
    currentWD = os.getcwd()
    os.chdir(repoPath)
    returnCode, content = excommandUntilDone("git add .")
    if returnCode > 0:
        formatPrint("repo清理失败。", " *")
        returnError()
    excommandUntilDone("git reset --hard")
    excommandUntilDone("git pull")
    os.chdir(currentWD)
    movePodspecToRepo(podName, version, repoPath)
    os.chdir(repoPath)
    excommandUntilDone("git add .")
    commitMsg = "自动发布" + podName + "的版本：" + version
    excommandUntilDone("git commit -m \"" + commitMsg + "\"")
    excommandUntilDone("git push origin")
    os.chdir(currentWD)

def movePodspecToRepo(podName, version, repoPath):
    podspecFileName = podName + ".podspec"
    podspecPath = repoPath + "/" + podName + "/" + version
    if fileExist(podspecPath):
        formatPrint("可能存在相同tag的的podspec，请检查" + podspecPath, " *")
    returnCode, content = excommandUntilDone("mkdir -p " + podspecPath)
    if returnCode > 0:
        formatPrint("创建文件夹失败", " *")
        returnError()
    returnCode, content = excommandUntilDone(
        "mv ./" + podspecFileName + " " + podspecPath + "/" + podspecFileName)
    if returnCode > 0:
        formatPrint("移动临时podspec失败", " *")
        returnError()


def getRepoDict():
    returnCode, content = excommandUntilDone("pod repo list")
    if returnCode > 0:
        formatPrint("pod repo list 失败", " *")
        returnError()
    contentLines = content.split("\n")
    yamlContent = ""
    for line in contentLines:
        if not line or " repo" in line:
            continue
        if ":" not in line:
            line += " :"
        if str(line).startswith("-"):
            line = line.replace("-", " ", 1)
        yamlContent += line + "\n"
    repoDict = yaml.load(yamlContent)
    return repoDict

def addRepo(repoURL):
    repoName = repoNameFromURL(repoURL)
    userPath = os.path.expanduser('~')
    repoPath = userPath + "/.cocoapods/repos/" + repoName
    if not fileExist(repoPath):
        excommandUntilDone(
            "pod repo add " + repoName + " " + repoURL)
        excommandUntilDone("pod repo update " + repoName)

def repoPathByURL(repoDict, repoURL):
    for repoName, repoInfo in repoDict.items():
        if repoURL == repoInfo["URL"]:
            return repoInfo["Path"]
    return ""


def repoNameFromURL(repoURL):
    if not isURL(repoURL):
        formatPrint("url 不合法", " *")
        returnError()
    host, port = URLHostAndPort(repoURL)
    hostList = str(host).split(".")
    hostName = ""
    if len(hostList) == 3:
        hostName = hostList[1]
    tmp, path = URLPath(repoURL)
    path = str(path).replace("/", "-")
    return hostName + path


def isURL(URL):
    """
    判断URL是否合法
    :param URL: 提供的URL
    :return: 是否合法
    """
    legalURL = matchList(r"^https?:/{2}\w.+$", URL)
    if legalURL:
        return True
    else:
        return False

def URLProtocol(URL):
    # http://www.ahlinux.com:8001/test
    protocol, s1 = urllib.splittype(URL)
    # ('http', '//www.ahlinux.com:8001/test')
    return protocol, s1

def URLPath(URL):
    protocol, s1 = URLProtocol(URL)
    hostAndPort, path = urllib.splithost(s1)
    # ('www.ahlinux.com:8001', '/test')
    return hostAndPort, path

def URLHostAndPort(URL):
    # type: () -> (str, str)
    hostAndPort, path = URLPath(URL)
    host, port = urllib.splitport(hostAndPort)
    # ('www.ahlinux.com', '8001')
    return host, port

def checkSource(projectPath, podName, originPath, examplePath):
    if fileExist(examplePath):
        os.chdir(examplePath)
        formatPrint("正在验证源码是否有问题", "- ")
        returnCode1, content = excommandUntilDone("IS_SOURCE=1 pod update --verbose --no-repo-update")
        if returnCode1 > 0:
            formatPrint("IS_SOURCE=1 pod update 不通过。请检查。","* ")
            returnError()
        buildworkspec(projectPath, podName)
        os.chdir(originPath)
    else:
        formatPrint(examplePath + "本地测试路径不存在，已经跳过检查","* ")


def buildworkspec(projectPath, podName):
    xcworkSpaceName = projectPath + "/Example/" + os.path.basename(projectPath) + ".xcworkspace"
    return
    if fileExist(xcworkSpaceName):
        # 获得target
        cmd = "xcodebuild -workspace " + xcworkSpaceName + " -scheme " + podName + " -configuration Release"
        returnCode, content = excommandUntilDone(cmd)
        if returnCode > 0:
            formatPrint(" framework 时候编译不通过，请检查")
            exit(1)
    else:
        formatPrint("Example目录不符合标准规范，没有找到目录进行编译：" + xcworkSpaceName, "* ")


def boolValue(arg):
    value = False
    if arg in ("false", "FALSE", "False", "0"):
        value = False
    else:
        value = True
    return value


def getarguments(type=""):
    """
    获得参数
    :param type: 哪个命令的参数
    :return:
    """
    if type == "":
        return
    try:
        opts, args = getopt.getopt(sys.argv[2:], "facdrp",
                                   ["help", "gerritUser=", "projectPath=", "subPackage=", "podName=", "branch=",
                                    "version=", "commitId=", "debug=", "dependencyJSON=", "framework", "archive",
                                    "check", "debugPackage", "releasePackage", "autoPush", "autoPushRepo",
                                    "repoSource=", "resultPath=", "whiteListPath=", "subspecs="])
        # sys.argv[1:] 过滤掉第一个参数(它是脚本名称，不是参数的一部分)
    except getopt.GetoptError:
        print("argv error,please input")
        returnError()
    if not args and not opts:
        printTips()
        returnError()
    projectPath = ""
    user = ""
    podName = ""
    branch = ""
    subPackage = False
    version = ''
    commitId = ""
    debug = False
    dependencyJSON = ""
    framework = False
    archive = False
    check = False
    debugPackage = False
    releasePackage = False
    autoPush = False
    autoPushRepo = False
    resultPath=""
    repoSource = ""
    whiteListPath = ""
    subspecs = ""
    for cmd, arg in opts:
        print cmd + "  " + arg
        # 使用一个循环，每次从opts中取出一个两元组，赋给两个变量。cmd保存选项参数，arg为附加参数。接着对取出的选项参数进行处理。
        if cmd in ("--projectPath"):
            projectPath = str(arg)
        elif cmd in ("--gerritUser"):
            user = str(arg)
        elif cmd == "--podName":
            podName = str(arg)
        elif cmd == "--branch":
            branch = str(arg)
        elif cmd == "--subPackage":
            subPackage = boolValue(arg)
        elif cmd in ("--version"):
            version = str(arg)
        elif cmd == "--commitId":
            commitId = str(arg)
        elif cmd == "--debug":
            debug = boolValue(arg)
        elif cmd == "--dependencyJSON":
            dependencyJSON = str(arg)
        elif cmd == "--framework":
            framework = boolValue(arg)
        elif cmd == "--archive":
            archive = boolValue(arg)
        elif cmd == "--check":
            check = boolValue(arg)
        elif cmd == "--debugPackage":
            debugPackage = boolValue(arg)
        elif cmd == "--releasePackage":
            releasePackage = boolValue(arg)
        elif cmd == "--autoPush":
            autoPush = boolValue(arg)
        elif cmd == "--autoPushRepo":
            autoPushRepo = boolValue(arg)
        elif cmd == "--repoSource":
            repoSource = str(arg)
        elif cmd == "--resultPath":
            resultPath = str(arg)
        elif cmd == "--whiteListPath":
            whiteListPath = str(arg)
        elif cmd == "--subspecs":
            subspecs = str(arg)
        else:
            printTips()
            returnError()
    for arg in args:
        print arg
    if type == "autoPackage":
        return projectPath, podName, branch, version, subPackage, commitId, dependencyJSON, framework, archive, check, \
               debugPackage, releasePackage, autoPush, autoPushRepo, repoSource, resultPath, whiteListPath, subspecs
    elif type == "init":
        return user, projectPath, subPackage
    elif type == "initSpec":
        return projectPath, podName, subPackage
    elif type == "package":
        return projectPath, podName, version, subPackage, commitId, debug, dependencyJSON
    elif type == "packageA":
        return projectPath, podName, version, subPackage, commitId, debug, dependencyJSON
    elif type == "check":
        return projectPath, podName, dependencyJSON
    else:
        printTips()


def packageFramework(projectPath, podName, version, subPackage, commitId, debug, dependencyJSON, subspecs):
    contentDict = {}
    if subPackage:
        subspecNames = []
        if len(subspecs) == 0:
            subspecNames = subspecList(podName)
        else:
            subspecNames = subspecs
        for subspec in subspecNames:
            content = package(projectPath, podName, subspec, version, commitId, debug, dependencyJSON, subspecNames)
            contentDict[subspec] = content
    else:
        content = package(projectPath, podName, "", version, commitId, debug, dependencyJSON, [])
        contentDict[podName] = content
    return contentDict


def packageArchive(projectPath, podName, version, subPackage, commitId, debug, dependencyJSON, subspecs):
    contentDict = {}
    if subPackage:
        subspecNames = []
        if len(subspecs) == 0:
            subspecNames = subspecList(podName)
        else:
            subspecNames = subspecs
        for subspec in subspecNames:
            content = packageA(projectPath, podName, subspec, version, commitId, debug, dependencyJSON, subspecNames)
            contentDict[subspec] = content
    else:
        content = packageA(projectPath, podName, "", version, commitId, debug, dependencyJSON, [])
        contentDict[podName] = content
    return contentDict


def checkParams(podName, subPackage, whiteListPath, version, subspecs=[], autoPushRepo=False):
    if whiteListPath:
        if str(whiteListPath).endswith("yaml") or str(whiteListPath).endswith("yml"):
            with open(whiteListPath, "r+") as fileReader:
                whiteList = yaml.load(fileReader)
                if podName not in whiteList:
                    formatPrint(podName + "没有在白名单内，请联系开发人员将这个工程加入白名单", " *")
                    exit(1)
        else:
            formatPrint("白名单需要是yaml文件")
            exit(1)
    if version and len(version.split(".")) > 3:
        formatPrint(version + "  输入的版本号不符合规范", " *")
        exit(1)
    if autoPushRepo:
        # 不发版，不检查tag
        returnCode, content = excommandUntilDone("git tag")
        if returnCode > 0:
            formatPrint("获得tag失败", " *")
            returnError()
        if content:
            tagList = content.split("\n")
            tagString = podName + "-" + str(version)
            for tag in tagList:
                if tagString == tag:
                    formatPrint("发现有相同的tag号, 请检查:" + tag, " *")
                    returnError()
    if subPackage:
        allSubspecs = subspecList(podName)
        for subspec in subspecs:
            if subspec in allSubspecs:
                continue
            formatPrint("发现不存在的subspec：" + subspec + ", 请检查", " *")
            returnError()


def checkopts():
    """检测输入参数

    Arguments:
        user {str} -- 用户名
        projectPath {str} -- 项目目录
    """
    if len(sys.argv) == 1:
        printTips()
        returnError()
    arg = sys.argv[1]
    if arg == "env":
        checkEnv()
    elif arg == "version":
        formatPrint(__version__)
    elif arg == "autoPackage":
        projectPath, podName, branch, version, subPackage, commitId, dependencyJSON, framework, archive, check, \
        debugPackage, releasePackage, autoPush, autoPushRepo, repoSource, resultPath, whiteListPath, subspecs = getarguments(arg)
        os.chdir(projectPath)
        autoPackage(projectPath, podName, branch, version, subPackage, commitId, dependencyJSON, framework, archive, check,\
               debugPackage, releasePackage, autoPush, autoPushRepo, repoSource, resultPath, whiteListPath, subspecs)
    elif arg == "init":
        user, projectPath, subPackage = getarguments(arg)
        initProject(user, projectPath, subPackage)
    elif arg == "initSpec":
        projectPath, podName, subPackage = getarguments(arg)
        if not fileExist(projectPath):
            formatPrint("没找到工程目录")
            returnError()
        os.chdir(projectPath)
        initPodspecFile(projectPath, podName, subPackage)
    elif arg == "package":
        projectPath, podName, version, subPackage, commitId, debug, dependencyJSON = getarguments(arg)
        os.chdir(projectPath)
        packageFramework(projectPath,podName, version, subPackage, commitId, debug, dependencyJSON)
    elif arg == "packageA":
        projectPath, podName, subPackage, version, commitId, debug, dependencyJSON = getarguments(arg)
        os.chdir(projectPath)
        packageArchive(projectPath, podName, version, subPackage, commitId, debug, dependencyJSON)
    elif arg == "check":
        projectPath, podName, dependencyJSON = getarguments(arg)
        os.chdir(projectPath)
        checkSpec(podName, dependencyJSON)
    else:
        printTips()


def cleanEnv():
    # type: () -> object
    excommandUntilDone("git add . ; git reset --hard")
    clean_tmp_podspec
    excommandUntilDone("pod repo update lianjia-mobile_ios-lianjia_component_podspec")
    excommandUntilDone("pod repo update lianjia-mobile_ios-LJComponentPodSpecs")

def subspecList(podName):
    """
    获得subspec的列表
    :param podName: pod库名称
    :return:
    """
    podspecDict = getSpecDict(podName)
    subspecNameList = []
    if "subspecs" not in podspecDict.keys():
        formatPrint("没有subspec要打包，如果不需要每个subspec单独打包，请把subPackage设置成false")
        exit(1)
    if podspecDict["subspecs"]:
        for subspec in podspecDict["subspecs"]:
            subspecNameList.append(subspec["name"])
    return byteify(subspecNameList)


def getSpecDict(podName):
    returnCode, content = excommandUntilDone("IS_SOURCE=1 pod ipc spec " + podName + ".podspec")
    contentList = matchList("({.+}$)", content)
    if returnCode > 0 or not contentList:
        formatPrint("podspec 有问题，不能转换成JSON数据")
        returnError()
    specJson = contentList[0]
    specDict = json.loads(specJson)
    return byteify(specDict)


def changeSpec(podName, subPackage=False, version="", commit=""):
    """
    改变podspec，不会创建新的文件
    :param podName: podName
    :param subPackage: 是否要一句subspec打包
    :param version: 版本
    :param commit: commitId
    """
    originSpecPath = podName + ".podspec"
    specDict = getSpecDict(podName)
    specDict = parserDict(specDict, "", version, commit, "{}")
    template = specTemplate(podName, specDict)
    writeToFile(template, podName + ".podspec")


def createSpec(podName, subSpecName="", version="", commit="", dependencyJson="{}"):
    """
    创建新的podspec，会把旧的备份
    :param podName:
    :param subSpecName:
    :param version:
    :param commit:
    :param dependencyJson:
    :return:
    """
    originSpecPath = podName + ".podspec"
    specDict = getSpecDict(podName)
    specDict = parserDict(specDict, subSpecName, version, commit, dependencyJson)
    template = specTemplate(podName, specDict)
    renamePodspec(originSpecPath, originSpecPath+".old")
    writeToFile(template, podName + subSpecName + ".podspec")


def byteify(input):
    # unicode 编码问题
    if isinstance(input, dict):
        return {byteify(key): byteify(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input


def getDependencyDict(dependencyJson="{}"):
    if fileExist(dependencyJson):
        # 文件形式
        dependencyJson = readFile(dependencyJson)
    if dependencyJson == "":
        dependencyJson == "{}"
    dependencyDict = json.loads(dependencyJson)
    return byteify(dependencyDict)


def parserDict(specDict, subSpecName="", version="", commit="", dependencyJson="{}"):
    dependencyDict = getDependencyDict(dependencyJson)
    tmpDict = specDict.copy()
    for key, value in tmpDict.items():
        if version and key == "version":
            specDict["version"] = version
        elif key == "source":
            for sourceKey, sourceValue in value.items():
                if sourceKey == "git":
                    gitList = sourceValue.split("/")
                    sourceValue = "http://gerrit.lianjia.com/" + gitList[-2] + "/" + gitList[-1]
                    specDict["source"]["git"] = sourceValue
                elif sourceKey == "tag":
                    specDict["source"]["tag"] = "s.name.to_s + \"-\" + s.version.to_s"
                if commit:
                    specDict["source"]["commit"] = commit
                    if sourceKey == "tag":
                        del specDict["source"]["tag"]
        elif key == "homepage":
            valueList = value.split("/")
            specDict["homepage"] = "http://git.lianjia.com/" + valueList[-2] + "/" + valueList[-1]
        elif key == "dependencies":
            for podName, versionList in specDict["dependencies"].items():
                if podName not in dependencyDict.keys():
                    continue
                if not isinstance(dependencyDict[podName], list):
                    formatPrint("传的DependencyJson里" + podName + "的依赖不是数组，请检查，这里不做处理。")
                    exit(1)
                specDict["dependencies"][podName] = dependencyDict[podName]
        elif key == "subspecs":
            index = 0
            for subspec in specDict["subspecs"]:
                if "dependencies" not in subspec.keys():
                    continue
                for podName, versionList in subspec["dependencies"].items():
                    if podName not in dependencyDict.keys():
                        continue
                    if not isinstance(dependencyDict[podName], list):
                        formatPrint("传的DependencyJson里" + podName + "的依赖不是数组，请检查，这里不做处理。")
                        continue
                    subspec["dependencies"][podName] = dependencyDict[podName]
                index += 1

    return specDict


def specTemplate(podName, specDict={}):
    if not specDict:
        return
    spec = """#
#  Be sure to run `pod spec lint %(name)s.podspec' to ensure this is a
#  valid spec and to remove all comments including this before submitting the spec.
#
#  To learn more about Podspec attributes see http://docs.cocoapods.org/specification.html
#  To see working Podspecs in the CocoaPods repo see https://github.com/CocoaPods/Specs/
#

Pod::Spec.new do |s|

  # ―――  Spec Metadata  ―――――――――――――――――――――――――――――――――――――――――――――――――――――――――― #
  #
  #  These will help people to find your library, and whilst it
  #  can feel like a chore to fill in it's definitely to your advantage. The
  #  summary should be tweet-length, and the description more in depth.
  #

  s.name         = "%(name)s"
  s.version      = "%(version)s"
  s.summary      = "%(summary)s"

  # This description is used to generate tags and improve search results.
  #   * Think: What does it do? Why did you write it? What is the focus?
  #   * Try to keep it short, snappy and to the point.
  #   * Write the description between the DESC delimiters below.
  #   * Finally, don't worry about the indent, CocoaPods strips it!
  s.description  = <<-DESC
  %(description)s
                   DESC
""" % specDict
    if "homepage" in specDict.keys():
        spec += setProperty("s", "homepage", "=", specDict["homepage"], 1)
    if "screenshots" in specDict.keys():
        spec += setProperty("s", "screenshots", "=", specDict["screenshots"], 1)
    if "documentation_url" in specDict.keys():
        spec += setProperty("s", "documentation_url", "=", specDict["documentation_url"], 1)
    if "license" in specDict.keys():
        spec += setProperty("s", "license", "=", specDict["license"], 1, True)
    if "authors" in specDict.keys():
        spec += setProperty("s", "author", "=", specDict["authors"], 1, True)
    if "source" in specDict.keys():
        spec += setProperty("s", "source", "=", specDict["source"], 1, True)
    if "social_media_url" in specDict.keys():
        spec += setProperty("s", "social_media_url", "=", specDict["social_media_url"], 1)
    if "cocoapods_version" in specDict.keys():
        spec += setProperty("s", "cocoapods_version", "=", specDict["cocoapods_version"], 1)
    if "platforms" in specDict.keys():
        spec += target("s", specDict["platforms"], 1)
    if "prepare_command" in specDict.keys():
        spec += setProperty("s", "prepare_command", "=", specDict["prepare_command"], 1)
    if "prefix_header_contents" in specDict.keys():
        spec += setProperty("s", "prefix_header_contents", "=", specDict["prefix_header_contents"], 1)
    spec +="""
  s.preserve_paths = "%(name)s/Classes/**/*", "%(name)s/Assets/**/*", "%(name)s/Framework/**/*", "%(name)s/Archive/**/*"

  configuration = "Release"
  if ENV["IS_DEBUG"] || ENV["%(name)s_DEBUG"]
    configuration = "Debug"
  elsif ENV["IS_RELEASE"] || ENV["%(name)s_Relase"]
    configuration = "Release"
  end
 
  if ENV['IS_SOURCE'] || ENV["%(name)s_SOURCE"]
    # 源码部分，请在这里写上必要的。
""" % specDict
    dependenceLibraries = []
    dependenceFrameworks = []
    if "default_subspecs" in specDict.keys():
        spec += setProperty("s", "default_subspecs", "=", specDict["default_subspecs"], 2)
    if "subspecs" in specDict.keys():
        spec += setSubspecs(podName, specDict["subspecs"], dependenceLibraries, dependenceFrameworks, 2)
    if "source_files" in specDict.keys():
        spec += setProperty("s", "source_files", "=", specDict["source_files"], 2)
    if "public_header_files" in specDict.keys():
        spec += setProperty("s", "public_header_files", "=", specDict["public_header_files"], 2)
    if "vendored_libraries" in specDict.keys():
        spec += setProperty("s", "vendored_libraries", "=", specDict["vendored_libraries"], 2)
        dependenceLibraries.extend(toList(specDict["vendored_libraries"]))
    if "vendored_frameworks" in specDict.keys():
        spec += setProperty("s", "vendored_frameworks", "=", specDict["vendored_frameworks"], 2)
        dependenceFrameworks.extend(toList(specDict["vendored_frameworks"]))
    spec += """
  elsif ENV['IS_ARCHIVE'] || ENV["%(name)s_ARCHIVE"]
    s.public_header_files = "%(name)s/Archive/#{configuration}/*.h"
    s.source_files = "%(name)s/Archive/#{configuration}/*.h"
    """ % specDict
    originLibrary = "%(name)s/Archive/#{configuration}/lib%(name)s.a" % specDict
    libraries = []
    libraries.extend(dependenceLibraries)
    libraries.append(originLibrary)
    frameworks = []
    frameworks.extend(dependenceFrameworks)
    if libraries:
        uniqueLibraries = {}.fromkeys(libraries).keys()
        spec += setProperty("s", "vendored_libraries", "=", uniqueLibraries, 2)
    if frameworks:
        uniqueFrameworks = {}.fromkeys(frameworks).keys()
        spec += setProperty("s", "vendored_frameworks", "=", uniqueFrameworks, 2)
    if "subspecs" in specDict.keys():
        for subspec in specDict["subspecs"]:
            if "dependencies" not in subspec.keys():
                continue
            spec += setDependencies(podName, "s", subspec["dependencies"], 2)
    spec += """
  else
    s.public_header_files = "%(name)s/Framework/#{configuration}/%(name)s.framework/Headers/*.h"
    s.source_files = "%(name)s/Framework/#{configuration}/%(name)s.framework/Headers/*.h" """ % specDict
    originFramework = "%(name)s/Framework/#{configuration}/%(name)s.framework" % specDict
    frameworks = []
    frameworks.extend(dependenceFrameworks)
    frameworks.append(originFramework)
    libraries = []
    libraries.extend(dependenceLibraries)
    if libraries:
        uniqueLibraries = {}.fromkeys(libraries).keys()
        spec += setProperty("s", "vendored_libraries", "=", uniqueLibraries, 2)
    if frameworks:
        uniqueFrameworks = {}.fromkeys(frameworks).keys()
        spec += setProperty("s", "vendored_frameworks", "=", uniqueFrameworks, 2)
    if "subspecs" in specDict.keys():
        for subspec in specDict["subspecs"]:
            if "dependencies" not in subspec.keys():
                continue
            spec += setDependencies(podName, "s", subspec["dependencies"], 2)
    spec += setEnd("end", 1)
    spec +="""
  # ――― Resources ―――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――― #
  #
  #  A list of resources included with the Pod. These are copied into the
  #  target bundle with a build phase script. Anything else will be cleaned.
  #  You can preserve files from being cleaned, please don't preserve
  #  non-essential files like tests, examples and documentation.
  #

  # s.resource  = "icon.png"
  # s.resources = "Resources/*.png"
    """
    if "static_framework" in specDict.keys():
        spec += setProperty("s", "static_framework", "=", specDict["static_framework"], 1)
    if "deprecated" in specDict.keys():
        spec += setProperty("s", "deprecated", "=", specDict["deprecated"], 1)
    if "deprecated_in_favor_of" in specDict.keys():
        spec += setProperty("s", "deprecated_in_favor_of", "=", specDict["deprecated_in_favor_of"], 1)
    if "resources" in specDict.keys():
        spec += setProperty("s", "resources", "=", specDict["resources"], 1)
    if "resource_bundles" in specDict.keys():
        spec += setProperty("s", "resource_bundles", "=", specDict["resource_bundles"], 1)
    spec += """
  # ――― Project Linking ―――――――――――――――――――――――――――――――――――――――――――――――――――――――――― #
  #
  #  Link your library with frameworks, or libraries. Libraries do not include
  #  the lib prefix of their name.
  #
  # 公共部分，比如公共资源类。framework等
  # s.framework  = "SomeFramework"
  # s.frameworks = "SomeFramework", "AnotherFramework" """
    if "frameworks" in specDict.keys():
        spec += setProperty("s", "frameworks", "=", specDict["frameworks"], 1)
    if "weak_frameworks" in specDict.keys():
        spec += setProperty("s", "weak_frameworks", "=", specDict["weak_frameworks"], 1)
    spec +="""
  # s.library   = "iconv"
  # s.libraries = "iconv", "xml2" """
    if "libraries" in specDict.keys():
        spec += setProperty("s", "libraries", "=", specDict["libraries"], 1)
    if "compiler_flags" in specDict.keys():
        spec += setProperty("s", "compiler_flags", "=", specDict["compiler_flags"], 1)
    spec += """
  # ――― Project Settings ――――――――――――――――――――――――――――――――――――――――――――――――――――――――― #
  #
  #  If your library depends on compiler flags you can set them in the xcconfig hash
  #  where they will only apply to your library. If you depend on other Podspecs
  #  you can include multiple dependencies to ensure it works."""
    if "requires_arc" in specDict.keys():
        spec += setProperty("s", "requires_arc", "=", specDict["requires_arc"], 1)
    if "module_map" in specDict.keys():
        spec += setProperty("s", "module_map", "=", specDict["module_map"], 1)
    if "xcconfig" in specDict.keys():
        spec += setProperty("s", "xcconfig", "=", specDict["xcconfig"], 1)
    if "pod_target_xcconfig" in specDict.keys():
        spec += setProperty("s", "pod_target_xcconfig", "=", specDict["pod_target_xcconfig"], 1)
    if "user_target_xcconfig" in specDict.keys():
        spec += setProperty("s", "user_target_xcconfig", "=", specDict["user_target_xcconfig"], 1)
    if "dependencies" in specDict.keys():
        spec += setDependencies(podName, "s", specDict["dependencies"], 1)
    spec += setEnd("end")
    return spec

def target(name, platforms, hierarchy=0):
    if not isinstance(platforms, dict):
        formatPrint("s.platforms 格式不对")
        exit(1)
    spec = ""
    for key ,platform in platforms.items():
        spec += setProperty(name, key + ".deployment_target", "=", platforms[key], hierarchy)
    return spec

def setSubspecs(podName, subspecs, dependenceLibraries, dependenceFrameworks, hierarchy=0, oneLine=False):
    spec = ""
    subHierarchy = hierarchy + 1
    for subspec in subspecs:
        lowerName = str(subspec["name"]).lower()
        spec += setSubspecTitle("s", subspec["name"], hierarchy)
        if "subspecs" in subspec.keys():
            spec += setSubspecs(podName, subspec, dependenceLibraries, dependenceFrameworks, subHierarchy)
        if "public_header_files" in subspec.keys():
            spec += setProperty(lowerName, "public_header_files", "=", subspec["public_header_files"], subHierarchy)
        if "source_files" in subspec.keys():
            spec += setProperty(lowerName, "source_files", "=", subspec["source_files"], subHierarchy)
        if "dependencies" in subspec.keys():
            spec += setDependencies(podName, lowerName, subspec["dependencies"], subHierarchy)
        if "vendored_libraries" in subspec.keys():
            spec += setProperty(lowerName, "vendored_libraries", "=", subspec["vendored_libraries"], subHierarchy)
            dependenceLibraries.extend(toList(subspec["vendored_libraries"]))
        if "vendored_frameworks" in subspec.keys():
            spec += setProperty(lowerName, "vendored_frameworks", "=", subspec["vendored_frameworks"], subHierarchy)
            dependenceFrameworks.extend(toList(subspec["vendored_frameworks"]))
        if "resources" in subspec.keys():
            spec += setProperty(lowerName, "resources", "=", subspec["resources"], subHierarchy)
        if "resource_bundles" in subspec.keys():
            spec += setProperty(lowerName, "resource_bundles", "=", subspec["resource_bundles"], subHierarchy)
        if "frameworks" in subspec.keys():
            spec += setProperty(lowerName, "frameworks", "=", subspec["frameworks"], subHierarchy)
        if "libraries" in subspec.keys():
            spec += setProperty(lowerName, "libraries", "=", subspec["libraries"], subHierarchy)
        if "module_map" in subspec.keys():
            spec += setProperty(lowerName, "module_map", "=", subspec["module_map"], subHierarchy)
        if "pod_target_xcconfig" in subspec.keys():
            spec += setProperty("s", "pod_target_xcconfig", "=", subspec["pod_target_xcconfig"], subHierarchy)
        spec += setEnd("end", hierarchy)
    return spec


def toList(value):
    if isinstance(value, str) or isinstance(value, unicode):
        return [value]
    elif isinstance(value, list):
        return value
    else:
        formatPrint("其他类型不能转数组")
        exit(1)

def setSubspecTitle(name, subName="", hierarchy=0):
    lowerName = subName.lower()
    spec ="""
%(hierarchys)s%(names)s.subspec '%(subNames)s' do |%(lowerNames)s|""" % {"hierarchys": "  " * hierarchy, "names": name, "subNames": subName, "lowerNames": lowerName}
    return spec

def setDependencies(podName, lowerName, dependencyDict, hierarchy=0):
    spec = ""
    for dependenceName, versionList in dependencyDict.items():
        nameAndVersions = [dependenceName]
        nameAndVersions.extend(versionList)
        if podName in dependenceName:
            continue
        spec += setProperty(lowerName, "dependency", "", nameAndVersions, hierarchy)
    return spec


def setEnd(name, hierarchy=0, oneLine=False):
    spec = ""
    if not oneLine:
        spec += "\n"
    spec += """%(hierarchys)s%(names)s
    """ % {"hierarchys": "  " *hierarchy, "names": name}
    return spec

def setProperty(name, property, operator, value, hierarchy=0, oneLine=False):
    spec = """
%(hierarchys)s%(name)s.%(property)-10s %(operator)s %(values)s""" % {"hierarchys":"  " * hierarchy, "name":name, "property":property, "operator":operator, "values":stringValue(value, hierarchy, oneLine)}
    return spec


def stringValue(values, hierarchy=0, oneline=False):
    keywords = ["type", "file", "text", "git", "svn", "hg", "http", "revision", "tag", "submodules"]
    result = ""
    if isinstance(values, str) or isinstance(values, unicode):
        if values in keywords:
            result = ":" + str(values)
        elif values == "s.name.to_s + \"-\" + s.version.to_s":
            result = str(values)
        else:
            result = "\"" + str(values) + "\""
    elif isinstance(values, bool):
        result = str(values).lower()
    elif isinstance(values, list):
        for value in values:
            result += stringValue(value, hierarchy) + ", "
        result = result.rstrip(", ")
        return result
    elif isinstance(values, dict):
        result = "{"
        if not oneline:
            result += "\n"
        else:
            hierarchy = 0
        tmp = ""
        for key, value in values.items():
            if isinstance(value, list):
                tmp += "  " * (hierarchy + 1) + stringValue(key) + " => [" + stringValue(value, hierarchy) + "],"
            else:
                tmp += "  " * (hierarchy + 1) + stringValue(key) + " => " + stringValue(value, hierarchy) + ","
            if not oneline:
                tmp += "\n"
        tmp = tmp.rstrip(",\n")
        result += tmp
        result += setEnd("}", hierarchy, oneline)
    return result


def initPodspecFile(projectPath, podName, subPackage):
    # changeSpec(podName, subPackage)
    originSpecPath = projectPath + "/" + podName + ".podspec"
    content = readFile(originSpecPath)
    sourceList = matchList("(s.source_files += +[\'|\"].*?[\'|\"])", content)
    publicHeaderList = matchList("(s.public_header_files += +[\"|\'].*?[\"|\'])", content)
    replaceContent = ""
    if sourceList:
        if publicHeaderList:
            replaceContent = content.replace(publicHeaderList[0], "", 1)
        sourceKey = sourceList[0]
        formatPrint("即将替换" + sourceKey)
        if subPackage:
            replaceContent = content.replace(sourceKey, packageBySubspec, 1)
        else:
            replaceContent = content.replace(sourceKey, noSubSpec, 1)
    else:
        formatPrint("错误，没有找到关键字source_files ，可能已经完成替换或者其他的未知错误")
        returnError()
    writeToFile(replaceContent, originSpecPath)


def main():
    # 调用接口
    formatPrint("当前版本:"+ __version__, " &")
    checkopts()


if __name__ == "__main__":
    sys.exit(checkopts())
