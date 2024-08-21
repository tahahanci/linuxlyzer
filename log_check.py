import subprocess


def run_command(command):
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        return f"Error: {result.stderr}"
    return result.stdout


def log_check():
    output = {}

    output['zero_size_logs'] = run_command('ls -al /var/log/*')
    output['utmpdump_wtmp'] = run_command('utmpdump /var/log/wtmp')
    output['utmpdump_utmp'] = run_command('utmpdump /var/run/utmp')
    output['utmpdump_btmp'] = run_command('utmpdump /var/log/btmp')
    output['last'] = run_command('last')
    output['lastb'] = run_command('lastb')
    output['binary_logs'] = run_command('grep [[:cntrl:]] /var/log/*.log')
    output['promiscuous_mode_logs'] = run_command('grep "entered promiscuous mode" /var/log/*')
    output['auth_failures'] = run_command('grep -i "failed" /var/log/auth.log /var/log/secure')
    output['rpc_strange_chars'] = run_command('grep -E ".{20,}" /var/log/rpc*.log')
    output['apache_errors'] = run_command('grep "error" /var/log/apache2/error.log /var/log/httpd/error_log')
    output['reboots_restarts'] = run_command('grep -i "reboot" /var/log/messages /var/log/syslog')

    return output