# import hmac
import os, time
from datetime import datetime
# from tkinter.messagebox import *
import pygetwindow as gw
import webbrowser
import ctypes
import sys
import psutil
import pyautogui

# import wmi
# from mainv3 import Ui

from multiprocessing import Process,Queue
import signal

from pynput import keyboard

bkppath = "C:\\Backups"

cmdpath = "C:\\Users\\Administrator\\prod"

_loginpj = "C:\\Users\\Administrator\\temp\\rod\\"
loginpj = "C:\\Users\\Administrator\\temp\\rod\\passv2.txt"

oseasypath = "C:\\Program Files (x86)\\Os-Easy\\os-easy multicast teaching system\\"

path_zidingyi_fort = "C:\\Users\\Administrator\\temp\\rod\\path_fort.txt"
path_zidingyi_bg = "C:\\Users\\Administrator\\temp\\rod\\path_bg.txt"
path_zidingyi_yiyan = "C:\\Users\\Administrator\\temp\\rod\\path_yiyan.txt"




class Logger():
    '''日志记录器'''

    def __init__(self) -> None:
        
        self.debug_mode = True
        # 展示DEBUG 等级的日志
        self.save_log = False
        # 保存日志文件至 运行目录
        
        self.curtpath = os.getcwd().replace("\\", "/")
        
        logfilename = self.get_logfilename()
        self.logpath = self.curtpath + "/" + logfilename + ".log"
                
        pass
    def info(self,log:str):
        times = self.get_logtime_str()
        lognr = f"{times} > [INFO] {log}"
        print(lognr)
        self.savelog(lognr)

    def debug(self,log:str):

        times = self.get_logtime_str()
        lognr = f"{times} > [DEBUG] {log}"
        self.savelog(lognr)
        if self.debug_mode ==True:
            print(lognr)

    def warn(self,log:str):
        times = self.get_logtime_str()
        lognr = f"{times} > [WARN] {log}"
        print(lognr)
        self.savelog(lognr)
        pass
    def error(self,log:str):
        times = self.get_logtime_str()
        lognr = f"{times} > [ERR] {log}"
        print(lognr)
        self.savelog(lognr)
        pass
    def success(self,log:str):
        times = self.get_logtime_str()
        lognr = f"{times} > [SUCCESS] {log}"
        print(lognr)
        self.savelog(lognr)
        pass

    def get_logtime_str(self):
        '''返回一个时间字符串'''
        time_str = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        return time_str

    def get_logfilename(self):
        time_str = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        return time_str

    def savelog(self,log:str):
        '''保存日志到日志文件中'''
        if self.save_log==True:
            fm = open(self.logpath,"a") 
            # 模式 'a' 表示以追加（append）的方式打开文件，如果文件不存在则会创建文件。
            log += "\n"
            fm.write(log)
            fm.close()
        
        
ZiHao_logger = Logger()




class Share_Name():
    '''共享变量名'''
    def __init__(self) -> None:
        self.replaceSCR = None
        self.Return_value = None
        self.curtpath = os.getcwd().replace("\\", "/")
        self.temp_path = self.curtpath + "/" + "hc" + ".temp"
        
        pass
    def save(self,name,vaule):
        eval(f"share_name.{name} = {vaule}")
        pass
    
    def saveDefault_in_mtprogress(self,value):
        # eval(f"share_name.Return_value = {vaule}")
        # ZiHao_logger.debug(f"try run func to save {value}")
        # setattr(share_name, "Return_value", value)
        #gpt
        # self.Return_value = value
        
        #下下策了 实在是难蚌了
        fm = open(self.temp_path,"w")
        save_str = ZiHao_logger.get_logtime_str()
        save_str += f" {value}"
        fm.write(save_str)
        fm.close()
        
        pass
    # def get(self,name):
        # pass
    def reflashDefault(self):
        try:
        
            fm = open(self.temp_path,"r")
            # fm.write(value)
            value = fm.read()
            setattr(share_name, "Return_value", value)
            fm.close()
            os.remove(self.temp_path)
        except FileNotFoundError:
            pass
        pass
    
share_name = Share_Name()


RunBoxKiller = False

RunProtectCMD = False

MMPCServRun = True

GuaQi_Status = False

os.makedirs(cmdpath,mode=0o777,exist_ok=True)
os.makedirs(bkppath,mode=0o777,exist_ok=True)
os.makedirs(_loginpj,mode=0o777,exist_ok=True)

temp_get = None

def get_key_value(key):
    '''获取key在后端remain的变量值'''
    global temp_get
    # eval(f"temp_get={key}")
    # exec(f"temp_get={key}")
    temp_get=key
    ZiHao_logger.debug(f"temp_get > {temp_get}")
    return temp_get


def get_guangbo_words():
    '''获取广播页状态关键字'''
    global Open_KJJ_SCR,Open_KJJ_FullSC
    fl = []
    il = [Open_KJJ_SCR,Open_KJJ_FullSC]
    for i in il:
        if i ==False:
            fl.append("未开启")
        else:
            fl.append("正在监听")
    
    
    
    yccmd_status = get_yuancheng_cmd()
    if yccmd_status ==None:
        fdbyc = "无拦截命令缓存"
    else:
        fdbyc = "已获取到拦截命令"
    return fl[0],fl[1],fdbyc
    pass

def SCR_on_press(key):
    '''用于检测快捷键杀SCR_Y进程'''
    global SCR_Press_Alt,SCR_Press_K
    if key == keyboard.KeyCode(char="K") or key == keyboard.KeyCode(char="k"):
        SCR_Press_K = True
    if key == keyboard.Key.alt or key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
        SCR_Press_Alt = True

    if SCR_Press_Alt and SCR_Press_K:
        SCR_Press_Alt = SCR_Press_K = False #重置按键按下状态
        # get_scshot()
        runcmd("taskkill /f /t /im ScreenRender_Y.exe")
        runcmd("taskkill /f /t /im ScreenRender.exe")


def FullSC_on_press(key):
    '''用于快捷键运行全屏控制窗口'''
    global FullSC_Press_Alt,FullSC_Press_Ctrl,FullSC_Press_F,Open_KJJ_SCR

    if key == keyboard.KeyCode(char="F") or key == keyboard.KeyCode(char="f"):
        FullSC_Press_F = True
    if key == keyboard.Key.alt or key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
        FullSC_Press_Alt = True
    if key ==keyboard.Key.ctrl or key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        FullSC_Press_Ctrl = True
    
    if FullSC_Press_Alt and FullSC_Press_F and FullSC_Press_Ctrl:
        FullSC_Press_Ctrl = FullSC_Press_Alt = FullSC_Press_F = False
        #重置按键状态
        # if RunFullSC_swc.value ==False:
        if Open_KJJ_SCR ==False:
            # show_snakemessage("警告！ 未开启快捷键杀广播进程\n尝试运行的操作已拦截....")
            # return "警告！ 未开启快捷键杀广播进程\n尝试运行的操作已拦截...."
            ZiHao_logger.warn("未开启快捷键杀广播进程 - 尝试运行的操作已拦截....")
            # share_name.saveDefault_in_mtprogress("未开启快捷键杀广播进程 尝试运行的操作已拦截....")
            pass
        else:
            status = get_yuancheng_cmd()
            if status ==None:
                pass
                ZiHao_logger.error("未拦截到控制命令参数")
                share_name.saveDefault_in_mtprogress("未拦截到控制命令参数")
                # return "未拦截到控制命令参数"
                # show_snakemessage("未拦截到控制命令参数")
            else:
                
                cmd = status.replace("#fullscreen#:0","#fullscreen#:1")
                builded = build_run_srcmd(cmd)
                # Fix 潜在的失败问题
                # print("DEBUG with build cmd",builded)
                runcmd(builded)
                # Fix 黑框
                return None

SCR_Press_K = False
SCR_Press_Alt = False


FullSC_Press_F = False
FullSC_Press_Alt = False
FullSC_Press_Ctrl = False

Open_KJJ_FullSC = False
Open_KJJ_SCR = False

RunFullSC_listener = keyboard.Listener(on_press=FullSC_on_press)

KillSCR_listener = keyboard.Listener(on_press=SCR_on_press)

def kjj_open_loj(wich_kjj:str):
    '''打开/关闭快捷键的逻辑触发函数'''
    global Open_KJJ_SCR,Open_KJJ_FullSC,RunFullSC_listener,KillSCR_listener
    
    # ZiHao_logger.debug(f"exc scr > {Open_KJJ_SCR} fullsc {Open_KJJ_FullSC}")
    
    if wich_kjj=="SCR":
        
        
        if Open_KJJ_SCR==False:
            # ZiHao_logger.debug(f"exc2 scr > {Open_KJJ_SCR} fullsc {Open_KJJ_FullSC}")

            Open_KJJ_SCR = True
            KillSCR_listener.run()
            # ZiHao_logger.debug(f"exc3 scr > {Open_KJJ_SCR} fullsc {Open_KJJ_FullSC}")
        elif Open_KJJ_SCR==True:
            
            Open_KJJ_SCR = False
            KillSCR_listener.stop()


    elif wich_kjj =="FullSC":
        
        if Open_KJJ_FullSC==False:
            
            Open_KJJ_FullSC = True
            RunFullSC_listener.run()
            
        elif Open_KJJ_FullSC==True:
            
            Open_KJJ_FullSC = False
            RunFullSC_listener.stop()
        
        pass

def guaqi_student_loj():
    '''挂起学生端的逻辑触发函数'''
    global GuaQi_Status
    ZiHao_logger.debug(f"Runed guqistatus > {GuaQi_Status}")
    if GuaQi_Status==False:
        fdb = guaqi_process("Student.exe")
        if fdb ==True:
            GuaQi_Status=True
            return "200"
        else:
            GuaQi_Status=False
            return f"挂起进程异常:{fdb}"
    else:
        fdb = huifu_process("Student.exe")
        if fdb ==True:
            GuaQi_Status=False
            return "200"
        else:
            GuaQi_Status=False
            return f"恢复挂起进程异常:{fdb}"

def get_progress_word():
    global RunProtectCMD,GuaQi_Status
    
    # print("Runed Get word guaqi >",GuaQi_Status)
    
    mmpc_code = check_MMPC_status()
    if mmpc_code==True:
        mmpc_text = "正在运行"
    else:
        mmpc_text = "未运行!"
    
    if RunProtectCMD==False:
        pro_text = "未运行"
    else:
        pro_text = "正在运行"
    
    if GuaQi_Status==True:
        GuaQi_text = "已挂起"
    else:
        GuaQi_text = "未挂起"
    
    return mmpc_text,pro_text,GuaQi_text






def replace_ScreenRender():
        '''替换原有scr用于拦截远程命令'''
        global bkppath,oseasypath
        filename = "ScreenRender_Helper.exe"
        # oepath = oseasypath + filename
        # needbkpath =  bkppath + "\\" + filename
        # runcmd(f'copy "{needbkpath}" "{oepath}"')
        nowrunpath = os.getcwd()
        nowcurhelper = nowrunpath + "\\" + filename
        
        copypath = oseasypath + filename
        
        # print("DEBUG > nowcurhelper",nowcurhelper)
        
        onetime_protectcheck()
        try:
            fm = open(nowcurhelper,'r') 
            # 检查ScreenRender_Helper.exe是否与工具箱处在同一目录
            fm.close()
        except FileNotFoundError:
            ZiHao_logger.error("ScreenRender_Helper.exe需要与工具箱处在同一目录")
            # share_name.saveDefault_in_mtprogress("ScreenRender_Helper.exe需要与工具箱处在同一目录")
            # share_name.Return_value = "ScreenRender_Helper.exe需要与工具箱处在同一目录"
            ZiHao_logger.debug(f"in func save > {share_name.Return_value}")
            return False

        ZiHao_logger.info("对原有程序重命名")
        runcmd('rename "C:\Program Files (x86)\Os-Easy\os-easy multicast teaching system\ScreenRender.exe" "ScreenRender_Y.exe"')
        time.sleep(2.5)
        # 将原有应用重命名
        ZiHao_logger.info("执行复制命令")
        # print(nowcurhelper)
        # print(copypath)
        runcmd(f'copy "{nowcurhelper}" "{copypath}"')
        # woc 哥们我真服了 双引号tmd漏一个
        time.sleep(2.5)
        # 复制拦截程序
        ZiHao_logger.info("为拦截程序重命名")
        runcmd('rename "C:\Program Files (x86)\Os-Easy\os-easy multicast teaching system\ScreenRender_Helper.exe" "ScreenRender.exe"')
        #将拦截程序重命名
        # share_name.saveDefault_in_mtprogress("理论上已经替换完成 可自行检查替换结果")
        ZiHao_logger.success("理论上已经替换完成 可自行检查替换结果")
        # share_name.Return_value = ""
        return True




def restone_ScreenRender():
    '''还原原有的ScreenRender'''
    
    onetime_protectcheck()
    path = "C:\Program Files (x86)\Os-Easy\os-easy multicast teaching system\ScreenRender.exe"
    check_path = "C:\Program Files (x86)\Os-Easy\os-easy multicast teaching system\ScreenRender_Y.exe"
    
    a = check_tihuan_SCRY_status()
    if a==False:
        ZiHao_logger.error("ScreenRender_Helper.exe需要与工具箱处在同一目录")
        return False

    try:
        os.remove(path)
    except FileNotFoundError:
        pass
    runcmd('rename "C:\Program Files (x86)\Os-Easy\os-easy multicast teaching system\ScreenRender_Y.exe" "ScreenRender.exe"')
    ZiHao_logger.success("理论上已还原完成 可自行检查结果")
    return True


def get_yuancheng_cmd():
    '''从文件中读取拦截到的远程命令\n
    未读取到返回None'''
    getpath = cmdpath + "\\SCCMD.txt"
    try:
        fm = open(getpath,'r')
        cmd = fm.read()
        fm.close()
        return cmd
    except FileNotFoundError:
        return None

# "C:\Program Files (x86)\Os-Easy\os-easy multicast teaching system\ScreenRender.exe" {#decoderName#:#h264#,#fullscreen#:0,#local#:#172.18.36.132#,#port#:7778,#remote#:#229.1.36.200#,#teacher_ip#:0,#verityPort#:7788}

def handin_save_yc_cmd(save_cmd):
    '''开发者选项 - 手动保存拦截的命令'''
    global cmdpath
    getpath = cmdpath + "\\SCCMD.txt"

    fm = open(getpath,"w")
    fm.write(str(save_cmd))
    fm.close()

def build_run_srcmd(YC_command):
    '''构造执行显示命令'''
    status = check_tihuan_SCRY_status()
    if status==True:
        fdb = f'"C:\Program Files (x86)\Os-Easy\os-easy multicast teaching system\ScreenRender_Y.exe" {YC_command}'
        return fdb
    else:
        fdb = f'"C:\Program Files (x86)\Os-Easy\os-easy multicast teaching system\ScreenRender.exe" {YC_command}'
        return fdb

def save_now_yccmd():
    '''开发者选项 - 保存现在获取到的远程指令到程序目录'''
    getpath = cmdpath + "\\SCCMD.txt"
    savepath = os.getcwd() + "\\" + "command.txt"
    
    try:
        fm = open(getpath,'r')
        cmd = fm.read()
        fm.close()
    except FileNotFoundError:
        return None

    fm = open(savepath,'w')
    fm.write(cmd)
    fm.close()
    return True

def check_tihuan_SCRY_status():
    '''通过检查SCR_Y是否存在
    \n来检查是否已经完成替换拦截程序
    \n返回True/False'''
    check_path = "C:\Program Files (x86)\Os-Easy\os-easy multicast teaching system\ScreenRender_Y.exe"
    try:
        fm = open(check_path,'r')
        fm.close()
        return True
    except FileNotFoundError:
        return False
    


def get_pid(name):
    '''
    根据进程名获取进程pid\n
    未寻找到返回None
    '''
    pids = psutil.process_iter()
    ZiHao_logger.debug("[" + name + "]'s pid is:")
    for pid in pids:
        if(pid.name() == name):
            ZiHao_logger.debug(pid.pid)
            return pid.pid
    return None

def get_time_str():
    '''返回一个时间字符串'''
    time_str = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    return time_str


def get_scshot():
    '''保存一张屏幕截图'''

    savepath = os.getcwd()

    PMsize = pyautogui.size()
    ZiHao_logger.debug("DEBUG 屏幕尺寸 > ",PMsize)
    win_h = PMsize.height
    win_w = PMsize.width

    img = pyautogui.screenshot()

    mix_name = savepath + "\\" + get_time_str() + ".jpg"
    img.save(mix_name)
    ZiHao_logger.debug("SavePath > ",mix_name)


def MMPC_shutdown_start_chufa():
    '''关闭/开启MMPC根服务的触发函数'''
    st = check_MMPC_status()
    if st==True:
    # self.mmpc_Stext.value = "正在运行"
    # self.mmpc-Stext.bgcolor = "green"
        runcmd("sc stop MMPC")
    elif st== False:
    # self.mmpc_Stext.value = "未运行"
    # self.mmpc-Stext.bgcolor = "red"
        runcmd("sc start MMPC")



def check_MMPC_status():
    '''检查MMPC根服务状态\n
    返回True/False'''
    # f=os.popen("sc query MMPC")
    name = "MMPC"
# def get_service(name):
    service = None
    try:
        service = psutil.win_service_get(name)
        service = service.as_dict()
    except Exception as ex:
        # print(str(ex))
        return False
    # return service

    if service and service['status'] == 'running':
        return True
    else:
        return False




def run_upto_admin():
    '''用于在非管理员运行时尝试提权'''
    if ctypes.windll.shell32.IsUserAnAdmin() == 0:
        ctypes.windll.shell32.ShellExecuteW(None,"runas",sys.executable,"".join(sys.argv),None,1)
        sys.exit()

def del_historyrem(e):
    '''删除保存的历史路径文件'''
    neddel = [path_zidingyi_bg,path_zidingyi_fort,path_zidingyi_yiyan]
    for name in neddel:
        try:
            os.remove(name)
        except FileNotFoundError:
            pass

# def suspend_process(process_name):
def guaqi_process(process_name):
    '''挂起进程'''
    try:
        for process in psutil.process_iter(['pid', 'name']):
            if process.info['name'] == process_name:
                pid = process.info['pid']
                psutil.Process(pid).suspend()
                ZiHao_logger.debug(f"Process {process_name} (PID {pid}) suspended.")
                return True

        ZiHao_logger.error(f"Process {process_name} not found.")
        ZiHao_logger.error("未找到尝试挂起的学生端进程?")
        return "尝试挂起的进程未找到"
    except psutil.AccessDenied as e:
        ZiHao_logger.error(f"Permission error: {e}")
        ZiHao_logger.error("尝试挂起进程失败? - 请检查是否以管理员权限运行qwq")
        return "尝试挂起进程失败"

# def resume_process(process_name):
def huifu_process(process_name):
    '''恢复挂起进程'''
    try:
        for process in psutil.process_iter(['pid', 'name']):
            if process.info['name'] == process_name:
                pid = process.info['pid']
                psutil.Process(pid).resume()
                ZiHao_logger.debug(f"Process {process_name} (PID {pid}) resumed.")
                return True

        ZiHao_logger.error(f"Process {process_name} not found.")
        ZiHao_logger.error("未找到尝试恢复挂起的学生端进程")
        return "尝试恢复挂起的进程未找到"
    except psutil.AccessDenied as e:
        ZiHao_logger.error(f"Permission error: {e}")
        ZiHao_logger.error("尝试恢复挂起失败? - 请检查是否以管理员权限运行qwq")
        return "尝试恢复挂起进程失败"



def onetime_protectcheck():
    '''检测是否开启了击杀脚本\n
    若未开启则帮助启动一次\n
    已经开启则忽略'''
    try:
        window = gw.getWindowsWithTitle('OsEasyToolBoxKiller')[0]
    except:
        summon_killer()
        runbat("k.bat")

def opengithubres(e):
    '''在浏览器打开github仓库页面'''
    webbrowser.open("https://github.com/ZiHaoSaMa66/OsEasy-ToolBox")
    
def opengithubres_Lite():
    '''在浏览器打开github仓库页面'''
    webbrowser.open("https://github.com/ZiHaoSaMa66/OsEasy-ToolBox-Lite")




def startprotect():
    global RunProtectCMD
    '''启动守护进程'''
    # print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    # print("--------------------------------")
    # print("Protect Progress Start!")
    # print("尝试运行守护进程函数 with status ",RunProtectCMD)
    # print("--------------------------------")
    ptct = 0
    # while RunProtectCMD==True:
    while True:
        # print("守护进程启动...")   
        try:
            # print("[Protect Check] 检查进程状态?\n")
            window = gw.getWindowsWithTitle('OsEasyToolBoxKiller')[0]
            time.sleep(0.5)
        except:
            # print("[info] 未检测到运行,将尝试重启进程\n")
            
            runbat("k.bat")
            ptct += 1
            # print(f"[√] 已成功为您守护{ptct}次进程")
            time.sleep(1)
    # print("")




def delcmdfiles():
    '''删除生成的脚本文件'''
    global cmdpath
    fln = ["k.bat","d.bat","temp.bat","kv2.bat",'net.bat']
    for i in fln:
        try:
            swpath = cmdpath + "\\" + i
            os.remove(swpath)
        except Exception:
            pass

def check_firsttime_start():
    '''检查是否为第一次启动'''
    #用于第一次判断是否使用autodesk fix
    try:
        fm = open("C:\\FST.data","r")
        fm.close()
        return False
    except FileNotFoundError:
        fm = open("C:\\FST.data","w")
        fm.close()
        return True

# os.makedirs(cmdpath,mode=0o777,exist_ok=True)
def summon_unlocknet():
    '''生成解锁网络锁定脚本'''
    global cmdpath
    mp = cmdpath + "\\net.bat"
    fm = open(mp,"w")
    cmdtext = "@ECHO OFF\ntitle OsEasyToolBoxUnlockNetHeler\n:a\ntaskkill /f /t /im Student.exe\ntaskkill /f /t /im DeviceControl_x64.exe\ngoto a"
    fm.write(cmdtext)
    fm.close()

def summon_killerV2():
    '''生成V2击杀脚本'''
    global cmdpath
    mp = cmdpath + "\\kv2.bat"
    fm = open(mp,"w")
    cmdtext = "@ECHO OFF\ntitle OsEasyToolBoxKillerV2\n:awa\nfor %%p in (Ctsc_Multi.exe,DeviceControl_x64.exe,HRMon.exe,MultiClient.exe,OActiveII-Client.exe,OEClient.exe,OELogSystem.exe,OEUpdate.exe,OEProtect.exe,ProcessProtect.exe,RunClient.exe,RunClient.exe,ServerOSS.exe,Student.exe,wfilesvr.exe,tvnserver.exe,updatefilesvr.exe,ScreenRender.exe) do taskkill /f /IM %%p\ngoto awa\n"
    fm.write(cmdtext)
    fm.close()

def summon_killer():
    '''生成击杀脚本'''
    global cmdpath
    mp = cmdpath + "\\k.bat"
    fm = open(mp,"w")
    cmdtext = "@ECHO OFF\ntitle OsEasyToolBoxKiller\ntaskkill /f /t /im MultiClient.exe\ntaskkill /f /t /im MultiClient.exe\n:a\ntaskkill /f /t /im Student.exe\ngoto a"
    fm.write(cmdtext)
    fm.close()

def backupOeKeyDll():
    '''备份OE的关键文件'''
    global bkppath,oseasypath
    ZiHao_logger.debug("尝试备份关键文件")
    namelist = ["oenetlimitx64.cat","OeNetLimitSetup.exe","OeNetLimit.sys","OeNetLimit.inf","MultiClient.exe","MultiClient.exe","LoadDriver.exe"]
    for filename in namelist:
        oepath = oseasypath + filename
        needbkpath =  bkppath + "\\" + filename

        # print("oepath>>",oepath)
        # print("nedbkpath>>",needbkpath)
        # runcmd()
        # runcmd(f'copy "{oepath}" "{needbkpath}"\npause')
        runcmd(f'copy "{oepath}" "{needbkpath}"')


def restoneMutClient(e):
    '''恢复用于控屏的MultiClient'''
    global bkppath,oseasypath
    filename = "MultiClient.exe"
    oepath = oseasypath + filename
    needbkpath =  bkppath + "\\" + filename
    runcmd(f'copy "{needbkpath}" "{oepath}"')

def restoneKeyDll():
    '''恢复OE关键文件'''
    global bkppath,oseasypath
    ZiHao_logger.debug("尝试还原关键文件")
    namelist = ["oenetlimitx64.cat","OeNetLimitSetup.exe","OeNetLimit.sys","OeNetLimit.inf","MultiClient.exe","LoadDriver.exe"]
    for filename in namelist:
        oepath = oseasypath + filename
        needbkpath =  bkppath + "\\" + filename

        runcmd(f'copy "{needbkpath}" "{oepath}"')
    pass

def runbat(batname:str):
    '''运行指定名称的bat脚本'''
    global cmdpath
    batp = cmdpath + "\\" + batname
    runcmd(f'start {batp}')

def summon_deldll(delMtc:bool,shutdown:bool):
    '''生成删除dll脚本'''
    global cmdpath
    backupOeKeyDll()
    
    mp = cmdpath + "\\d.bat"
    fm = open(mp,"w")
    cmdtext = "@ECHO OFF\ntitle OsEasyToolBox-Helper\ncd /D C:\Program Files (x86)\Os-Easy\os-easy multicast teaching system\\\ntimeout 1\ndel /F /S OeNetLimitSetup.exe\ndel /F /S OeNetLimit.sys\ndel /F /S OeNetLimit.inf\ndel /F /S LockKeyboard.dll\ndel /F /S LoadDriver.exe\ndel /F /S LoadDriver.exe\ndel /F /S oenetlimitx64.cat"
    if delMtc ==True:
        cmdtext += "\ndel /F /S MultiClient.exe"
    if shutdown ==False:
        pass
    elif shutdown ==True:
        cmdtext += "\ntimeout 5\nshutdown /l"
    #cmdtext += "\ntimeout 10\nshutdown /l"
    cmdtext += "\nexit"
    fm.write(cmdtext)
    fm.close()

def regkillercmd():
    '''生成击杀脚本并绑定粘滞键'''
    summon_killer()
    # mp = cmdpath + "\\r.bat"
    # fm = open(mp,"w")
    # cmdtext = 'REG ADD "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Image File Execution Options\\sethc.exe" /v Debugger /t REG_SZ /d "C:\\Program Files\\dotnet\\k.bat"'
    # fm.write(cmdtext)
    # fm.close()
    # os.system("start C:\\Program Files\\dotnet\\r.bat")
    runcmd(f'REG ADD "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Image File Execution Options\\sethc.exe" /v Debugger /t REG_SZ /d "{cmdpath}\\k.bat"')

def regkillerV2cmd():
    '''生成击杀脚本V2并绑定粘滞键'''
    summon_killerV2()
    runcmd(f'REG ADD "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Image File Execution Options\\sethc.exe" /v Debugger /t REG_SZ /d "{cmdpath}\\kv2.bat"')

    
def boxkiller():
    global RunBoxKiller
    while RunBoxKiller==True:
    # os.system(command="taskkill /f /t /im Student.exe")
        opt = os.system("taskkill /f /t /im Student.exe")
        #print("test run")
        time.sleep(0.2)
    #print(f"[DEBUG] Killer Runned {opt}")

def runcmd(givecmd:str,*quiterun:bool):
    '''运行指定的命令'''
    if not quiterun:
        os.popen(cmd=givecmd)
    elif quiterun==False:
        os.system(command=givecmd)
    elif quiterun==True:
        os.popen(cmd=givecmd)
    else:
        os.system(command=givecmd)

def usecmd_runcmd(cmd:str):
    '''生成一个临时cmd文件运行指定命令'''
    global cmdpath
    mp = cmdpath + "\\temp.bat"
    fm = open(mp,"w")
    cmdtext = "@ECHO OFF\n"
    cmdtext += cmd
    cmdtext += "\nexit"
    fm.write(cmdtext)
    fm.close()
    runcmd(f"start {mp}")

#策略

# def selfunc_c1(e):
#     #完全不听课 - 全程全脱控制 不接收文件
#     regkillercmd()
#     startprotect()
    
# def selfunc_c2(e):
#     #稍微听点 不会被控屏 可接收文件
#     regkillercmd()
#     onetime_protectcheck()
#     summon_deldll(delMtc=True,shutdown=True)
#     showwarning("温馨提醒","该解锁略微需要手速\n在工具箱帮助你注销以后\n只要看见可以重新登录后即可点出粘滞键的脚本完成解锁")
#     time.sleep(1.5)
#     runbat("d.bat")

# def selfunc_c3(e):
#     #几乎全听 可被老师控屏 但可主动注销跳出控制
#     regkillercmd()
#     onetime_protectcheck()
#     summon_deldll(delMtc=False,shutdown=True)
#     showwarning("温馨提醒","该解锁略微需要手速\n在工具箱帮助你注销以后\n只要看见可以重新登录后即可点出粘滞键的脚本完成解锁")
#     time.sleep(1.5)
#     runbat("d.bat")
#     pass

#快捷功能类

def selfunc_g0(e):
    #清理生成的脚本文件
    delcmdfiles()
def selfunc_g1(e):
    #注册粘滞键替换击杀脚本
    regkillercmd()
    
def selfunc_g1plus(e):
    #注册V2版本的替换击杀脚本
        regkillerV2cmd()

def selfunc_g2(e):
    global RunBoxKiller
    # result = askquestion("温馨提示","此功能为半成品功能\n是否继续?")
    # # print(result)
    # if result =="yes":
    if RunBoxKiller ==False:
        # save_loginwithoutpwd()
        RunBoxKiller = True
        boxkiller()
    elif RunBoxKiller ==True:
        RunBoxKiller = False
        
def selfunc_g3(need_shutdown:bool):
    # showwarning("温馨提醒","此功能略微需要手速\n在工具箱帮助你注销以后\n只要看见可以重新登录后即可点出粘滞键的脚本完成解锁")
    # showwarning("温馨提醒","在注销后若无效果请手动重启机器\n(如果你的机房电脑有重启立刻还原请无视)\n(可以再次打开工具箱再次尝试注销解锁)\n并在进入系统桌面前手动点开粘滞键的击杀脚本\n若不想要注销可手动X掉命令窗口!!")
    summon_killer()
    onetime_protectcheck()
    summon_deldll(delMtc=True,shutdown=need_shutdown)
    time.sleep(2)
    runbat("d.bat")
    
def selfunc_g4(e):
    usecmd_runcmd('"C:\Program Files (x86)\Os-Easy\os-easy multicast teaching system\Student.exe"')

def selfunc_g5(e):
    restoneKeyDll()

def selfunc_g6(e):
    global RunProtectCMD
    if RunProtectCMD ==False:
        RunProtectCMD = True
        summon_killer()
        startprotect()
    elif RunProtectCMD ==True:
        RunProtectCMD = False
        usecmd_runcmd('taskkill /f /t /fi "imagename eq cmd.exe" /fi "windowtitle eq 管理员:  OsEasyToolBoxKiller"')

def run_waibu_protect_loj():
    '''外部cmd守护进程的功能触发逻辑函数'''
    global RunProtectCMD,protect_pid
    # print("逻辑函数处的状态码",RunProtectCMD)
    protect = Process(target=startprotect)
    if RunProtectCMD ==False:
        RunProtectCMD = True
        summon_killer()
        protect.start()
        protect_pid = protect.pid
        # print("ppid=",protect_pid)
        
    elif RunProtectCMD ==True:
        RunProtectCMD = False
        # ppid = protect.pid
        # print("ppid=",protect_pid)
        os.kill(protect_pid,signal.SIGINT)
        # 妈了个蛋的 麻烦过你大坝
        # protect.kill()
        # protect.close()
        # protect.terminate()
        # protect.kill()
        usecmd_runcmd('taskkill /f /t /fi "imagename eq cmd.exe" /fi "windowtitle eq 管理员:  OsEasyToolBoxKiller"')

def begin_a_child_progress(func_name):
    '''给定函数名启动开启子线程\n
    仅适用于非死循环函数'''
    # queue = Queue()  
    # 创建队列用于进程间通信
    child_progress = Process(target=func_name)
    child_progress.start()
    child_progress_pid = child_progress.pid
    ZiHao_logger.debug(f"启动了函数={func_name},PID={child_progress_pid}的子线程")
    
    child_progress.join()
    # result = child_progress.exitcode
    # 妈的什么歪门邪道
    # share_name.Return_value = result
    
    # 从队列中获取子进程的返回值
    # result = queue.get()
    # print("子进程返回值:", result)
    
    # ZiHao_logger.debug(f"EXC child_func put > {share_name.Return_value}")

# def child_progress_helper(func_name, queue):
#     '''给定函数名启动开启子线程的辅助函数\n
#     请勿直接调用'''
#     result = func_name()  # 调用函数获取返回值
#     queue.put(result)  # 将返回值放入队列
#     pass

def selfunc_g7():
    summon_unlocknet()
    runbat("net.bat")
    time.sleep(2)
    runcmd("sc stop OeNetlimit")
    time.sleep(1)
    usecmd_runcmd('taskkill /f /t /fi "imagename eq cmd.exe" /fi "windowtitle eq 管理员:  OsEasyToolBoxUnlockNetHeler"')
    time.sleep(1)

def selfunc_g8(e):

    onetime_protectcheck()
    time.sleep(2)
    runcmd(f'"{oseasypath}AssistHelper.exe"')