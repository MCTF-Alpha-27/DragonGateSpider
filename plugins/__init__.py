"""
插件导入文件，负责导入所有插件并创建插件菜单
"""
from libs import *
import importlib
import glob
import os

dragonGateSpider.log("正在载入插件", dragonGateSpider.INFO)

plugins = {}
for i in glob.glob("plugins/*.py"):
    plugin_file_name = i.replace("\\", ".").replace(".py", "")
    if "__init__" not in plugin_file_name:
        plugin = importlib.import_module(plugin_file_name)
        dragonGateSpider.log(f"载入插件: {plugin.__name__}", dragonGateSpider.INFO)
        plugins[plugin_file_name.replace("plugins.", "")] = plugin

disabled_plugins = []
for i in glob.glob("plugins/*.disabled"):
    plugin_file_name = i.replace("plugins\\", "").replace(".disabled", "")
    dragonGateSpider.log(f"禁用的插件: {plugin_file_name}", dragonGateSpider.INFO)
    disabled_plugins.append(plugin_file_name)

def enable():
    def _enable(plugin):
        os.rename("plugins/%s.disabled"%plugin, "plugins/%s.py"%plugin)
        exit_app("重启", "已启用此插件，本次操作需要手动重启程序")
    return _enable

def info():
    def _info(i):
        doc = plugins[i].__doc__
        if doc is None:
            doc = "\n此插件没有说明文档\n"
        
        def disable(plugin):
            os.rename("plugins/%s.py"%plugin, "plugins/%s.disabled"%plugin)
            exit_app("重启", "已禁用此插件，本次操作需要手动重启程序")

        return {
            "name": plugins[i].__name__,
            "author": getattr(plugins[i], "__author__", "未知"),
            "version": getattr(plugins[i], "__version__", "1.0.0"),
            "document": doc,
            "show": lambda: QMessageBox.information(dragonGateSpider, "插件信息", f"插件注册名：{i}\n插件名称：{plugins[i].__name__}\n插件作者：{getattr(plugins[i], '__author__', '未知')}\n插件版本：v{getattr(plugins[i], '__version__', '1.0.0')}\n{doc}"),
            "disable": lambda: disable(i),
        }
    functions = {}
    for i in plugins:
        functions[i] = _info(i)
    return functions

for i in info():
    plugin_menu = QMenu(info()[i]["name"], dragonGateSpider.ui.plugins_menu)
    plugin_menu.setObjectName(i)
    dragonGateSpider.ui.plugins_menu.addMenu(plugin_menu)

    plugin_menu_info_action = QAction("插件信息", plugin_menu)
    plugin_menu_info_action.setObjectName(i + "_info_action")
    plugin_menu_info_action.triggered.connect(info()[i]["show"])
    plugin_menu.addAction(plugin_menu_info_action)

    plugin_menu_disable_action = QAction("禁用此插件", plugin_menu)
    plugin_menu_disable_action.setObjectName(i + "_disable_action")
    plugin_menu_disable_action.triggered.connect(info()[i]["disable"])
    plugin_menu.addAction(plugin_menu_disable_action)

if len(disabled_plugins) == 0:
    dragonGateSpider.ui.disabled_plugins_menu.deleteLater()
else:
    for i in disabled_plugins:
        disabled_plugins_menu = QMenu(i, dragonGateSpider.ui.disabled_plugins_menu)
        disabled_plugins_menu.setObjectName(i)
        dragonGateSpider.ui.disabled_plugins_menu.addMenu(disabled_plugins_menu)

        disabled_plugins_menu_action = QAction("启用此插件", disabled_plugins_menu)
        disabled_plugins_menu_action.setObjectName(i + "_enable_action")
        disabled_plugins_menu_action.triggered.connect(lambda: enable()(i))

        disabled_plugins_menu.addAction(disabled_plugins_menu_action)

dragonGateSpider.log(f"{str(len(plugins))} 个插件已载入，{str(len(disabled_plugins))} 个插件已被禁用", dragonGateSpider.INFO)
