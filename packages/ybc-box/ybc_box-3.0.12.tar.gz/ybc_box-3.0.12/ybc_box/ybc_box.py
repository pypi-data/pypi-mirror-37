# coding=utf-8
import easygui as eg

def buttonbox(msg='', choices=[], title=''):
    return eg.buttonbox(msg, title, choices)

def choicebox(msg='', choices=[], title=''):
    return eg.choicebox(msg, title, choices)

def codebox(msg='', text='', title=''):
    return eg.codebox(msg, title, text)

def enterbox(msg='', image=None, title=''):
    return eg.enterbox(msg, title, image=image)

def fileopenbox(msg='', title=''):
    return eg.fileopenbox(msg, title)

def indexbox(msg='', choices=[], title=''):
    return eg.indexbox(msg, title, choices)

def intbox(msg=''):
    return eg.integerbox(msg)

def integerbox(msg=''):
    return eg.integerbox(msg)

def msgbox(msg='', image=None):
    return eg.msgbox(msg, image=image)

def multchoicebox(msg='', choices=[], title=''):
    return eg.multchoicebox(msg, title, choices)

def multpasswordbox(msg='', fields=[], title=''):
    return eg.multpasswordbox(msg, title, fields=fields)

def passwordbox(msg='', title=''):
    return eg.passwordbox(msg, title)

def textbox(msg='', text='', title='', codebox=True):
    return eg.textbox(msg, title, text, codebox)

def ynbox(msg='', title=''):
    return eg.ynbox(msg, title)
