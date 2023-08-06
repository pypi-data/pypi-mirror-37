#!/usr/bin/python3

"""
  poll_gpfs_policy.py - script to query the database underlying an IBM General Parallel File System,
  in order to identify files which have changed, since the last invocation.

poll_script_command - the name of the GPFS policy script (which outputs one file name per line.)

policy_start_time - looking for files modified since this time.
  (only on first pass, subsequent passes use time saved in the start_time_file)


 
"""

import os,sys,stat,time
import calendar,socket

class POLL_SCRIPT(object): 

   def __init__(self,parent):

      if not hasattr(parent,'poll_script_command'):
         parent.poll_script_command= [ '/usr/bin/find', '/tmp', '-type', 'f', '-print'  ]
      else:
         if ' ' in parent.poll_script_command[0]:
             parent.poll_script_command = parent.poll_script_command[0]
             #parent.poll_script_command = parent.poll_script_command[0].split(' ')

      self.new_policy_start_time = ""
 
      #the cache file for saving the start time
      self.start_time_file = self.user_cache_dir + os.sep + '_last_start_time'

      #get the start time in the poll config file or the cache if it has one.
      if not hasattr(parent,'policy_start_time'):
         if os.path.isfile(self.start_time_file):
            try:         
              f = open(self.start_time_file,'r')
              self.policy_start_time = f.readline().rstrip() 
              f.close()
            except:pass
         else:
            self.policy_start_time = time.strftime('%Y-%m-%d@%H:%M:%S',time.gmtime(time.time() - 60))
      else:
         self.policy_start_time = parent.policy_start_time[0] 
       
      self.host = parent.destination.split('@')[1].replace('/','')
      self.listhosts = list( map( lambda x: x[4][0], socket.getaddrinfo(self.host,22,socket.AF_INET,socket.SOCK_STREAM)) )
      try:
         self.listhosts.remove(parent.vip)
      except:pass
      parent.logger.info("list of hosts %s" % self.listhosts)

   def has_vip(self,parent):
      self.interfaces = netifaces.interfaces()
      for i in self.interfaces:
          for a in (netifaces.ifaddresses(i)):
              if parent.vip in netifaces.ifaddresses(i)[a][0].get('addr'):
                 parent.logger.info("host has vip %s" % parent.vip)
                 return True
      return False        
   
   def perform(self,parent):
      logger = parent.logger
      msg    = parent.msg
     
      if not self.has_vip(parent): 
         logger.info("vip %s not exists: sr_poll is sleeping." % parent.vip)
         self.policy_start_time = time.strftime('%Y-%m-%d@%H:%M:%S',time.gmtime())
         
         return True 
       
      import subprocess
      try:
           from sr_util import timestr2flt
      except:
           from sarra.sr_util import timestr2flt
      
      self.new_policy_start_time = time.strftime('%Y-%m-%d@%H:%M:%S',time.gmtime(time.time() - 75))
      self.policy_start_time = self.policy_start_time[:-2]+'00'
      cmd = parent.poll_script_command + ' ' + self.policy_start_time
      #save the start time in the cache file
      f = open(self.start_time_file,'w')
      f.write(self.policy_start_time)
      f.close()      
 
      logger.info("poll_script invoking: %s " % cmd )
      stime = time.time()
      (status,output) = subprocess.getstatusoutput(cmd) 
      logger.info("time for running poll_script: %s sec" % int(time.time() - stime) )
      
      if status == 0: 
          output_file = self.user_cache_dir + os.sep + parent.config_name + '_' + self.policy_start_time + '.output'
          logger.info("save output: %s " % output_file )
          f = open(output_file,'w')
          f.write(output)
          f.close()

          if "No files were changed" in output: 
              for line in output.split('\n')[2:-1]:
                  logger.info("%s " % line )
          else: 
              stime = time.time()
              nmsg = 0
              self.policy_start_time = self.new_policy_start_time
              for line in output.split('\n')[1:-2]:
                  fname = line
                  logger.info("poll_script fname is: %s " % fname )
                  nmsg = nmsg + 1
                  destination = parent.destination.replace(self.host,random.choice(self.listhosts))
 
                  #msg.urlstr = parent.destination  + '/' + fname
                  msg.urlstr = destination  + '/' + fname
                  
                  logger.debug("poll_script urlstr is: %s " % msg.urlstr )
                  
                  msg.url = urllib.parse.urlparse(msg.urlstr)
                  
                  try:
                     isdir = False
                     islink = False
                     link = ""

                     if os.path.islink(fname):
                         islink = True
                         msg.sumstr  = 'L,0'
                         link = os.readlink(fname)
                         if '/fs/site1' in link: link = link.replace('/fs/site1','/fs/site2')
                         elif '/fs/site2' in link: link = link.replace('/fs/site2','/fs/site1')
 
                     elif os.path.isfile(fname):
                         msg.sumstr  = '0,0'
                         #logger.info("test1 poll_script fname is: %s " % fname )
                     else:
                         isdir = True
                         logger.info("fname is a directory: %s " % fname )
                         
                     if not isdir:
                         fst = os.lstat(fname)
                         #logger.info("test2 poll_script fname is: %s " % fname )
                         msg.partstr = '1,%s,1,0,0' % fst.st_size
                         mtimestr = timeflt2str(fst.st_mtime)
                         atimestr = timeflt2str(fst.st_atime)
                         #logger.info("test3 poll_script fname is: %s " % fname )
                         logger.debug(\
                             "poll_script exchange: %s url: %s to_cluster: %s partstr: %s " \
                             % (parent.exchange, msg.url, parent.to_clusters, msg.partstr) )

                         if islink: 
                             ok = parent.post1file(fname,fst)
                         else:
                             ok = parent.post1file(fname,fst)
                         #logger.info("test4 poll_script fname is: %s " % fname )
                  except:
                     logger.info("fname not found: %s " % fname )
                     pass
              logger.info("time for posting %s files: %s sec" % (nmsg, int(time.time() - stime)))

      return True 


poll_script = POLL_SCRIPT(self)
self.do_poll = poll_script.perform

