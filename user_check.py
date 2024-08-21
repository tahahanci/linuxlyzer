import subprocess


def run_command(command):
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        return f"Error: {result.stderr}"
    return result.stdout


def user_check():
    output = {}

    output['authorized_keys'] = run_command('find / -name authorized_keys')
    output['history_files'] = run_command('find / -name .*history')
    output['history_files_dev_null'] = run_command('ls -alR / 2> /dev/null | grep .*history | grep null')
    output['uid_0_gid_0_users'] = run_command('grep ":0:" /etc/passwd')
    output['sudoers_file'] = run_command('cat /etc/sudoers')
    output['group_file'] = run_command('cat /etc/group')
    output['crontab'] = run_command('crontab -l')
    output['atq'] = run_command('atq')
    output['systemctl_timers'] = run_command('systemctl list-timers --all')

    return output