import qt

# helper functions for developing - see bottom for key bindings

def tracker():
  print("tracker setup...")
  import imp, sys
  p = '/home/pieper/hacks/itrack'
  if not sys.path.__contains__(p):
    sys.path.insert(0,p)


  mod = "itrack"
  sourceFile = p + "/itrack.py"
  fp = open(sourceFile, "r")
  globals()[mod] = imp.load_module(mod, fp, sourceFile, ('.py', 'r', imp.PY_SOURCE))
  fp.close()

  globals()['i'] = i = globals()[mod].itrack()
  i.capture()


def endoscopy():
  print("endoscopy setup...")
  import imp, sys
  endoPath = '%s/../../Slicer4/QTScriptedModules/Scripts' % os.environ['Slicer_HOME']
  if not sys.path.__contains__(endoPath):
    sys.path.insert(0,endoPath)


  mod = "Endoscopy"
  sourceFile = endoPath + "/Endoscopy.py"
  fp = open(sourceFile, "r")
  globals()[mod] = imp.load_module(mod, fp, sourceFile, ('.py', 'r', imp.PY_SOURCE))
  fp.close()

  globals()['e'] = e = globals()[mod].EndoscopyWidget()


def editor():
  print("editor setup...")
  import imp, sys
  tcl("set ::guipath $::env(Slicer3_HOME)/../../Slicer4/Base/GUI/Tcl")
  tcl("if { [lsearch $::auto_path $::guipath] == -1 } { set ::auto_path [list $::env(Slicer3_HOME)/../../Slicer4/Base/GUI/Tcl $::auto_path] } ")
  tcl("package forget SlicerBaseGUITcl")
  tcl("package require SlicerBaseGUITcl")
  tcl("EffectSWidget::RemoveAll")
  tcl("EffectSWidget::Add DrawEffect")

  if not getNodes().has_key('2006-spgr'):
    slicer.mrmlScene.SetURL('/home/pieper/data/edit/edit-small.mrml')
    slicer.mrmlScene.Connect()

  if 0 and not getNodes().has_key('CTA-cardio'):
    slicer.mrmlScene.SetURL('/home/pieper/data/edit/edit.mrml')
    slicer.mrmlScene.Connect()

  editorLibPath = '%s/../../Slicer4/QTScriptedModules/EditorLib' % os.environ['Slicer_HOME']
  if not sys.path.__contains__(editorLibPath):
    sys.path.insert(0, editorLibPath)
  editorPath = '%s/../../Slicer4/QTScriptedModules/Scripts' % os.environ['Slicer_HOME']
  if not sys.path.__contains__(editorPath):
    sys.path.insert(0,editorPath)


  modules = ("EditUtil", "EditColor", "EditOptions", "EditBox", "ColorBox", "HelperBox")
  for mod in modules:
    sourceFile = editorLibPath + "/" + mod + ".py"
    fp = open(sourceFile, "r")
    globals()[mod] = imp.load_module(mod, fp, sourceFile, ('.py', 'r', imp.PY_SOURCE))
    fp.close()
    exec("globals()['EditorLib'].%s = globals()['%s'].%s" % (mod,mod,mod))

  mod = "Editor"
  sourceFile = editorPath + "/Editor.py"
  fp = open(sourceFile, "r")
  globals()[mod] = imp.load_module(mod, fp, sourceFile, ('.py', 'r', imp.PY_SOURCE))
  fp.close()

  globals()['e'] = e = globals()[mod].EditorWidget()


def fileScan():
  print("fileScan setup...")
  import imp, sys
  p = '%s/../../Slicer4/QTScriptedModules/Scripts' % os.environ['Slicer_HOME']
  if not sys.path.__contains__(p):
    sys.path.insert(0,p)


  mod = "FileScan"
  sourceFile = p + "/FileScan.py"
  fp = open(sourceFile, "r")
  globals()[mod] = imp.load_module(mod, fp, sourceFile, ('.py', 'r', imp.PY_SOURCE))
  fp.close()

  globals()['e'] = e = globals()[mod].FileScanWidget()



def loadRCFile():
  """ reload this file - can't use the version in _internalInstance, since
  it does not exist yet when the key macros are defined"""
  import os.path
  rcfile = os.path.expanduser('~/.slicerrc.py')
  if os.path.isfile(rcfile):
    execfile(rcfile)



# set up hot keys for various development scenarios

globals()['loadRCFile'] = loadRCFile
globals()['tracker'] = tracker
globals()['endoscopy'] = endoscopy
globals()['editor'] = editor
globals()['fileScan'] = fileScan

def setupMacros():
  macros = (
      ("Ctrl+0", loadRCFile),
      ("Ctrl+1", tracker),
      ("Ctrl+2", endoscopy),
      ("Ctrl+3", editor),
      ("Ctrl+4", fileScan),
      )

  if mainWindow():
    print('got main window')
    for keys,f in macros:
      k = qt.QKeySequence(keys)
      s = qt.QShortcut(k,mainWindow())
      s.connect('activated()', f)
      s.connect('activatedAmbiguously()', f)
  else:
    # main window does not exist yet, try again later
    # TODO: shouldn't there be a signal when the main window is ready to access?
    timer = qt.QTimer()
    timer.setSingleShot(True)
    timer.connect("timeout()", setupMacros)
    timer.start()
    globals()['_macroTimer'] = timer
    print('timer active')

globals()['setupMacros'] = setupMacros
setupMacros()


