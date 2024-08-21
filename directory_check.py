import subprocess


def run_command(command):
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        return f"Error: {result.stderr}"
    return result.stdout


def directory_check():
    output = {}

    output['targeted_directories'] = run_command('ls -lap /tmp /var/tmp /dev/shm /var/run /var/spool /home')
    output['hidden_directories'] = run_command('find / -type d -name ".*"')
    output['suid_sgid_files'] = run_command('find / -type f \\( -perm -04000 -o -perm -02000 \\) -exec ls -lg {} \\;')
    output['immutable_files'] = run_command('lsattr / -R 2> /dev/null | grep "\\----i"')
    output['orphaned_files'] = run_command('find / \\( -nouser -o -nogroup \\) -exec ls -lg {} \\;')

    return output