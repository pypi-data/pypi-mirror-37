# this causes file not found error!
# import subprocess
#
# cmd = ['pip', 'freeze']
# process = subprocess.Popen(
#     cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE,
#     stderr=subprocess.PIPE)
# stdoutdata = process.communicate()[0]
# freeze = stdoutdata.decode("utf-8").split('\n')
# freeze = [x for x in freeze if x]
#
# edc_packages = [
#     x for x in freeze if 'clinicedc' in x or 'erikvw' in x or 'edc-'in x]
# edc_packages.sort()
#
# third_party_packages = [x for x in freeze if x and x not in edc_packages]
# third_party_packages.sort()

edc_packages = []
third_party_packages = []
