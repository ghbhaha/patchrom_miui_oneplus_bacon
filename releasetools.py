import common
import edify_generator

def RemoveDeviceAssert(info):
  edify = info.script
  for i in xrange(len(edify.script)):
    if "assert" in edify.script[i]:
      edify.script[i] = ''
      return

def RemoveDeviceGetprop(info):
  edify = info.script
  for i in xrange(len(edify.script)):
    if "getprop" in edify.script[i]:
      edify.script[i] = ''
      return

def AddAssertions(info):
    edify = info.script
    for i in xrange(len(edify.script)):
        if " ||" in edify.script[i] and ("ro.product.device" in edify.script[i] or "ro.build.product" in edify.script[i]):
            edify.script[i] = edify.script[i].replace(" ||", ' || getprop("ro.build.product") == "A0001 || getprop("ro.product.device") == "NX507J" || getprop("ro.build.product") == "A0001" ||')
            return


def MountSystem(info):
  edify = info.script
  for i in xrange(len(edify.script)):
    if "unmount(" in edify.script[i] and "/system" in edify.script[i]:
      edify.script[i] = 'mount("ext4", "EMMC", "/dev/block/platform/msm_sdcc.1/by-name/system", "/system");'
      return

def DeleteSystem(info):
  edify = info.script
  for i in xrange(len(edify.script)):
    if "format(" in edify.script[i] and "/dev/block/platform/msm_sdcc.1/by-name/system" in edify.script[i]:
      edify.script[i] = 'delete_recursive("/system");'
      return

def WritePolicyConfig(info):
  try:
    file_contexts = info.input_zip.read("META/file_contexts")
    common.ZipWriteStr(info.output_zip, "file_contexts", file_contexts)
  except KeyError:
    print "warning: file_context missing from target;"

def AddArgsForSetPermission(info):
  edify = info.script
  for i in xrange(len(edify.script)):
    if "set_perm(" in edify.script[i] and "/system/xbin/lbesec" in edify.script[i]:
      edify.script[i] = 'set_perm(0, 0, 06755, "/system/xbin/lbesec");'
      return
	  
def InstallImage(img_name, img_file, partition, info):
  common.ZipWriteStr(info.output_zip, img_name, img_file)
  info.script.AppendExtra(('package_extract_file("' + img_name + '", "' + partition + '");'))

def FullOTA_InstallRecovery(info):
  img_file = info.input_zip.read("BOOTABLE_IMAGES/recovery.img")
  info.script.Print("Writing recovery")
  InstallImage("recovery.img", img_file, "/dev/block/platform/msm_sdcc.1/by-name/recovery", info)

def IncrementalOTA_InstallRecovery(info):
  try:
    source_file = info.source_zip.read("BOOTABLE_IMAGES/recovery.img")
    target_file = info.target_zip.read("BOOTABLE_IMAGES/recovery.img")
    if source_file != target_file:
      info.script.Print("Writing recovery")
      InstallImage("recovery.img", target_file, "/dev/block/platform/msm_sdcc.1/by-name/recovery", info)
    else:
      print "recovery unchanged; skipping"
  except KeyError:
    print "warning: recovery missing from target"

def FullOTA_InstallEnd(info):
    RemoveDeviceGetprop(info)
    MountSystem(info)
    DeleteSystem(info)
    AddArgsForSetPermission(info)
    WritePolicyConfig(info)

def IncrementalOTA_InstallEnd(info):
    RemoveDeviceAssert(info)
    RemoveDeviceGetprop(info)
    AddArgsForSetPermission(info)
