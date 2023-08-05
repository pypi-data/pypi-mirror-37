#! python3
# -*- encoding: utf-8 -*-
'''
Current module: winuidriver.driver

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:     luokefeng@163.com
    RCS:      winuidriver.driver,  v1.0 2018年9月30日
    FROM:   2018年9月30日
********************************************************************
======================================================================

Provide a function for the automation test

'''


import re
from rtsf.p_executer import Runner
from rtsf.p_common import CommonUtils,ModuleUtils
from rtsf.p_exception import FunctionNotFound,VariableNotFound

class Driver(Runner):
        
    def run_test(self, testcase_dict, driver_map):
        fn, _ = driver_map
        tracer = self.tracers[fn]
        parser = self.parser        
        
        functions = {}
        _Actions = ModuleUtils.get_imported_module("winuidriver.actions")
        
        win_actions_functions = ModuleUtils.get_callable_class_method_names(_Actions.WinActions)
        win_context_functions = ModuleUtils.get_callable_class_method_names(_Actions.WinContext)
        win_element_functions = ModuleUtils.get_callable_class_method_names(_Actions.WinElement)
        win_verify_functions = ModuleUtils.get_callable_class_method_names(_Actions.WinVerify)
        win_wait_functions = ModuleUtils.get_callable_class_method_names(_Actions.WinWait)
        
        functions.update(win_actions_functions)
        functions.update(win_context_functions)
        functions.update(win_element_functions)
        functions.update(win_verify_functions)
        functions.update(win_wait_functions)
        parser.bind_functions(functions)
        parser.update_binded_variables(_Actions.WinContext.glob)
         
        case_name = testcase_dict["name"]                 
        tracer.start(self.proj_info["module"], case_name, testcase_dict.get("responsible","Administrator"), testcase_dict.get("tester","Administrator"))        
        tracer.section(case_name)
        
        try:
            tracer.normal("**** bind glob variables")                
            glob_vars = parser.eval_content_with_bind_actions(testcase_dict.get("glob_var",{}))
            tracer.step("set global variables: {}".format(glob_vars))                
            _Actions.WinContext.glob.update(glob_vars)            
             
            tracer.normal("**** bind glob regular expression")
            globregx = {k: re.compile(v) for k,v in testcase_dict.get("glob_regx",{}).items()}
            tracer.step("set global regular: {}".format(globregx))            
            _Actions.WinContext.glob.update(globregx)
                             
            tracer.normal("**** precommand")
            precommand = testcase_dict.get("pre_command",[])    
            parser.eval_content_with_bind_actions(precommand)
            for i in precommand:
                tracer.step("{}".format(i))
             
            tracer.normal("**** steps")
            steps = testcase_dict["steps"]
            for step in steps:
                #print("---")            
                if not "windriver" in step:
                    continue
                
                if not step["windriver"].get("action"):
                    raise KeyError("windriver.action")            
                
                #print(step)                
                _properties = ("ControlType","ClassName","AutomationId","Name","SubName","RegexName","Depth")
                properties = {prop:parser.eval_content_with_bind_actions(step["windriver"].get(prop)) for prop in _properties if step["windriver"].get(prop)}                
                if properties:
                    properties.update({"index" : parser.eval_content_with_bind_actions(step["windriver"].get("index", 0))})
                    properties.update({"timeout" : parser.eval_content_with_bind_actions(step["windriver"].get("timeout", 10))})
                    tracer.normal("preparing: properties -> {}".format(properties))
                
                    prepare =parser.get_bind_function("SetSearchProperty")
                    prepare(**properties)
                                
                result = parser.eval_content_with_bind_actions(step["windriver"]["action"])
                
                if result == False:
                    tracer.fail(step["windriver"]["action"])
                else:
                    tracer.ok(step["windriver"]["action"])
                        
            tracer.normal("**** postcommand")
            postcommand = testcase_dict.get("post_command", [])        
            parser.eval_content_with_bind_actions(postcommand)
            for i in postcommand:
                tracer.step("{}".format(i))
            
            tracer.normal("**** verify")
            verify = testcase_dict.get("verify",[])
            result = parser.eval_content_with_bind_actions(verify)
            for v, r in zip(verify,result):
                if r == False:
                    tracer.fail(u"{} --> {}".format(v,r))
                else:
                    tracer.ok(u"{} --> {}".format(v,r))
                        
        except KeyError as e:
            tracer.error("Can't find key[%s] in your testcase." %e)
            print(CommonUtils.get_exception_error())
        except FunctionNotFound as e:
            tracer.error(e)
        except VariableNotFound as e:
            tracer.error(e)
        except Exception as e:
            tracer.error("%s\t%s" %(e,CommonUtils.get_exception_error()))
        finally:
            #tracer.normal("globals:\n\t{}".format(parser._variables)) 
            tracer.stop()
        
               
        