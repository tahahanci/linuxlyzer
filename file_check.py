import subprocess


def run_command(command):
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        return f"Error: {result.stderr}"
    return result.stdout


def file_check():
    output = {}

    output['immutable_files'] = run_command('lsattr / -R 2> /dev/null | grep "\\----i"')
    output['suid_sgid_files'] = run_command('find / -type f \\( -perm -04000 -o -perm -02000 \\) -exec ls -lg {} \\;')
    output['orphaned_files'] = run_command('find / \\( -nouser -o -nogroup \\) -exec ls -lg {} \\;')
    output['file_types'] = run_command('file * -p')
    output['executables'] = run_command('find / -type f -exec file -p \'{}\' \\; | grep ELF')
    output['tmp_executables'] = run_command('find /tmp -type f -exec file -p \'{}\' \\; | grep ELF')
    output['recent_files'] = run_command('find / -mtime -1')
    output['persistence_areas'] = run_command(
        'ls /etc/rc.local /etc/initd /etc/rc*.d /etc/modules /etc/cron* /var/spool/cron/* 2> /dev/null')
    output['changed_files_rpm'] = run_command('rpm -Va | grep ^..5.')
    output['changed_files_debsums'] = run_command('debsums -c')

    return output