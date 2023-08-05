class PyBox(object):
  def __init__(self,path='main.db'):
    import pickle
    self.isopen = True
    self.path = path
    try:
      self.data = pickle.load(open(path,'rb'))
    except:
      self.data = {'db-config-test':True}
    import pickle
    try:
      open(path,'rb').read()
      try:
        open(path,'r')
      except:
        open(self.path,'w+')
        with open(self.path,'wb') as f:
          pickle.dump(self.data,f)
          f.flush()
    except:
      pass
    from threading import Timer
    self.t = Timer(0, self.refresher)
    self.t.start()
  def refresher(self):
    while self.isopen == True:
      self.update()
  def update(self):
    import pickle
    import time
    try:
      with open(self.path,'rb') as f:
        self.data = pickle.load(f)
    except:
      pass
    time.sleep(0.3)
    with open(self.path,'wb') as f:
      pickle.dump(self.data,f)
      f.flush()
  def close(self):
    self.isopen = False
    self.update()
    return 'Database closed at ' + self.path