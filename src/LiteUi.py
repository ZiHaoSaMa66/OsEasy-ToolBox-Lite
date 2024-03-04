

import flask
from flask import request,render_template
import webbrowser
from remain import *
import logging

server = flask.Flask(__name__)

from multiprocessing import freeze_support
# 启动守护进程 B溃修复支持

Numver = "Lite 1.0"
BackNumver = "1.6RC4+ - Lite"

# @server.route("/func",methods=['get'])
# def runfunc():
#     pass

@server.route("/func/gfw",methods=['get'])
def stop_start_gfw():
    MMPC_shutdown_start_chufa()
    return "200"
    
@server.route("/func/reBootStudent",methods=['get'])
def bootStudent():
    selfunc_g4("TypeError")
    return "200"


@server.route("/func/shift_tihuan",methods=['get'])
def web_shift_tihuan():
    selfunc_g1("TypeError")
    return "200"


@server.route("/func/guaqi",methods=['get'])
def runguaqi_func():
    fdb = guaqi_student_loj()
    return fdb


@server.route("/func/shjc",methods=['get'])
def run_shouhujc_func():
    # startprotect()
    run_waibu_protect_loj() # 启动守护进程的逻辑函数
    return "OK"

@server.route("/func/openTool",methods=['get'])
def openTools():
    selfunc_g8("typeerror")
    return "200"


# Page2

@server.route("/func/delbat",methods=['get'])
def web_delbat():
    selfunc_g0("typeerror")
    return "200"

@server.route("/func/delkbl_mtc",methods=['get'])
def web_delkbl_mtc():
    selfunc_g3(need_shutdown=True)
    return "200"

@server.route("/func/only_delmtc",methods=['get'])
def web_only_delmtc():
    selfunc_g3(need_shutdown=False)
    return "200"

@server.route("/func/restone_all",methods=['get'])
def web_restone_all():
    selfunc_g5("typeerror")
    return "200"

@server.route("/func/restone_mtc",methods=['get'])
def web_restone_mtc():
    restoneMutClient("typeerror")
    return "200"

@server.route("/func/unlock_net",methods=['get'])
def web_unlock_net():
    selfunc_g7()
    return "200"

@server.route("/func/unlock_usb",methods=['get'])
def web_unlock_usb():
    #预留功能函数
    return "404"
    
# TypeError: The view function did not return a valid response. 
# The return type must be a string, dict, list, tuple with headers or status, 
# Response instance, or WSGI callable, but it was a int.

@server.route("/github",methods=['get'])
def run_opengithub():
    opengithubres_Lite()
    return "OK"


# Return_vaule = ""

#Page3

@server.route("/func/replaceSCR",methods=['get'])
def web_replaceSCR():
    # replace_ScreenRender()
    begin_a_child_progress(replace_ScreenRender)
    return "200"
    
@server.route("/func/RunWincmd",methods=['get'])
def web_RunWincmd():
    r = get_yuancheng_cmd()
    if r==None:
        ZiHao_logger.error("未拦截到控制命令参数")
    else:
        bcmd = build_run_srcmd(YC_command=r)
        runcmd(bcmd)
    return "None"

@server.route("/func/RunFullWincmd",methods=['get'])
def web_RunFullWincmd():
    get = get_key_value(Open_KJJ_SCR)
    ZiHao_logger.debug(get)
    if get ==False:
        ZiHao_logger.warn("未开启快捷键杀广播进程 - 尝试运行的操作已拦截...")
        return "Faild"
    else:
        r = get_yuancheng_cmd()
        if r==None:
            ZiHao_logger.error("未拦截到控制命令参数")
            return "Faild"
        else:
            cmd = r.replace("#fullscreen#:0","#fullscreen#:1")
            bcmd = build_run_srcmd(YC_command=cmd)
            runcmd(bcmd)
    return "None"

@server.route("/func/killscr",methods=['get'])
def web_kill_scr():
    runcmd("taskkill /f /t /im ScreenRender_Y.exe")
    runcmd("taskkill /f /t /im ScreenRender.exe")

    return "200"

@server.route("/func/restoneSCR",methods=['get'])
def web_restoneSCR():
    begin_a_child_progress(restone_ScreenRender)
    return "200"

@server.route("/func/kjj_killsc",methods=['get'])
def web_kjj_killsc():
    kjj_open_loj("SCR")
    return "200"

@server.route("/func/kjj_runfullsc",methods=['get'])
def web_kjj_runfullsc():
    kjj_open_loj("FullSC")

    return "200"

@server.route("/func/saveYCcmd",methods=['get'])
def web_saveYCcmd():
    save_now_yccmd()
    ZiHao_logger.success("已保存命令至程序运行目录下")
    return "200"

@server.route("/guangbo",methods=['POST'])
def web_upate_yc_cmd():
    yc_cmd = request.values.get('yc_cmd')
    handin_save_yc_cmd(yc_cmd)
    ZiHao_logger.debug(f"wirte yccmd > {yc_cmd}")
    return page3()
    
#最后也要至少返回一个值回来...

#TypeError: The view function for 'web_RunWincmd' did not return a valid response. 
# The function either returned None or ended without a return statement.


# @server.route("/get_mmc_status",methods=['get'])
# def get_mmc_status():
#     pass

# @server.route("/")
# def 
@server.route('/')
def index():
    return render_template("ToolBox.html",GUI_ver=Numver)

@server.route('/ToolBox')
def index2():
    return render_template("ToolBox.html",GUI_ver=Numver)

@server.route('/Progress')
def page1():

    t1,t2,t3=get_progress_word()
    
    datatran = {
        
        "gfw_status": t1,
        "Protect_status": t2,
        "guaqi_status": t3
    }
    
    return render_template("ProGress.html",**datatran)

@server.route('/other')
def page2():

    return render_template("other.html")



@server.route('/guangbo')
def page3():
    
    # nowtime = time.time()

    
    # share_name.reflashDefault()
    
    # ZiHao_logger.debug(f"Main Return_value > {share_name.Return_value}")
    # if share_name.Return_value != None:
    #     # loj fix TypeError: can only concatenate str (not "NoneType") to str
    #     Return_value_mix = share_name.Return_value
    # else:
    #     Return_value_mix = None
        
    scjjc,fullsc,yccmd_word = get_guangbo_words()

    data_tran = {
        
        # "function_feedback": Return_value_mix,
        "kill_sc_kjj_status": scjjc,
        "runFull_sc_kjj_status": fullsc,
        "alreadyget_cmd": yccmd_word
    }

    return render_template("guangbo.html",**data_tran)

# print("轻量版工具箱!启动!...")

if __name__ == '__main__':
    
    freeze_support()
    
    log = logging.getLogger('werkzeug')
    log.disabled = True
    ZiHao_logger.info("OsEasyToolBox-Lite 欢迎回来sa~")
    ZiHao_logger.success(f"当前工具箱版本为 {Numver}")
    # print(f"后端分支版本 {}")
    ZiHao_logger.success("工具箱界面地址 > http://127.0.0.1:22330/")
    webbrowser.open("http://127.0.0.1:22330/ToolBox")
    server.run(host='127.0.0.1',port=22330)